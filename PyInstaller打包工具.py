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

# 保障能导入同目录下的 i18n 包
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 语言支持（外置）
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
    """简易气泡提示：鼠标悬停显示文本"""
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
            self.widget.after_cancel(self._after_id)
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
    # 提取数字段落，例如 "6.4.1" -> (6,4,1)
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
        # 尝试通过命令行检测
        cmds = [
            [sys.executable, "-m", "PyInstaller", "--version"],
            ["pyinstaller", "--version"],
        ]
        for cmd in cmds:
            try:
                out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=8)
                text = (out.stdout or "").strip()
                if text:
                    # 取第一行中的版本样式
                    first = text.splitlines()[0].strip()
                    vstr = first
                    break
            except Exception:
                pass
    return parse_version_tuple(vstr), vstr


class PyInstallerGUI:
    def __init__(self, root):
        # 翻译器
        lang_code = detect_language_code()
        self._ = get_translator(lang_code)
        self.lang_code = lang_code

        # 检测 PyInstaller 版本（用于 UI/参数兼容）
        self.pyi_version_tuple, self.pyi_version_str = detect_pyinstaller_version()
        self.has_winsxs_opts = bool(
            sys.platform.startswith('win') and self.pyi_version_tuple and self.pyi_version_tuple < (6, 0)
        )
        # 未检测到版本时，为安全起见不展示 WinSxS 选项
        if self.pyi_version_tuple is None:
            self.has_winsxs_opts = False

        self.root = root
        self.root.title(self._("app_title"))

        # 初始窗口大小限制在屏幕 90%，避免超屏；提供合理的最小尺寸
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

        # 存储用户数据
        self.script_path = ""
        self.icon_path = ""
        self.version_file_path = ""

        # 统一的资源清单（目录/文件）：[(abs_source, dest_rel)]
        self.resources_list = []

        self.hidden_imports_list = []
        self.exclude_modules_list = []
        self.hooks_dir_list = []
        self.runtime_hooks_list = []
        self.upx_exclude_list = []
        self.upx_available = None  # None/True/False

        # Windows 专属选项变量（即使不显示，也创建变量以避免引用报错）
        self.win_no_prefer_redirects = tk.BooleanVar(value=False)
        self.win_private_assemblies = tk.BooleanVar(value=False)

        # 构建各页面 UI
        self.build_page_basic()
        self.build_page_assets()
        self.build_page_advanced()
        self.build_page_logs()
        self.create_action_buttons()

        # 构建完成后刷新滚动容器
        self.page_assets_scroll.refresh()
        self.page_adv_scroll.refresh()
        # 切换分页时自动刷新
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self._refresh_scrollables())

    def _refresh_scrollables(self):
        if hasattr(self, "page_assets_scroll"):
            self.page_assets_scroll.refresh()
        if hasattr(self, "page_adv_scroll"):
            self.page_adv_scroll.refresh()

    # 小工具：若翻译缺失，则使用默认文本
    def tr(self, key, default_text):
        v = self._(key)
        return v if v != key else default_text

    # --------------------- 页面构建 ---------------------
    def build_page_basic(self):
        # 脚本设置
        file_frame = ttk.LabelFrame(self.page_basic, text=self._("group_script_settings"), padding=(10, 8))
        file_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text=self._("label_main_script")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.script_entry = ttk.Entry(file_frame)
        self.script_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(file_frame, text=self._("btn_browse"), command=self.select_script).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(file_frame, text=self._("label_output_name")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(file_frame)
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(file_frame, text=self._("label_output_dir")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.distpath_entry = ttk.Entry(file_frame)
        self.distpath_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(file_frame, text=self._("btn_browse"), command=self.select_distpath).grid(row=2, column=2, padx=5, pady=5)
        self.distpath_entry.insert(0, os.path.abspath("dist"))

        # 打包选项
        opt_frame = ttk.LabelFrame(self.page_basic, text=self._("group_build_options"), padding=(10, 8))
        opt_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(4):
            opt_frame.columnconfigure(i, weight=1 if i == 1 else 0)

        ttk.Label(opt_frame, text=self._("label_pack_mode")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.mode_var = tk.StringVar(value="-F")
        ttk.Radiobutton(opt_frame, text=self._("radio_onefile"), variable=self.mode_var, value="-F").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(opt_frame, text=self._("radio_onedir"), variable=self.mode_var, value="-D").grid(row=0, column=2, sticky="w", padx=5, pady=5)

        ttk.Label(opt_frame, text=self._("label_console")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.console_var = tk.StringVar(value="-c")
        ttk.Radiobutton(opt_frame, text=self._("radio_console"), variable=self.console_var, value="-c").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(opt_frame, text=self._("radio_windowed"), variable=self.console_var, value="-w").grid(row=1, column=2, sticky="w", padx=5, pady=5)

        ttk.Label(opt_frame, text=self._("label_app_icon")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.icon_entry = ttk.Entry(opt_frame)
        self.icon_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(opt_frame, text=self._("btn_browse"), command=self.select_icon).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(opt_frame, text=self._("label_version_file")).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.version_entry = ttk.Entry(opt_frame)
        self.version_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(opt_frame, text=self._("btn_browse"), command=self.select_version_file).grid(row=3, column=2, padx=5, pady=5)

        self.upx_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_frame, text=self._("check_use_upx"), variable=self.upx_var).grid(row=4, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        # UPX 压缩级别（后处理）
        upx_row = ttk.Frame(opt_frame)
        upx_row.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 5))
        upx_row.columnconfigure(1, weight=1)
        ttk.Label(upx_row, text=self.tr("label_upx_level", "UPX 压缩级别")).grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.upx_level_var = tk.DoubleVar(value=5)
        self.upx_level_scale = ttk.Scale(upx_row, from_=1, to=10, orient="horizontal",
                                         variable=self.upx_level_var, command=lambda v: self._on_upx_level_changed(v))
        self.upx_level_scale.grid(row=0, column=1, sticky="ew")
        self.upx_level_value = ttk.Label(upx_row, text="5")
        self.upx_level_value.grid(row=0, column=2, sticky="w", padx=(8, 0))
        Tooltip(self.upx_level_scale, self.tr(
            "tip_upx_level",
            "构建完成后对输出文件执行 UPX 压缩：1=最快，9=最小（10按9处理）。\n"
            "PyInstaller 本身不提供压缩级别参数，已自动禁用其内置 UPX 并改为后处理。"
        ))
        self.upx_var.trace_add("write", lambda *a: self._update_upx_controls_state())
        self._update_upx_controls_state()

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
        ttk.Button(self.res_frame, text=self.tr("btn_browse_file", "选择文件"), width=10, command=self.select_resource_file).grid(row=0, column=1, padx=2)
        ttk.Button(self.res_frame, text=self.tr("btn_browse_dir", "选择目录"), width=10, command=self.select_resource_dir).grid(row=0, column=2, padx=2)
        ttk.Button(self.res_frame, text=self._("btn_add"), width=8, command=self.add_resource).grid(row=0, column=3, padx=4)
        ttk.Button(self.res_frame, text=self._("btn_clear"), width=8, command=self.clear_resources).grid(row=0, column=4)

        hint_text = self.tr(
            "hint_resources_input",
            "输入路径后点击“添加”。支持：\n"
            "• 直接填源路径（文件或目录）。目录将以同名文件夹放到临时根目录；文件将直接放到临时根目录。\n"
            "• 若需自定义目标路径/名称，用“|”或“=>”分隔，例如：源路径|目标子路径 或 源路径=>目标子路径。"
        )
        ttk.Label(lf_res, text=hint_text, foreground="#666").grid(row=1, column=0, sticky="w", padx=0, pady=(0, 6))

        self.resource_listbox = tk.Listbox(lf_res, height=7, bg='white')
        self.resource_listbox.grid(row=2, column=0, sticky="ew", padx=0, pady=0)

        # 隐藏导入
        lf_hidden = ttk.LabelFrame(frame, text=self._("group_hidden_imports"), padding=(10, 8))
        lf_hidden.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        lf_hidden.columnconfigure(0, weight=1)
        self.hidden_frame = ttk.Frame(lf_hidden)
        self.hidden_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.hidden_frame.columnconfigure(0, weight=1)
        self.hidden_entry = ttk.Entry(self.hidden_frame)
        self.hidden_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(self.hidden_frame, text=self._("btn_add"), width=8, command=self.add_hidden_import).grid(row=0, column=1, padx=5)
        ttk.Button(self.hidden_frame, text=self._("btn_clear"), width=8, command=self.clear_hidden_imports).grid(row=0, column=2)
        self.hidden_listbox = tk.Listbox(lf_hidden, height=4, bg='white')
        self.hidden_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        # 排除模块
        lf_excl = ttk.LabelFrame(frame, text=self._("group_excludes"), padding=(10, 8))
        lf_excl.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        lf_excl.columnconfigure(0, weight=1)
        self.exclude_frame = ttk.Frame(lf_excl)
        self.exclude_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.exclude_frame.columnconfigure(0, weight=1)
        self.exclude_entry = ttk.Entry(self.exclude_frame)
        self.exclude_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(self.exclude_frame, text=self._("btn_add"), width=8, command=self.add_exclude_module).grid(row=0, column=1, padx=5)
        ttk.Button(self.exclude_frame, text=self._("btn_clear"), width=8, command=self.clear_exclude_modules).grid(row=0, column=2)
        self.exclude_listbox = tk.Listbox(lf_excl, height=4, bg='white')
        self.exclude_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        self.page_assets_scroll.refresh()

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
        ttk.Button(self.hooks_dir_frame, text=self._("btn_add"), width=8, command=self.add_hooks_dir).grid(row=0, column=1, padx=5)
        ttk.Button(self.hooks_dir_frame, text=self._("btn_clear"), width=8, command=self.clear_hooks_dir).grid(row=0, column=2)
        self.hooks_dir_listbox = tk.Listbox(lf_hooks, height=3, bg='white')
        self.hooks_dir_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        # 运行时 Hook
        lf_rth = ttk.LabelFrame(frame, text=self._("group_runtime_hooks"), padding=(10, 8))
        lf_rth.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        lf_rth.columnconfigure(0, weight=1)
        self.runtime_hook_frame = ttk.Frame(lf_rth)
        self.runtime_hook_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.runtime_hook_frame.columnconfigure(0, weight=1)
        self.runtime_hook_entry = ttk.Entry(self.runtime_hook_frame)
        self.runtime_hook_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(self.runtime_hook_frame, text=self._("btn_add"), width=8, command=self.add_runtime_hook).grid(row=0, column=1, padx=5)
        ttk.Button(self.runtime_hook_frame, text=self._("btn_clear"), width=8, command=self.clear_runtime_hooks).grid(row=0, column=2)
        self.runtime_hook_listbox = tk.Listbox(lf_rth, height=3, bg='white')
        self.runtime_hook_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        # UPX 排除
        lf_upx_ex = ttk.LabelFrame(frame, text=self._("group_upx_exclude"), padding=(10, 8))
        lf_upx_ex.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        lf_upx_ex.columnconfigure(0, weight=1)
        self.upx_excl_frame = ttk.Frame(lf_upx_ex)
        self.upx_excl_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        self.upx_excl_frame.columnconfigure(0, weight=1)
        self.upx_excl_entry = ttk.Entry(self.upx_excl_frame)
        self.upx_excl_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(self.upx_excl_frame, text=self._("btn_add"), width=8, command=self.add_upx_exclude).grid(row=0, column=1, padx=5)
        ttk.Button(self.upx_excl_frame, text=self._("btn_clear"), width=8, command=self.clear_upx_exclude).grid(row=0, column=2)
        self.upx_excl_listbox = tk.Listbox(lf_upx_ex, height=3, bg='white')
        self.upx_excl_listbox.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        # 其他开关（已移除 --noarchive；WinSxS 选项按版本显示）
        options_row = ttk.LabelFrame(frame, text=self._("group_other_switches"), padding=(10, 8))
        options_row.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.disable_windowed_tb = tk.BooleanVar(value=False)

        ttk.Checkbutton(options_row, text=self._("check_disable_windowed_tb"), variable=self.disable_windowed_tb).grid(row=0, column=0, sticky="w", padx=5, pady=3)

        if self.has_winsxs_opts:
            cb1 = ttk.Checkbutton(options_row, text=self._("check_win_no_prefer_redirects"), variable=self.win_no_prefer_redirects)
            cb1.grid(row=1, column=0, sticky="w", padx=5, pady=3)
            cb2 = ttk.Checkbutton(options_row, text=self._("check_win_private_assemblies"), variable=self.win_private_assemblies)
            cb2.grid(row=1, column=1, sticky="w", padx=5, pady=3)
            tip1 = self.tr("tip_win_no_prefer_redirects",
                           "仅 Windows（且 PyInstaller < 6）。禁用对 WinSxS 清单重定向的优先使用，改用常规 DLL 搜索顺序。")
            tip2 = self.tr("tip_win_private_assemblies",
                           "仅 Windows（且 PyInstaller < 6）。启用私有程序集，优先使用程序目录内的 DLL。")
            Tooltip(cb1, tip1)
            Tooltip(cb2, tip2)
        else:
            # 显示版本提示（可选）
            if sys.platform.startswith('win'):
                note = self.tr("note_winsxs_removed",
                               "提示：PyInstaller 6 起移除了 WinSxS 相关参数（--win-no-prefer-redirects / --win-private-assemblies）。")
                ttk.Label(options_row, text=note, foreground="#666").grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=(3, 0))

        # 运行时临时目录
        lf_rt = ttk.LabelFrame(frame, text=self._("label_runtime_tmpdir"), padding=(10, 8))
        lf_rt.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        lf_rt.columnconfigure(0, weight=1)
        self.runtime_tmpdir_entry = ttk.Entry(lf_rt)
        self.runtime_tmpdir_entry.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        # 额外参数
        lf_extra = ttk.LabelFrame(frame, text=self._("label_extra_args"), padding=(10, 8))
        lf_extra.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        lf_extra.columnconfigure(0, weight=1)
        self.extra_args_entry = ttk.Entry(lf_extra)
        self.extra_args_entry.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        self.page_adv_scroll.refresh()

    def build_page_logs(self):
        frame = self.page_logs
        self.console_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=10, bg='#23272A', fg='white')
        self.console_output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # 显示 PyInstaller 版本信息，便于诊断
        ver = self.pyi_version_str or "unknown"
        self.add_to_console(f"[INFO] PyInstaller version detected: {ver}\n")
        self.add_to_console(self._("log_ready") + "\n")
        self.add_to_console(self._("log_select_script") + "\n")

    def create_action_buttons(self):
        frame = ttk.Frame(self.main_frame)
        frame.grid(row=1, column=0, sticky="e", padx=5, pady=6)
        self.btn_build = ttk.Button(frame, text=self._("btn_build"), command=self.start_build, width=15)
        self.btn_build.grid(row=0, column=0, padx=5)
        self.btn_clean = ttk.Button(frame, text=self._("btn_clean"), command=self.clean_project, width=15)
        self.btn_clean.grid(row=0, column=1, padx=5)
        self.btn_exit = ttk.Button(frame, text=self._("btn_exit"), command=self.root.destroy, width=15)
        self.btn_exit.grid(row=0, column=2, padx=5)

    # --------------------- 事件处理：资源 ---------------------
    def _expand_path(self, p: str) -> str:
        return os.path.abspath(os.path.expanduser(os.path.expandvars(p.strip('"').strip("'"))))

    def _parse_resource_input(self, text: str):
        """返回 (abs_source, dest_rel) 或 None"""
        if not text:
            return None
        raw = text.strip()
        # 支持 “源|目标” 或 “源=>目标”，避免与 Windows 盘符冒号冲突
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
            dest = dest.strip().lstrip("\\/")  # 目标是包内相对路径
        else:
            # 默认规则：目录→同名文件夹；文件→临时根目录（保留文件名）
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
        p = filedialog.askopenfilename(title=self.tr("title_select_resource_file", "选择资源文件"))
        if p:
            self.resource_entry.delete(0, tk.END)
            self.resource_entry.insert(0, p)

    def select_resource_dir(self):
        p = filedialog.askdirectory(title=self.tr("title_select_resource_dir", "选择资源目录"))
        if p:
            self.resource_entry.delete(0, tk.END)
            self.resource_entry.insert(0, p)

    # --------------------- 事件处理：其他 ---------------------
    def select_script(self):
        script_path = filedialog.askopenfilename(
            filetypes=[(self._("filter_py"), "*.py"), (self._("filter_all"), "*.*")]
        )
        if script_path:
            self.script_path = os.path.abspath(script_path)
            self.script_entry.delete(0, tk.END)
            self.script_entry.insert(0, self.script_path)

            # 更换脚本后重置“输出名称”为脚本文件名（不含扩展名）
            file_name = os.path.splitext(os.path.basename(script_path))[0]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, file_name)

    def select_distpath(self):
        distpath = filedialog.askdirectory()
        if distpath:
            self.distpath_entry.delete(0, tk.END)
            self.distpath_entry.insert(0, os.path.abspath(distpath))

    def select_icon(self):
        icon_path = filedialog.askopenfilename(
            filetypes=[(self._("filter_ico"), "*.ico"), (self._("filter_all"), "*.*")]
        )
        if icon_path:
            self.icon_path = os.path.abspath(icon_path)
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, self.icon_path)

    def select_version_file(self):
        ver_path = filedialog.askopenfilename(
            title=self._("title_select_version_file"),
            filetypes=[(self._("filter_version"), "*.txt;*.ver;*.version"), (self._("filter_all"), "*.*")]
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

    def add_to_console(self, text):
        self.console_output.insert(tk.END, text)
        self.console_output.see(tk.END)
        self.console_output.update_idletasks()

    # --------------------- UPX 控件与后处理 ---------------------
    def _on_upx_level_changed(self, val):
        try:
            v = int(round(float(val)))
        except Exception:
            v = 5
        v = max(1, min(10, v))
        self.upx_level_value.config(text=str(v))

    def _update_upx_controls_state(self):
        state = "normal" if self.upx_var.get() else "disabled"
        try:
            self.upx_level_scale.state([state])
        except Exception:
            self.upx_level_scale.configure(state=state)
        try:
            self.upx_level_value.configure(state=state)
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
        """在构建成功后，按滑块级别运行 UPX 压缩"""
        if not self.upx_var.get() or self.upx_available is False:
            return

        # 级别 1~10，10 也按 9 处理
        try:
            level = int(round(float(self.upx_level_var.get())))
        except Exception:
            level = 5
        level = max(1, min(10, level))
        lvl_arg = f"-{min(level, 9)}"

        dist_root = self.distpath_entry.get().strip() or "dist"
        dist_root = os.path.abspath(dist_root)

        name = (self.name_entry.get().strip()
                or (os.path.splitext(os.path.basename(self.script_path))[0] if self.script_path else ""))

        candidates = []
        exts = {".exe", ".dll", ".pyd", ".so", ".dylib"}

        if self.mode_var.get() == "-F":
            exe_name = f"{name}.exe" if sys.platform.startswith('win') else name
            exe_path = os.path.join(dist_root, exe_name)
            if os.path.isfile(exe_path):
                candidates.append(exe_path)
        else:
            folder = os.path.join(dist_root, name)
            search_root = folder if os.path.isdir(folder) else dist_root
            for root, dirs, files in os.walk(search_root):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in exts:
                        path = os.path.join(root, f)
                        if not self._upx_is_excluded(path):
                            candidates.append(path)

        uniq = []
        seen = set()
        for p in candidates:
            if p not in seen and os.path.isfile(p):
                uniq.append(p)
                seen.add(p)

        if not uniq:
            self.add_to_console("[INFO] 没有可进行 UPX 压缩的目标文件。\n")
            return

        self.add_to_console(f"[INFO] 正在应用 UPX 压缩级别 {level}，目标文件数：{len(uniq)} ...\n")
        base_cmd = ["upx", "-q", "--no-progress", lvl_arg]

        for path in uniq:
            try:
                res = subprocess.run(base_cmd + [path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                out = res.stdout or ""
                rel = os.path.relpath(path, dist_root)
                if res.returncode == 0:
                    self.add_to_console(f"[UPX] Packed: {rel}\n")
                else:
                    if "Already packed" in out or "AlreadyPackedException" in out:
                        self.add_to_console(f"[UPX] Skipped (already packed): {rel}\n")
                    else:
                        self.add_to_console(f"[UPX] Failed ({res.returncode}): {rel}\n{out}\n")
            except Exception as e:
                self.add_to_console(f"[UPX] Error: {path} -> {e}\n")

    # --------------------- UPX 检测与安装 ---------------------
    def ensure_upx_available(self):
        """确保 upx 可被 PyInstaller 调用；若缺失则尝试通过 pip 安装并加入 PATH"""
        if not self.upx_var.get():
            self.upx_available = False
            return False

        def which_upx():
            exe = "upx.exe" if sys.platform.startswith('win') else "upx"
            return shutil.which("upx") or shutil.which(exe)

        if which_upx():
            self.upx_available = True
            return True

        self.add_to_console(self._("upx_not_found_try_install") + "\n")
        pip_cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "upx"]
        try:
            subprocess.run(pip_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
        except Exception:
            pip_cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "upx",
                       "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
            try:
                subprocess.run(pip_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
            except Exception:
                self.upx_available = False
                self.add_to_console(self._("upx_unavailable_disable") + "\n")
                return False

        if which_upx():
            self.add_to_console(self._("upx_installed_ok") + "\n")
            self.upx_available = True
            return True

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
                for root_dir, dirs, files in os.walk(base):
                    for f in files:
                        if f.lower() in ("upx", "upx.exe"):
                            found_dir = root_dir
                            break
                    if found_dir:
                        break
                if found_dir:
                    break

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

    # --------------------- 命令构建与执行 ---------------------
    def build_command_list(self):
        if self.upx_var.get():
            self.ensure_upx_available()

        if not self.script_path:
            messagebox.showerror(self._("title_error"), self._("error_select_script"))
            return None

        command = ["pyinstaller"]

        # 模式与控制台
        command.append(self.mode_var.get())
        command.append(self.console_var.get())

        # 图标
        icon_path = self.icon_entry.get().strip()
        if icon_path:
            ipath = os.path.abspath(icon_path)
            if os.path.exists(ipath):
                command.extend(["-i", ipath])
            else:
                self.add_to_console(self._("warn_icon_missing").format(path=ipath) + "\n")

        # 版本信息文件
        ver_file = self.version_entry.get().strip()
        if ver_file:
            vpath = os.path.abspath(ver_file)
            if os.path.exists(vpath):
                command.extend(["--version-file", vpath])
            else:
                self.add_to_console(self._("warn_version_missing").format(path=vpath) + "\n")

        # 输出名称
        if self.name_entry.get():
            command.extend(["-n", self.name_entry.get()])

        # 输出目录
        distpath = self.distpath_entry.get().strip()
        if distpath:
            command.extend(["--distpath", distpath])

        # 禁用 PyInstaller 内置 UPX，由我们在构建成功后自行压缩
        command.append("--noupx")

        # 资源（目录/文件）
        for source, dest in self.resources_list:
            command.extend(["--add-data", f"{source}{os.pathsep}{dest}"])

        # 隐藏导入 / 排除模块
        for mod in self.hidden_imports_list:
            command.extend(["--hidden-import", mod])
        for mod in self.exclude_modules_list:
            command.extend(["--exclude-module", mod])

        # Hooks 目录 / 运行时 Hook
        for p in self.hooks_dir_list:
            command.extend(["--additional-hooks-dir", p])
        for p in self.runtime_hooks_list:
            command.extend(["--runtime-hook", p])

        # 调试等级（支持 noarchive 作为 -d 参数值）
        dbg_label = self.debug_level.get()
        dbg_value = self.debug_map.get(dbg_label)
        if dbg_value:
            command.extend(["--debug", dbg_value])

        # 禁用 windowed traceback
        if self.disable_windowed_tb.get():
            command.append("--disable-windowed-traceback")

        # 运行时临时目录
        rt_tmp = self.runtime_tmpdir_entry.get().strip()
        if rt_tmp:
            command.extend(["--runtime-tmpdir", rt_tmp])

        # Windows 专有（仅在 < 6.0 时使用）
        if self.has_winsxs_opts:
            if self.win_no_prefer_redirects.get():
                command.append("--win-no-prefer-redirects")
            if self.win_private_assemblies.get():
                command.append("--win-private-assemblies")

        # 额外参数
        extra_args = self.extra_args_entry.get().strip()
        if extra_args:
            try:
                command.extend(shlex.split(extra_args))
            except Exception as e:
                self.add_to_console(self._("err_extra_args").format(err=str(e)) + "\n")

        # 脚本
        if os.path.exists(self.script_path):
            command.append(self.script_path)
        else:
            self.add_to_console(self._("err_script_missing").format(path=self.script_path) + "\n")
            return None

        self.add_to_console(self._("log_full_cmd") + " " + ' '.join(command) + "\n")
        return command

    def execute_command(self, command_list):
        self.add_to_console("=" * 60 + "\n")
        self.add_to_console(self._("log_start_build") + "\n")

        try:
            creationflags = 0
            if sys.platform.startswith('win') and hasattr(subprocess, "CREATE_NO_WINDOW"):
                creationflags = subprocess.CREATE_NO_WINDOW

            process = subprocess.Popen(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=creationflags
            )

            for line in iter(process.stdout.readline, ''):
                if line:
                    self.add_to_console(line)

            return_code = process.wait()

            if return_code == 0:
                # 构建成功后执行 UPX 后处理
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

        # 点击开始后自动切换到“日志”分页
        self.notebook.select(self.page_logs)

        self.enable_buttons(False)
        self.add_to_console(self._("log_building") + "\n")

        thread = threading.Thread(target=self.execute_command, args=(command_list,))
        thread.daemon = True
        thread.start()

    def clean_project(self):
        if not self.script_path or not os.path.exists(self.script_path):
            messagebox.showerror(self._("title_error"), self._("error_select_script"))
            return

        self.add_to_console("\n" + self._("log_cleaning") + "\n")
        try:
            # 删除build目录
            build_dir = "build"
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
                self.add_to_console(self._("log_deleted").format(name=build_dir) + "\n")

            # 删除spec文件
            script_name = os.path.splitext(os.path.basename(self.script_path))[0]
            spec_file = f"{script_name}.spec"
            if os.path.exists(spec_file):
                os.remove(spec_file)
                self.add_to_console(self._("log_deleted").format(name=spec_file) + "\n")

            # 删除生成的__pycache__
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
        traverse(self.root)


if __name__ == "__main__":
    apply_high_dpi_awareness()
    root = tk.Tk()
    app = PyInstallerGUI(root)
    root.mainloop()