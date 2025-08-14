# PyInstaller打包工具.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import shlex
import sys
import shutil
import site
import fnmatch
import re
import time

# 保障能导入同目录下的 i18n 包
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ---------------- i18n 导入 ----------------
try:
    from i18n import get_translator, detect_language_code
except Exception:
    def get_translator(lang_code):
        def _t(k, **kw):
            return k.format(**kw) if kw else k
        return _t
    def detect_language_code():
        return "en_US"


# ---------------- 高 DPI 支持（优先在 Tk 启动前设置） ----------------
def apply_high_dpi_awareness():
    if sys.platform.startswith('win'):
        try:
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-Monitor V2
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class Tooltip:
    """简易气泡提示：鼠标悬停显示文本（文本由 i18n 提供，仅一种语言）"""
    def __init__(self, widget, text, delay=600, wraplength=380):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wraplength = wraplength
        self._after_id = None
        self.tipwin = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._unschedule)
        widget.bind("<ButtonPress>", self._unschedule)

    def _schedule(self, _event=None):
        self._unschedule()
        self._after_id = self.widget.after(self.delay, self._show)

    def _unschedule(self, _event=None):
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        self._hide()

    def _show(self):
        if self.tipwin or not self.text:
            return
        try:
            x, y, cx, cy = self.widget.bbox("insert") or (0, 0, 0, 0)
        except Exception:
            x, y, cx, cy = (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + cy + 20
        self.tipwin = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#FFFFE0",
            relief=tk.SOLID,
            borderwidth=1,
            wraplength=self.wraplength
        )
        label.pack(ipadx=8, ipady=6)

    def _hide(self):
        if self.tipwin:
            try:
                self.tipwin.destroy()
            except Exception:
                pass
            self.tipwin = None


class ScrollableFrame(ttk.Frame):
    """可滚动容器：自动同步内部宽度与滚动区域（稳定版滚轮绑定）"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)

        self.inner = ttk.Frame(self.canvas)
        self._win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # 布局
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 更新滚动区域与宽度同步
        self.inner.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # 全局滚轮绑定（Win/macOS）
        self.inner.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux 上的滚轮
        self.inner.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.inner.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _on_frame_configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        try:
            self.canvas.itemconfig(self._win_id, width=event.width)
        except Exception:
            pass

    def _on_mousewheel(self, event):
        delta = int(-1 * (event.delta / 120))
        self.canvas.yview_scroll(delta, "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def refresh(self):
        self.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        try:
            self.canvas.itemconfig(self._win_id, width=self.canvas.winfo_width())
        except Exception:
            pass


def parse_version_tuple(vstr: str):
    if not vstr:
        return None
    parts = re.findall(r"\d+", vstr)
    if not parts:
        return None
    return tuple(int(x) for x in parts[:3])


def detect_pyinstaller_version():
    """返回 (version_tuple, version_str)。未安装或无法检测时返回 (None, None)"""
    vstr = None
    try:
        import PyInstaller  # noqa
        vstr = getattr(sys.modules['PyInstaller'], '__version__', None)
    except Exception:
        vstr = None

    if not vstr:
        cmds = [
            [sys.executable, "-m", "PyInstaller", "--version"],
            ["pyinstaller", "--version"],
        ]
        for cmd in cmds:
            try:
                out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=8)
                text = (out.stdout or "").strip()
                if text:
                    first = text.splitlines()[0].strip()
                    vstr = first
                    break
            except Exception:
                pass
    return parse_version_tuple(vstr), vstr


# ---------------- 简单的安装等待窗口（不可关闭） ----------------
class InstallWaitingDialog(tk.Toplevel):
    def __init__(self, parent, title, label_text):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        # 禁用右上角关闭按钮
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        # 置顶 & 模态（父窗未映射时不设 transient，强制顶置+lift）
        try:
            if parent and parent.winfo_ismapped():
                self.transient(parent)
            self.grab_set()
            self.attributes("-topmost", True)
            self.lift()
            self.after(300, lambda: self.attributes("-topmost", False))
        except Exception:
            pass

        frm = ttk.Frame(self, padding=16)
        frm.grid(row=0, column=0, sticky="nsew")
        frm.columnconfigure(0, weight=1)

        lbl = ttk.Label(frm, text=label_text, justify="left")
        lbl.grid(row=0, column=0, sticky="w")

        # 不定进度动画（视觉反馈，不显示百分比）
        self.bar = ttk.Progressbar(frm, orient="horizontal", mode="indeterminate", length=360)
        self.bar.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        try:
            self.bar.start(10)  # 数值越小越快
        except Exception:
            pass

        # 居中
        self.update_idletasks()
        self._center(parent)

    def _center(self, parent):
        try:
            self.update_idletasks()
            # 如果父窗已隐藏，改用屏幕中心
            if not parent or not parent.winfo_ismapped():
                sw = self.winfo_screenwidth()
                sh = self.winfo_screenheight()
                w = self.winfo_reqwidth()
                h = self.winfo_reqheight()
                x = (sw - w) // 2
                y = (sh - h) // 3
            else:
                px, py = parent.winfo_rootx(), parent.winfo_rooty()
                pw, ph = parent.winfo_width(), parent.winfo_height()
                w, h = self.winfo_reqwidth(), self.winfo_reqheight()
                x = px + (pw - w) // 2
                y = py + (ph - h) // 2
            self.geometry(f"+{max(0,x)}+{max(0,y)}")
        except Exception:
            pass


# ---------------- 冻结态（exe）支持：外部 PyInstaller 与 Python 处理 ----------------
def is_frozen_app() -> bool:
    return bool(getattr(sys, "frozen", False))

def _split_cmd(cmd_str: str):
    try:
        return shlex.split(cmd_str)
    except Exception:
        return [cmd_str]

def get_python_candidates() -> list:
    # 优先顺序：Windows 上 'py -3' → 'python' → 'python3'；其它平台 'python3' → 'python'
    if sys.platform.startswith('win'):
        return [_split_cmd("py -3"), _split_cmd("python"), _split_cmd("python3")]
    else:
        return [_split_cmd("python3"), _split_cmd("python")]

def external_pyinstaller_probe():
    """
    返回 (mode, value)
      - ('exe', 'pyinstaller_path') 表示直接可调用 pyinstaller(.exe)
      - ('py',  ['python','-m','PyInstaller']) 表示可用外部 Python -m PyInstaller
      - (None, None) 表示未找到
    """
    exe = shutil.which("pyinstaller")
    if exe:
        return ("exe", exe)

    for py_cmd in get_python_candidates():
        try:
            res = subprocess.run(py_cmd + ["-m", "PyInstaller", "--version"],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, timeout=8)
            if res.returncode == 0 and (res.stdout or "").strip():
                return ("py", py_cmd)
        except Exception:
            pass
    return (None, None)

def ensure_pip_then_install(py_cmd: list, pkg: str, use_tsinghua: bool) -> bool:
    """
    在外部 Python 上安装 pkg。若 pip 缺失，先 ensurepip。
    """
    def _run(cmd):
        try:
            creationflags = 0
            if sys.platform.startswith('win') and hasattr(subprocess, "CREATE_NO_WINDOW"):
                creationflags = subprocess.CREATE_NO_WINDOW
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, creationflags=creationflags)
            return p.returncode == 0
        except Exception:
            return False

    # 先试 pip 安装
    base = py_cmd + ["-m", "pip", "install", "--upgrade", pkg]
    if use_tsinghua:
        base += ["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
    if _run(base):
        return True

    # 尝试 ensurepip，再次安装
    _run(py_cmd + ["-m", "ensurepip", "--upgrade"])
    return _run(base)


def install_pyinstaller_waiting(root, lang_code, _, py_cmd_external: list | None = None):
    """
    显示不可关闭的等待窗口，安装 PyInstaller。
    - 非 frozen：默认用当前解释器 pip 安装（与旧逻辑一致）
    - frozen：必须传入 py_cmd_external（例如 ['py','-3'] 或 ['python']），用其 pip 安装
    成功 True / 失败 False
    """
    title = _("install_window_title")
    if title == "install_window_title":
        title = "安装 PyInstaller" if lang_code.lower().startswith("zh") else "Installing PyInstaller"
    label_text = _("install_progress_label_wait")
    if label_text == "install_progress_label_wait":
        label_text = ("正在安装 PyInstaller（窗口将自动关闭），安装速度取决于网速，请耐心等待…"
                      if lang_code.lower().startswith("zh")
                      else "Installing PyInstaller (this window will close automatically). Speed depends on your network…")

    dlg = InstallWaitingDialog(root, title, label_text)
    dlg.update(); dlg.lift()

    result = {"ok": False}

    def worker():
        try:
            use_tsinghua = (lang_code.lower().startswith("zh_cn"))
            if is_frozen_app():
                if not py_cmd_external:
                    result["ok"] = False
                else:
                    result["ok"] = ensure_pip_then_install(py_cmd_external, "pyinstaller", use_tsinghua)
            else:
                pip_cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"]
                if use_tsinghua:
                    pip_cmd += ["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
                creationflags = 0
                if sys.platform.startswith('win') and hasattr(subprocess, "CREATE_NO_WINDOW"):
                    creationflags = subprocess.CREATE_NO_WINDOW
                try:
                    p = subprocess.Popen(pip_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                         text=True, creationflags=creationflags)
                    for _ in iter(p.stdout.readline, ''):
                        pass
                    result["ok"] = (p.wait() == 0)
                except Exception:
                    result["ok"] = False
        except Exception:
            result["ok"] = False

    th = threading.Thread(target=worker, daemon=True)
    th.start()
    while th.is_alive():
        try:
            root.update()
        except Exception:
            pass
        time.sleep(0.02)

    try:
        dlg.bar.stop()
    except Exception:
        pass
    try:
        dlg.grab_release()
    except Exception:
        pass
    try:
        dlg.destroy()
    except Exception:
        pass

    return bool(result["ok"])


class PyInstallerGUI:
    def __init__(self, root):
        # 翻译器（只显示一种语言）
        lang_code = detect_language_code()
        self._ = get_translator(lang_code)
        self.lang_code = lang_code

        # 关闭流程标记 & tooltip 列表
        self.is_closing = False
        self._tooltips = []

        # 检测 PyInstaller 版本（用于 UI/参数兼容）
        self.pyi_version_tuple, self.pyi_version_str = detect_pyinstaller_version()
        self.has_winsxs_opts = bool(
            sys.platform.startswith('win') and self.pyi_version_tuple and self.pyi_version_tuple < (6, 0)
        )
        if self.pyi_version_tuple is None:
            self.has_winsxs_opts = False

        self.root = root
        self.root.title(self._("app_title"))

        # 初始窗口大小与最小值
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        init_w = min(980, int(sw * 0.9))
        init_h = min(760, int(sh * 0.9))
        self.root.geometry(f"{init_w}x{init_h}")
        self.root.minsize(720, 560)
        self.root.resizable(True, True)

        # 主框架与选项卡
        self.main_frame = ttk.Frame(root, padding="8")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # 页面
        self.page_basic = ttk.Frame(self.notebook)
        self.notebook.add(self.page_basic, text=self._("tab_basic"))
        self.page_basic.columnconfigure(0, weight=1)

        self.page_assets_scroll = ScrollableFrame(self.notebook)
        self.page_assets = self.page_assets_scroll.inner
        self.notebook.add(self.page_assets_scroll, text=self._("tab_assets"))
        self.page_assets.columnconfigure(0, weight=1)

        self.page_adv_scroll = ScrollableFrame(self.notebook)
        self.page_advanced = self.page_adv_scroll.inner
        self.notebook.add(self.page_adv_scroll, text=self._("tab_advanced"))
        self.page_advanced.columnconfigure(0, weight=1)

        self.page_logs = ttk.Frame(self.notebook)
        self.notebook.add(self.page_logs, text=self._("tab_logs"))
        self.page_logs.rowconfigure(0, weight=1)
        self.page_logs.columnconfigure(0, weight=1)

        # 数据区
        self.script_path = ""
        self.icon_path = ""
        self.version_file_path = ""
        self.resources_list = []
        self.hidden_imports_list = []
        self.exclude_modules_list = []
        self.hooks_dir_list = []
        self.runtime_hooks_list = []
        self.upx_exclude_list = []
        self.upx_available = None  # None/True/False
        self.win_no_prefer_redirects = tk.BooleanVar(value=False)
        self.win_private_assemblies = tk.BooleanVar(value=False)

        # 构建各页面 UI 与操作按钮
        self.build_page_basic()
        self.build_page_assets()
        self.build_page_advanced()
        self.build_page_logs()
        self.create_action_buttons()

        # 绑定关闭协议
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # 刷新滚动容器
        self.page_assets_scroll.refresh()
        self.page_adv_scroll.refresh()
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self._refresh_scrollables())

    def _refresh_scrollables(self):
        if hasattr(self, "page_assets_scroll"):
            self.page_assets_scroll.refresh()
        if hasattr(self, "page_adv_scroll"):
            self.page_adv_scroll.refresh()

    # 统一加提示（文本由 i18n 提供）
    def add_tip(self, widget, key):
        try:
            text = self._(key)
            if text and text != key:
                t = Tooltip(widget, text)
                self._tooltips.append(t)
        except Exception:
            pass

    # --------------------- 页面构建 ---------------------
    def build_page_basic(self):
        # 脚本设置
        file_frame = ttk.LabelFrame(self.page_basic, text=self._("group_script_settings"), padding=(10, 8))
        file_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text=self._("label_main_script")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.script_entry = ttk.Entry(file_frame)
        self.script_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.add_tip(self.script_entry, "tip_main_script")
        btn = ttk.Button(file_frame, text=self._("btn_browse"), command=self.select_script)
        btn.grid(row=0, column=2, padx=5, pady=5)
        self.add_tip(btn, "tip_browse_script")

        ttk.Label(file_frame, text=self._("label_output_name")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(file_frame)
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.add_tip(self.name_entry, "tip_output_name")

        ttk.Label(file_frame, text=self._("label_output_dir")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.distpath_entry = ttk.Entry(file_frame)
        self.distpath_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.add_tip(self.distpath_entry, "tip_distpath")
        btn = ttk.Button(file_frame, text=self._("btn_browse"), command=self.select_distpath)
        btn.grid(row=2, column=2, padx=5, pady=5)
        self.add_tip(btn, "tip_browse_dist")
        self.distpath_entry.insert(0, os.path.abspath("dist"))

        # 打包选项
        opt_frame = ttk.LabelFrame(self.page_basic, text=self._("group_build_options"), padding=(10, 8))
        opt_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(4):
            opt_frame.columnconfigure(i, weight=1 if i == 1 else 0)

        ttk.Label(opt_frame, text=self._("label_pack_mode")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.mode_var = tk.StringVar(value="-F")
        rb = ttk.Radiobutton(opt_frame, text=self._("radio_onefile"), variable=self.mode_var, value="-F")
        rb.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.add_tip(rb, "tip_onefile")
        rb = ttk.Radiobutton(opt_frame, text=self._("radio_onedir"), variable=self.mode_var, value="-D")
        rb.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.add_tip(rb, "tip_onedir")

        ttk.Label(opt_frame, text=self._("label_console")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.console_var = tk.StringVar(value="-c")
        rb = ttk.Radiobutton(opt_frame, text=self._("radio_console"), variable=self.console_var, value="-c")
        rb.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.add_tip(rb, "tip_console")
        rb = ttk.Radiobutton(opt_frame, text=self._("radio_windowed"), variable=self.console_var, value="-w")
        rb.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.add_tip(rb, "tip_windowed")

        ttk.Label(opt_frame, text=self._("label_app_icon")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.icon_entry = ttk.Entry(opt_frame)
        self.icon_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.add_tip(self.icon_entry, "tip_icon")
        btn = ttk.Button(opt_frame, text=self._("btn_browse"), command=self.select_icon)
        btn.grid(row=2, column=2, padx=5, pady=5)
        self.add_tip(btn, "tip_browse_icon")

        ttk.Label(opt_frame, text=self._("label_version_file")).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.version_entry = ttk.Entry(opt_frame)
        self.version_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        self.add_tip(self.version_entry, "tip_version_file")
        btn = ttk.Button(opt_frame, text=self._("btn_browse"), command=self.select_version_file)
        btn.grid(row=3, column=2, padx=5, pady=5)
        self.add_tip(btn, "tip_browse_version")

        # ========== UPX 选项区域 ==========
        upx_row = ttk.Frame(opt_frame)
        upx_row.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 5))
        upx_row.columnconfigure(1, weight=1)

        # 变量
        self.upx_var = tk.BooleanVar(value=True)            # 使用UPX（总开关）
        self.upx_force_var = tk.BooleanVar(value=False)     # 仅外压生效
        self.upx_internal_var = tk.BooleanVar(value=False)  # 是否使用内置UPX
        self.upx_external_dlls_only_var = tk.BooleanVar(value=False)  # 仅压 DLL/PYD，不压主 EXE（仅 -D）

        # 0：使用 UPX（总开关）
        self.cb_use_upx = ttk.Checkbutton(upx_row, text=self._("check_use_upx"), variable=self.upx_var)
        self.cb_use_upx.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 6))
        self.add_tip(self.cb_use_upx, "tip_use_upx")

        # 1：使用内置 UPX（放在滑块上方、靠左）
        self.cb_upx_internal = ttk.Checkbutton(upx_row, text=self._("check_upx_internal"), variable=self.upx_internal_var)
        self.cb_upx_internal.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 6))
        self.add_tip(self.cb_upx_internal, "tip_upx_internal")

        # 2：UPX 压缩级别（外压时可用）—— 无刻度 + 右侧数字
        self.lbl_upx_level = ttk.Label(upx_row, text=self._("label_upx_level"))
        self.lbl_upx_level.grid(row=2, column=0, sticky="w", padx=(0, 8))
        self.upx_level_var = tk.DoubleVar(value=5)
        self.upx_level_scale = ttk.Scale(
            upx_row, from_=1, to=10, orient="horizontal",
            variable=self.upx_level_var, command=lambda v: self._on_upx_level_changed(v)
        )
        self.upx_level_scale.grid(row=2, column=1, sticky="ew")
        self.add_tip(self.upx_level_scale, "tip_upx_level")
        self.upx_level_value = ttk.Label(upx_row, text="5")
        self.upx_level_value.grid(row=2, column=2, sticky="w", padx=(8, 0))

        # 3+4：同一行 —— 左“--force”，右“仅压 DLL/PYD，不压主 EXE”（只在 -D 显示）
        self.upx_force_cb = ttk.Checkbutton(upx_row, text=self._("check_upx_force"), variable=self.upx_force_var)
        self.upx_force_cb.grid(row=4, column=0, sticky="w", padx=0, pady=(6, 0))
        self.add_tip(self.upx_force_cb, "tip_upx_force")

        self.cb_only_libs = ttk.Checkbutton(
            upx_row, text=self._("check_upx_only_libs"),
            variable=self.upx_external_dlls_only_var
        )
        self.cb_only_libs.grid(row=4, column=1, sticky="w", padx=(12, 0), pady=(6, 0))
        self.add_tip(self.cb_only_libs, "tip_upx_only_libs")

        # 响应模式/UPX切换
        self.upx_var.trace_add("write", lambda *a: self._update_upx_controls_state())
        self.upx_internal_var.trace_add("write", lambda *a: self._update_upx_controls_state())
        self.upx_force_var.trace_add("write", lambda *a: self._update_upx_controls_state())
        self.mode_var.trace_add("write", lambda *a: (self._update_only_libs_visibility(), self._update_upx_controls_state()))
        # 初始状态
        self._update_only_libs_visibility()
        self._update_upx_controls_state()

        # 调试等级
        ttk.Label(opt_frame, text=self._("label_debug_level")).grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.debug_map = {
            self._("debug_off"): None,
            self._("debug_all"): "all",
            self._("debug_imports"): "imports",
            self._("debug_noarchive"): "noarchive",
        }
        self.debug_level = tk.StringVar(value=self._("debug_off"))
        self.debug_combo = ttk.Combobox(opt_frame, textvariable=self.debug_level, state="readonly",
                                        values=list(self.debug_map.keys()), width=20)
        self.debug_combo.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        self.add_tip(self.debug_combo, "tip_debug")

    def _update_only_libs_visibility(self):
        """根据打包模式隐藏/显示“仅压 DLL/PYD，不压主 EXE”（放在 --force 的右边：row=4, col=1）"""
        try:
            if self.mode_var.get() == "-D":
                self.cb_only_libs.grid_configure(row=4, column=1, sticky="w", padx=(12, 0), pady=(6, 0))
                self.cb_only_libs.grid()
            else:
                self.cb_only_libs.grid_remove()
        except Exception:
            pass

    def build_page_assets(self):
        frame = self.page_assets

        # 附加资源（统一管理文件/目录）
        lf_res = ttk.LabelFrame(frame, text=self._("group_data"), padding=(10, 8))
        lf_res.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        lf_res.columnconfigure(0, weight=1)

        self.res_frame = ttk.Frame(lf_res)
        self.res_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 6))
        self.res_frame.columnconfigure(0, weight=1)

        self.resource_entry = ttk.Entry(self.res_frame)
        self.resource_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.add_tip(self.resource_entry, "tip_data_add")
        btn = ttk.Button(self.res_frame, text=self._("btn_browse_file"), width=10, command=self.select_resource_file)
        btn.grid(row=0, column=1, padx=2)
        self.add_tip(btn, "tip_browse_res_file")
        btn = ttk.Button(self.res_frame, text=self._("btn_browse_dir"), width=10, command=self.select_resource_dir)
        btn.grid(row=0, column=2, padx=2)
        self.add_tip(btn, "tip_browse_res_dir")
        btn = ttk.Button(self.res_frame, text=self._("btn_add"), width=8, command=self.add_resource)
        btn.grid(row=0, column=3, padx=4)
        self.add_tip(btn, "tip_add_res")
        btn = ttk.Button(self.res_frame, text=self._("btn_clear"), width=8, command=self.clear_resources)
        btn.grid(row=0, column=4)
        self.add_tip(btn, "tip_clear_res")

        hint_text = self._("hint_resources_input") if self._("hint_resources_input") != "hint_resources_input" else ""
        if hint_text:
            ttk.Label(lf_res, text=hint_text, foreground="#666").grid(row=1, column=0, sticky="w", padx=0, pady=(0, 6))

        self.resource_listbox = tk.Listbox(lf_res, height=7, bg='white')
        self.resource_listbox.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        self.add_tip(self.resource_listbox, "tip_data_list")

        # 隐藏导入
        lf_hidden = ttk.LabelFrame(frame, text=self._("group_hidden_imports"), padding=(10, 8))
        lf_hidden.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        lf_hidden.columnconfigure(0, weight=1)
        self.hidden_frame = ttk.Frame(lf_hidden)
        self.hidden_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.hidden_frame.columnconfigure(0, weight=1)
        self.hidden_entry = ttk.Entry(self.hidden_frame)
        self.hidden_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.add_tip(self.hidden_entry, "tip_hidden_imports")
        btn = ttk.Button(self.hidden_frame, text=self._("btn_add"), width=8, command=self.add_hidden_import)
        btn.grid(row=0, column=1, padx=5)
        self.add_tip(btn, "tip_add_hidden")
        btn = ttk.Button(self.hidden_frame, text=self._("btn_clear"), width=8, command=self.clear_hidden_imports)
        btn.grid(row=0, column=2)
        self.add_tip(btn, "tip_clear_hidden")
        self.hidden_listbox = tk.Listbox(lf_hidden, height=4, bg='white')
        self.hidden_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.add_tip(self.hidden_listbox, "tip_hidden_list")

        # 排除模块
        lf_excl = ttk.LabelFrame(frame, text=self._("group_excludes"), padding=(10, 8))
        lf_excl.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        lf_excl.columnconfigure(0, weight=1)
        self.exclude_frame = ttk.Frame(lf_excl)
        self.exclude_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.exclude_frame.columnconfigure(0, weight=1)
        self.exclude_entry = ttk.Entry(self.exclude_frame)
        self.exclude_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.add_tip(self.exclude_entry, "tip_excludes")
        btn = ttk.Button(self.exclude_frame, text=self._("btn_add"), width=8, command=self.add_exclude_module)
        btn.grid(row=0, column=1, padx=5)
        self.add_tip(btn, "tip_add_exclude")
        btn = ttk.Button(self.exclude_frame, text=self._("btn_clear"), width=8, command=self.clear_exclude_modules)
        btn.grid(row=0, column=2)
        self.add_tip(btn, "tip_clear_exclude")
        self.exclude_listbox = tk.Listbox(lf_excl, height=4, bg='white')
        self.exclude_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.add_tip(self.exclude_listbox, "tip_excludes_list")

    def build_page_advanced(self):
        frame = self.page_advanced

        # 额外 Hooks 目录
        lf_hooks = ttk.LabelFrame(frame, text=self._("group_hooks_dir"), padding=(10, 8))
        lf_hooks.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        lf_hooks.columnconfigure(0, weight=1)
        self.hooks_dir_frame = ttk.Frame(lf_hooks)
        self.hooks_dir_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.hooks_dir_frame.columnconfigure(0, weight=1)
        self.hooks_dir_entry = ttk.Entry(self.hooks_dir_frame)
        self.hooks_dir_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.add_tip(self.hooks_dir_entry, "tip_hooks_dir")
        btn = ttk.Button(self.hooks_dir_frame, text=self._("btn_add"), width=8, command=self.add_hooks_dir)
        btn.grid(row=0, column=1, padx=5)
        self.add_tip(btn, "tip_add_hooks_dir")
        btn = ttk.Button(self.hooks_dir_frame, text=self._("btn_clear"), width=8, command=self.clear_hooks_dir)
        btn.grid(row=0, column=2)
        self.add_tip(btn, "tip_clear_hooks_dir")
        self.hooks_dir_listbox = tk.Listbox(lf_hooks, height=3, bg='white')
        self.hooks_dir_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.add_tip(self.hooks_dir_listbox, "tip_hooks_list")

        # 运行时 Hook
        lf_rth = ttk.LabelFrame(frame, text=self._("group_runtime_hooks"), padding=(10, 8))
        lf_rth.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        lf_rth.columnconfigure(0, weight=1)
        self.runtime_hook_frame = ttk.Frame(lf_rth)
        self.runtime_hook_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.runtime_hook_frame.columnconfigure(0, weight=1)
        self.runtime_hook_entry = ttk.Entry(self.runtime_hook_frame)
        self.runtime_hook_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.add_tip(self.runtime_hook_entry, "tip_runtime_hook")
        btn = ttk.Button(self.runtime_hook_frame, text=self._("btn_add"), width=8, command=self.add_runtime_hook)
        btn.grid(row=0, column=1, padx=5)
        self.add_tip(btn, "tip_add_runtime_hook")
        btn = ttk.Button(self.runtime_hook_frame, text=self._("btn_clear"), width=8, command=self.clear_runtime_hooks)
        btn.grid(row=0, column=2)
        self.add_tip(btn, "tip_clear_runtime_hook")
        self.runtime_hook_listbox = tk.Listbox(lf_rth, height=3, bg='white')
        self.runtime_hook_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.add_tip(self.runtime_hook_listbox, "tip_runtime_list")

        # UPX 排除
        lf_upx_ex = ttk.LabelFrame(frame, text=self._("group_upx_exclude"), padding=(10, 8))
        lf_upx_ex.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        lf_upx_ex.columnconfigure(0, weight=1)
        self.upx_excl_frame = ttk.Frame(lf_upx_ex)
        self.upx_excl_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.upx_excl_frame.columnconfigure(0, weight=1)
        self.upx_excl_entry = ttk.Entry(self.upx_excl_frame)
        self.upx_excl_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.add_tip(self.upx_excl_entry, "tip_upx_exclude")
        btn = ttk.Button(self.upx_excl_frame, text=self._("btn_add"), width=8, command=self.add_upx_exclude)
        btn.grid(row=0, column=1, padx=5)
        self.add_tip(btn, "tip_add_upx_exclude")
        btn = ttk.Button(self.upx_excl_frame, text=self._("btn_clear"), width=8, command=self.clear_upx_exclude)
        btn.grid(row=0, column=2)
        self.add_tip(btn, "tip_clear_upx_exclude")
        self.upx_excl_listbox = tk.Listbox(lf_upx_ex, height=3, bg='white')
        self.upx_excl_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.add_tip(self.upx_excl_listbox, "tip_upx_excl_list")

        # 其他开关（按版本显示 WinSxS）
        options_row = ttk.LabelFrame(frame, text=self._("group_other_switches"), padding=(10, 8))
        options_row.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.disable_windowed_tb = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(options_row, text=self._("check_disable_windowed_tb"), variable=self.disable_windowed_tb)
        cb.grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.add_tip(cb, "tip_disable_windowed_tb")

        if self.has_winsxs_opts:
            cb1 = ttk.Checkbutton(options_row, text=self._("check_win_no_prefer_redirects"), variable=self.win_no_prefer_redirects)
            cb1.grid(row=1, column=0, sticky="w", padx=5, pady=3)
            cb2 = ttk.Checkbutton(options_row, text=self._("check_win_private_assemblies"), variable=self.win_private_assemblies)
            cb2.grid(row=1, column=1, sticky="w", padx=5, pady=3)
        else:
            if sys.platform.startswith('win'):
                note = self._("note_winsxs_removed")
                if note != "note_winsxs_removed":
                    ttk.Label(options_row, text=note, foreground="#666").grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=(3, 0))

        # 运行时临时目录
        lf_rt = ttk.LabelFrame(frame, text=self._("label_runtime_tmpdir"), padding=(10, 8))
        lf_rt.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        lf_rt.columnconfigure(0, weight=1)
        self.runtime_tmpdir_entry = ttk.Entry(lf_rt)
        self.runtime_tmpdir_entry.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.add_tip(self.runtime_tmpdir_entry, "tip_runtime_tmpdir")

        # 额外参数
        lf_extra = ttk.LabelFrame(frame, text=self._("label_extra_args"), padding=(10, 8))
        lf_extra.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        lf_extra.columnconfigure(0, weight=1)
        self.extra_args_entry = ttk.Entry(lf_extra)
        self.extra_args_entry.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.add_tip(self.extra_args_entry, "tip_extra_args")

        self.page_adv_scroll.refresh()

    def build_page_logs(self):
        frame = self.page_logs
        self.console_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=10, bg='#23272A', fg='white')
        self.console_output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        try:
            self.console_output.tag_config('green', foreground='lightgreen')
        except Exception:
            pass
        ver = self.pyi_version_str or "unknown"
        self.add_to_console(f"[INFO] PyInstaller version detected: {ver}\n")
        self.add_to_console(self._("log_ready") + "\n")
        self.add_to_console(self._("log_select_script") + "\n")

    def create_action_buttons(self):
        frame = ttk.Frame(self.main_frame)
        frame.grid(row=1, column=0, sticky="e", padx=5, pady=6)

        self.btn_build = ttk.Button(frame, text=self._("btn_build"), command=self.start_build, width=15)
        self.btn_build.grid(row=0, column=0, padx=5)
        self.add_tip(self.btn_build, "tip_btn_build")

        self.btn_clean = ttk.Button(frame, text=self._("btn_clean_tmp"), command=self.clean_project, width=15)
        self.btn_clean.grid(row=0, column=1, padx=5)
        self.add_tip(self.btn_clean, "tip_btn_clean")

        self.btn_exit = ttk.Button(frame, text=self._("btn_exit"), command=self.on_close, width=15)
        self.btn_exit.grid(row=0, column=2, padx=5)
        self.add_tip(self.btn_exit, "tip_btn_exit")

    # --------------------- 事件处理/数据 ---------------------
    def _expand_path(self, p: str) -> str:
        return os.path.abspath(os.path.expanduser(os.path.expandvars(p.strip('"').strip("'"))))

    def _parse_resource_input(self, text: str):
        """返回 (abs_source, dest_rel) 或 None；支持 “源|目标” 或 “源=>目标”"""
        if not text:
            return None
        raw = text.strip()
        if "|" in raw:
            src, dest = raw.split("|", 1)
        elif "=>" in raw:
            src, dest = raw.split("=>", 1)
        else:
            src, dest = raw, None

        src = self._expand_path(src)
        if not os.path.exists(src):
            self.add_to_console(f"[WARN] 资源不存在：{src}\n")
            return None

        if dest:
            dest = dest.strip().lstrip("\\/")
        else:
            if os.path.isdir(src):
                dest = os.path.basename(os.path.normpath(src)) or "."
            else:
                dest = "."
        return (src, dest)

    def add_resource(self):
        item = self._parse_resource_input(self.resource_entry.get())
        if not item:
            return
        src, dest = item
        self.resources_list.append((src, dest))
        disp_dest = dest if dest else "."
        self.resource_listbox.insert(tk.END, f"{src} → {disp_dest}")
        self.resource_entry.delete(0, tk.END)

    def clear_resources(self):
        self.resources_list = []
        self.resource_listbox.delete(0, tk.END)

    def select_resource_file(self):
        p = filedialog.askopenfilename(title=self._("title_select_resource_file"), parent=self.root)
        if p:
            self.resource_entry.delete(0, tk.END)
            self.resource_entry.insert(0, p)

    def select_resource_dir(self):
        p = filedialog.askdirectory(title=self._("title_select_resource_dir"), mustexist=True)
        if p:
            self.resource_entry.delete(0, tk.END)
            self.resource_entry.insert(0, p)

    def select_script(self):
        script_path = filedialog.askopenfilename(
            filetypes=[(self._("filter_py"), "*.py"), (self._("filter_all"), "*.*")],
            parent=self.root
        )
        if script_path:
            self.script_path = os.path.abspath(script_path)
            self.script_entry.delete(0, tk.END)
            self.script_entry.insert(0, self.script_path)
            file_name = os.path.splitext(os.path.basename(script_path))[0]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, file_name)

    def select_distpath(self):
        distpath = filedialog.askdirectory(parent=self.root)
        if distpath:
            self.distpath_entry.delete(0, tk.END)
            self.distpath_entry.insert(0, os.path.abspath(distpath))

    def select_icon(self):
        icon_path = filedialog.askopenfilename(
            filetypes=[(self._("filter_ico"), "*.ico"), (self._("filter_all"), "*.*")],
            parent=self.root
        )
        if icon_path:
            self.icon_path = os.path.abspath(icon_path)
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, self.icon_path)

    def select_version_file(self):
        ver_path = filedialog.askopenfilename(
            title=self._("title_select_version_file"),
            filetypes=[(self._("filter_version"), "*.txt;*.ver;*.version"), (self._("filter_all"), "*.*")],
            parent=self.root
        )
        if ver_path:
            self.version_file_path = os.path.abspath(ver_path)
            self.version_entry.delete(0, tk.END)
            self.version_entry.insert(0, self.version_file_path)

    def add_hidden_import(self):
        mod = self.hidden_entry.get().strip()
        if mod:
            self.hidden_imports_list.append(mod)
            self.hidden_listbox.insert(tk.END, mod)
            self.hidden_entry.delete(0, tk.END)

    def clear_hidden_imports(self):
        self.hidden_imports_list = []
        self.hidden_listbox.delete(0, tk.END)

    def add_exclude_module(self):
        mod = self.exclude_entry.get().strip()
        if mod:
            self.exclude_modules_list.append(mod)
            self.exclude_listbox.insert(tk.END, mod)
            self.exclude_entry.delete(0, tk.END)

    def clear_exclude_modules(self):
        self.exclude_modules_list = []
        self.exclude_listbox.delete(0, tk.END)

    def add_hooks_dir(self):
        p = self.hooks_dir_entry.get().strip()
        if p:
            p = os.path.abspath(p)
            self.hooks_dir_list.append(p)
            self.hooks_dir_listbox.insert(tk.END, p)
            self.hooks_dir_entry.delete(0, tk.END)

    def clear_hooks_dir(self):
        self.hooks_dir_list = []
        self.hooks_dir_listbox.delete(0, tk.END)

    def add_runtime_hook(self):
        p = self.runtime_hook_entry.get().strip()
        if p:
            p = os.path.abspath(p)
            self.runtime_hooks_list.append(p)
            self.runtime_hook_listbox.insert(tk.END, p)
            self.runtime_hook_entry.delete(0, tk.END)

    def clear_runtime_hooks(self):
        self.runtime_hooks_list = []
        self.runtime_hook_listbox.delete(0, tk.END)

    def add_upx_exclude(self):
        pat = self.upx_excl_entry.get().strip()
        if pat:
            self.upx_exclude_list.append(pat)
            self.upx_excl_listbox.insert(tk.END, pat)
            self.upx_excl_entry.delete(0, tk.END)

    def clear_upx_exclude(self):
        self.upx_exclude_list = []
        self.upx_excl_listbox.delete(0, tk.END)

    # --------------------- 控制台输出（关闭后拦截） ---------------------
    def add_to_console(self, text):
        if self.is_closing:
            return
        try:
            self.console_output.insert(tk.END, text)
            self.console_output.see(tk.END)
            self.console_output.update_idletasks()
        except Exception:
            pass

    def add_colored(self, text, tag='green'):
        if self.is_closing:
            return
        try:
            self.console_output.insert(tk.END, text, tag)
            self.console_output.see(tk.END)
            self.console_output.update_idletasks()
        except Exception:
            pass

    # --------------------- UPX 控件与后处理 ---------------------
    def _on_upx_level_changed(self, val):
        try:
            v = int(round(float(val)))
        except Exception:
            v = 5
        v = max(1, min(10, v))
        self.upx_level_value.config(text=str(v))

    def _update_upx_controls_state(self):
        """统一根据『使用UPX』总开关 + 内置/外压 + 模式(-F/-D) 切换控件状态"""
        use_upx = self.upx_var.get()
        use_internal = self.upx_internal_var.get()
        external_enabled = use_upx and (not use_internal)

        try:
            self.cb_upx_internal.configure(state="normal" if use_upx else "disabled")
        except Exception:
            pass

        try:
            self.upx_level_scale.configure(state="normal" if external_enabled else "disabled")
        except Exception:
            pass
        try:
            self.upx_level_value.configure(state="normal" if external_enabled else "disabled")
        except Exception:
            pass

        try:
            self.upx_force_cb.configure(state="normal" if external_enabled else "disabled")
        except Exception:
            pass

        try:
            only_libs_state = "normal" if (external_enabled and self.mode_var.get() == "-D") else "disabled"
            self.cb_only_libs.configure(state=only_libs_state)
        except Exception:
            pass

    def _upx_is_excluded(self, path: str) -> bool:
        p = path.replace("\\", "/")
        base = os.path.basename(p)
        for pat in self.upx_exclude_list:
            pat = (pat or "").strip()
            if not pat:
                continue
            if fnmatch.fnmatch(base, pat) or fnmatch.fnmatch(p, pat) or pat in base:
                return True
        return False

    def post_upx_compress(self):
        """构建成功后按滑块级别运行 UPX（仅外压）。
        遇到 GUARD_CF/CFG 且未启用 --force 时跳过并提示绿色引导。
        """
        if not self.upx_var.get() or self.upx_internal_var.get():
            return
        if self.upx_available is False:
            return

        try:
            level = int(round(float(self.upx_level_var.get())))
        except Exception:
            level = 5
        level = max(1, min(10, level))
        lvl_arg = f"-{min(level, 9)}"  # 10 等价 9

        dist_root = os.path.abspath(self.distpath_entry.get().strip() or "dist")
        name = (self.name_entry.get().strip()
                or (os.path.splitext(os.path.basename(self.script_path))[0] if self.script_path else ""))

        # 收集候选
        candidates, exts = [], {".exe", ".dll", ".pyd", ".so", ".dylib"}
        if self.mode_var.get() == "-F":
            exe_name = f"{name}.exe" if sys.platform.startswith('win') else name
            exe_path = os.path.join(dist_root, exe_name)
            if os.path.isfile(exe_path):
                candidates.append(exe_path)
        else:
            folder = os.path.join(dist_root, name)
            search_root = folder if os.path.isdir(folder) else dist_root
            for root_dir, _dirs, files in os.walk(search_root):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in exts:
                        path = os.path.join(root_dir, f)
                        if not self._upx_is_excluded(path):
                            candidates.append(path)

        uniq, seen = [], set()
        for p in candidates:
            if p not in seen and os.path.isfile(p):
                uniq.append(p); seen.add(p)

        if not uniq:
            self.add_to_console("[INFO] 没有可进行 UPX 压缩的目标文件。\n")
            return

        self.add_to_console(f"[INFO] 正在应用 UPX 压缩级别 {level}，目标文件数：{len(uniq)} ...\n")
        base_cmd = ["upx", "-q", "--no-progress", lvl_arg]
        if self.upx_force_var.get():
            base_cmd.append("--force")

        CFG_MARKERS = (
            "GUARD_CF enabled PE files are not supported",
            "CantPackException: GUARD_CF",
            "consider using --force",
        )

        main_exe_abs = None
        if self.mode_var.get() == "-D":
            main_name = self.name_entry.get().strip()
            if main_name:
                main_exe_abs = os.path.abspath(os.path.join(dist_root, main_name, f"{main_name}.exe"))

        for path in uniq:
            if self.mode_var.get() == "-D" and self.upx_external_dlls_only_var.get():
                if main_exe_abs and os.path.abspath(path) == main_exe_abs:
                    self.add_to_console(f"[UPX] Skip main EXE (DLL/PYD only): {os.path.relpath(path, dist_root)}\n")
                    continue

            rel = os.path.relpath(path, dist_root)
            try:
                res = subprocess.run(base_cmd + [path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                out = (res.stdout or "").strip()

                if res.returncode == 0:
                    self.add_to_console(f"[UPX] Packed: {rel}\n"); continue
                if "Already packed" in out or "AlreadyPackedException" in out:
                    self.add_to_console(f"[UPX] Skipped (already packed): {rel}\n"); continue

                if any(m in out for m in CFG_MARKERS):
                    if not self.upx_force_var.get():
                        self.add_to_console(self._("upx_cfg_unsupported_skip").format(name=rel) + "\n")
                        self.add_colored(self._("upx_cfg_hint_enable_force") + "\n", tag='green')
                        continue

                self.add_to_console(f"[UPX] Failed ({res.returncode}): {rel}\n{out}\n")
            except Exception as e:
                self.add_to_console(f"[UPX] Error: {rel} -> {e}\n")

    # --------------------- UPX 检测与安装 ---------------------
    def ensure_upx_available(self):
        """确保 upx 可被外压调用；若缺失则尝试通过 pip 安装并加入 PATH"""
        def which_upx():
            exe = "upx.exe" if sys.platform.startswith('win') else "upx"
            return shutil.which("upx") or shutil.which(exe)

        if which_upx():
            self.upx_available = True
            return True

        self.add_to_console(self._("upx_not_found_try_install") + "\n")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "upx"],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
        except Exception:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "upx",
                                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"],
                               check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
            except Exception:
                self.upx_available = False
                self.add_to_console(self._("upx_unavailable_disable") + "\n")
                return False

        if which_upx():
            self.add_to_console(self._("upx_installed_ok") + "\n")
            self.upx_available = True
            return True

        # 兜底：扫描 site-packages 尝试加入 PATH
        try:
            search_dirs = []
            try:
                search_dirs.extend(site.getsitepackages())
            except Exception:
                pass
            try:
                search_dirs.append(site.getusersitepackages())
            except Exception:
                pass
            search_dirs = [d for d in search_dirs if d and os.path.isdir(d)]

            found_dir = None
            for base in search_dirs:
                for root_dir, _dirs, files in os.walk(base):
                    for f in files:
                        if f.lower() in ("upx", "upx.exe"):
                            found_dir = root_dir; break
                    if found_dir: break
                if found_dir: break

            if found_dir:
                os.environ["PATH"] = found_dir + os.pathsep + os.environ.get("PATH", "")
                if which_upx():
                    self.add_to_console(self._("upx_added_to_path").format(path=found_dir) + "\n")
                    self.upx_available = True
                    return True
        except Exception:
            pass

        self.add_to_console(self._("upx_unavailable_disable") + "\n")
        self.upx_available = False
        return False

    # --------------------- PyInstaller 可用性（冻结/源码两态） ---------------------
    def ensure_pyinstaller_available(self):
        """
        冻结（exe）下：探测外部 PyInstaller；无则报错。
        源码运行下：尝试 import PyInstaller；失败报错。
        """
        if is_frozen_app():
            mode, value = external_pyinstaller_probe()
            if mode is not None:
                return True
            messagebox.showerror(self._("ask_install_pyinstaller_title"), self._("msg_dependency_required"), parent=self.root)
            return False
        else:
            try:
                import PyInstaller  # noqa
                return True
            except Exception:
                messagebox.showerror(self._("ask_install_pyinstaller_title"), self._("msg_dependency_required"), parent=self.root)
                return False

    # --------------------- 命令构建与执行 ---------------------
    def build_command_list(self):
        if not self.ensure_pyinstaller_available():
            return None

        if self.upx_var.get() and (not self.upx_internal_var.get()):
            self.ensure_upx_available()

        if not self.script_path:
            messagebox.showerror(self._("title_error"), self._("error_select_script"), parent=self.root)
            return None

        command = ["pyinstaller"]
        command.append(self.mode_var.get())
        command.append(self.console_var.get())

        icon_path = self.icon_entry.get().strip()
        if icon_path:
            ipath = os.path.abspath(icon_path)
            if os.path.exists(ipath):
                command.extend(["-i", ipath])
            else:
                self.add_to_console(self._("warn_icon_missing").format(path=ipath) + "\n")

        ver_file = self.version_entry.get().strip()
        if ver_file:
            vpath = os.path.abspath(ver_file)
            if os.path.exists(vpath):
                command.extend(["--version-file", vpath])
            else:
                self.add_to_console(self._("warn_version_missing").format(path=vpath) + "\n")

        if self.name_entry.get():
            command.extend(["-n", self.name_entry.get()])

        distpath = self.distpath_entry.get().strip()
        if distpath:
            command.extend(["--distpath", distpath])

        # 关闭/启用内置 UPX
        if (not self.upx_var.get()) or (not self.upx_internal_var.get()):
            command.append("--noupx")
        else:
            for pat in self.upx_exclude_list:
                if pat.strip():
                    command.extend(["--upx-exclude", pat.strip()])

        for source, dest in self.resources_list:
            command.extend(["--add-data", f"{source}{os.pathsep}{dest}"])

        for mod in self.hidden_imports_list:
            command.extend(["--hidden-import", mod])
        for mod in self.exclude_modules_list:
            command.extend(["--exclude-module", mod])

        for p in self.hooks_dir_list:
            command.extend(["--additional-hooks-dir", p])
        for p in self.runtime_hooks_list:
            command.extend(["--runtime-hook", p])

        dbg_label = self.debug_level.get()
        dbg_value = self.debug_map.get(dbg_label)
        if dbg_value:
            command.extend(["--debug", dbg_value])

        if self.disable_windowed_tb.get():
            command.append("--disable-windowed-traceback")

        rt_tmp = self.runtime_tmpdir_entry.get().strip()
        if rt_tmp:
            command.extend(["--runtime-tmpdir", rt_tmp])

        if self.has_winsxs_opts:
            if self.win_no_prefer_redirects.get():
                command.append("--win-no-prefer-redirects")
            if self.win_private_assemblies.get():
                command.append("--win-private-assemblies")

        extra_args = self.extra_args_entry.get().strip()
        if extra_args:
            try:
                command.extend(shlex.split(extra_args))
            except Exception as e:
                self.add_to_console(self._("err_extra_args").format(err=str(e)) + "\n")

        if os.path.exists(self.script_path):
            command.append(self.script_path)
        else:
            self.add_to_console(self._("err_script_missing").format(path=self.script_path) + "\n")
            return None

        self.add_to_console(self._("log_full_cmd") + " " + ' '.join(command) + "\n")
        return command

    def _resolve_pyinstaller_invocation(self, command_list):
        """
        返回可执行的命令行（含解释器/可执行）：
        - frozen：优先 PATH 上的 pyinstaller；否则挑选外部 Python 执行 -m PyInstaller
        - 非 frozen：沿用原有逻辑，若找不到则回退到当前解释器 -m PyInstaller
        """
        if is_frozen_app():
            exe = shutil.which("pyinstaller")
            if exe:
                return [exe] + command_list[1:]
            for py_cmd in get_python_candidates():
                try:
                    res = subprocess.run(py_cmd + ["-m", "PyInstaller", "--version"],
                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                         text=True, timeout=6)
                    if res.returncode == 0:
                        return py_cmd + ["-m", "PyInstaller"] + command_list[1:]
                except Exception:
                    pass
            # 找不到就按原样返回（后续执行会失败，日志会提示）
            return command_list
        else:
            try:
                exe = command_list[0]
                if shutil.which(exe):
                    return command_list
            except Exception:
                pass
            return [sys.executable, "-m", "PyInstaller"] + command_list[1:]

    def execute_command(self, command_list):
        if self.mode_var.get() == "-F" and self.upx_external_dlls_only_var.get():
            self.add_colored(self._("log_only_libs_hint_singlefile") + "\n", tag='green')

        self.add_to_console("=" * 60 + "\n")
        self.add_to_console(self._("log_start_build") + "\n")

        try:
            creationflags = 0
            if sys.platform.startswith('win') and hasattr(subprocess, "CREATE_NO_WINDOW"):
                creationflags = subprocess.CREATE_NO_WINDOW

            command_list = self._resolve_pyinstaller_invocation(command_list)

            process = subprocess.Popen(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=creationflags
            )

            for line in iter(process.stdout.readline, ''):
                if self.is_closing:
                    break
                if line:
                    self.add_to_console(line)

            return_code = process.wait()

            if self.is_closing:
                return -1

            if return_code == 0:
                self.post_upx_compress()
                self.add_to_console("\n" + self._("log_build_success") + " ✓\n")
                distpath = self.distpath_entry.get()
                if distpath:
                    distpath = os.path.abspath(distpath)
                    self.add_to_console(self._("log_output_dir").format(path=distpath) + "\n")
                    try:
                        if sys.platform.startswith('win'):
                            os.startfile(distpath)
                        elif sys.platform.startswith('darwin'):
                            subprocess.Popen(['open', distpath])
                        else:
                            subprocess.Popen(['xdg-open', distpath])
                    except Exception as e:
                        self.add_to_console(self._("log_open_dir_failed").format(err=str(e)) + "\n")
            else:
                self.add_to_console("\n" + self._("log_build_failed").format(code=return_code) + "\n")

            return return_code

        except Exception as e:
            self.add_to_console("\n" + str(e) + "\n")
            return -1
        finally:
            self.enable_buttons(True)

    def start_build(self):
        if self.console_var.get() == "-w" and not self.disable_windowed_tb.get():
            self.add_to_console(self._("msg_tip_windowed") + "\n")

        command_list = self.build_command_list()
        if not command_list:
            return

        self.notebook.select(self.page_logs)
        self.enable_buttons(False)
        self.add_to_console(self._("log_building") + "\n")

        thread = threading.Thread(target=self.execute_command, args=(command_list,))
        thread.daemon = True
        thread.start()

    def clean_project(self):
        if not self.script_path or not os.path.exists(self.script_path):
            messagebox.showerror(self._("title_error"), self._("error_select_script"), parent=self.root)
            return

        self.add_to_console("\n" + self._("log_cleaning") + "\n")
        try:
            build_dir = "build"
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
                self.add_to_console(self._("log_deleted").format(name=build_dir) + "\n")

            script_name = os.path.splitext(os.path.basename(self.script_path))[0]
            spec_file = f"{script_name}.spec"
            if os.path.exists(spec_file):
                os.remove(spec_file)
                self.add_to_console(self._("log_deleted").format(name=spec_file) + "\n")

            cache_dir = "__pycache__"
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                self.add_to_console(self._("log_deleted").format(name=cache_dir) + "\n")

            self.add_to_console(self._("log_clean_done") + "\n")
        except Exception as e:
            self.add_to_console(self._("log_clean_error").format(err=str(e)) + "\n")

    def enable_buttons(self, state):
        """启用或禁用所有按钮（递归遍历）"""
        def traverse(widget):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Button):
                    child.config(state=tk.NORMAL if state else tk.DISABLED)
                traverse(child)
        try:
            traverse(self.root)
        except Exception:
            pass

    # --------------------- 统一关闭处理 ---------------------
    def on_close(self):
        if self.is_closing:
            return
        self.is_closing = True
        try:
            for t in getattr(self, "_tooltips", []):
                try:
                    t._unschedule()
                except Exception:
                    pass
        except Exception:
            pass
        try:
            self.root.unbind_all("<MouseWheel>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")
        except Exception:
            pass
        try:
            self.root.after(50, self.root.destroy)
        except Exception:
            try:
                self.root.destroy()
            except Exception:
                pass
        try:
            sys.exit(0)
        except SystemExit:
            raise
        except Exception:
            pass


# --------------------- 启动阶段：预检查 PyInstaller（兼容 exe/源码） ---------------------
def startup_check_pyinstaller(root, lang_code):
    _ = get_translator(lang_code)

    if is_frozen_app():
        # 仅检查“外部” PyInstaller
        mode, value = external_pyinstaller_probe()
        if mode is not None:
            return True

        # 未找到：询问是否安装（需要可用的外部 Python）
        title = _("ask_install_pyinstaller_title")
        msg = _("ask_install_pyinstaller")
        if not messagebox.askyesno(title, msg, parent=root):
            # 拒绝安装：提示并退出
            try:
                messagebox.showerror(title, _("msg_dependency_required"), parent=root)
            except Exception:
                pass
            try:
                root.destroy()
            except Exception:
                pass
            sys.exit(0)

        # 选择外部 Python
        py_cmd = None
        for cand in get_python_candidates():
            try:
                res = subprocess.run(cand + ["-V"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     text=True, timeout=5)
                if res.returncode == 0:
                    py_cmd = cand
                    break
            except Exception:
                pass

        if not py_cmd:
            # 没有可用的外部 Python
            try:
                if lang_code.lower().startswith("zh"):
                    messagebox.showerror(title, "未检测到可用的外部 Python 解释器，请先安装 Python 3.8+。", parent=root)
                else:
                    messagebox.showerror(title, "No external Python interpreter found. Please install Python 3.8+.", parent=root)
            except Exception:
                pass
            try:
                root.destroy()
            except Exception:
                pass
            sys.exit(0)

        ok = install_pyinstaller_waiting(root, lang_code, _, py_cmd_external=py_cmd)
        if ok:
            # 再次探测
            mode2, value2 = external_pyinstaller_probe()
            if mode2 is not None:
                return True

        # 安装失败
        try:
            messagebox.showerror(title, _("msg_install_failed"), parent=root)
        except Exception:
            pass
        try:
            root.destroy()
        except Exception:
            pass
        sys.exit(0)

    else:
        # 非 frozen：维持旧逻辑（当前解释器内检测/安装）
        try:
            import PyInstaller  # noqa
            return True
        except Exception:
            pass

        title = _("ask_install_pyinstaller_title")
        msg = _("ask_install_pyinstaller")
        if not messagebox.askyesno(title, msg, parent=root):
            try:
                messagebox.showerror(title, _("msg_dependency_required"), parent=root)
            except Exception:
                pass
            try:
                root.destroy()
            except Exception:
                pass
            sys.exit(0)

        ok = install_pyinstaller_waiting(root, lang_code, _)
        if ok:
            try:
                import PyInstaller  # noqa
                return True
            except Exception:
                pass

        try:
            messagebox.showerror(title, _("msg_install_failed"), parent=root)
        except Exception:
            pass
        try:
            root.destroy()
        except Exception:
            pass
        sys.exit(0)


if __name__ == "__main__":
    # 1) 启用高 DPI（Windows）
    apply_high_dpi_awareness()
    # 2) 创建 Tk，并同步 tk scaling（确保不同缩放下视觉一致）
    root = tk.Tk()
    try:
        root.tk.call('tk', 'scaling', root.winfo_fpixels('1i') / 72.0)
    except Exception:
        pass

    # 3) 启动即检查 PyInstaller（隐藏主窗，检查结束后再显示/或退出）
    try:
        root.withdraw()
    except Exception:
        pass
    _lang = detect_language_code()
    startup_check_pyinstaller(root, _lang)  # 拒绝或失败会在内部退出
    try:
        root.deiconify()
    except Exception:
        pass

    # 4) 进入主程序
    app = PyInstallerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
