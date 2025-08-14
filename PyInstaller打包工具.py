import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# 尝试导入tkinterdnd2库用于拖放功能
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    dnd_available = True
except ImportError:
    dnd_available = False
import subprocess
import threading
import os
import shlex
import sys
import shutil
import json
import locale

class PyInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyInstaller 打包工具")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 初始化变量
        self.script_path = ""
        self.current_language = "zh"  # 默认中文
        self.additional_libraries = []
        self.add_data_list = []
        self.current_python_path = sys.executable  # 保存当前Python路径
        
        # 检测系统语言
        self.detect_language()
        
        # 加载翻译
        self.translations = self.load_translations()
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建带滚动条的主框架
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        # 配置滚动区域
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        
        # 绑定鼠标滚轮事件
        self.main_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        # 布局Canvas和滚动条
        self.main_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.main_scrollbar.pack(side="right", fill="y")
        
        # 创建内容框架
        self.content_frame = ttk.Frame(self.scrollable_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建各个区域的框架
        self.file_frame = ttk.Frame(self.content_frame)
        self.file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.options_frame = ttk.Frame(self.content_frame)
        self.options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.console_frame = ttk.Frame(self.content_frame)
        self.console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.advanced_frame = ttk.Frame(self.content_frame)
        self.advanced_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.buttons_frame = ttk.Frame(self.content_frame)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # 设置框架引用，保持与原有代码的兼容性
        self.left_main_frame = self.file_frame
        self.right_main_frame = self.console_frame
        self.bottom_main_frame = self.advanced_frame
        
        # 创建各个区域
        self.create_file_section()
        self.create_options_section()
        self.create_console_output()
        self.create_advanced_section()
        self.create_action_buttons()
        
        
    def detect_language(self):
        """检测系统语言"""
        try:
            # 获取系统语言
            system_locale = locale.getlocale()[0]
            if system_locale and system_locale.startswith('zh'):
                return 'zh'
            else:
                return 'en'
        except:
            return 'en'
    
    def load_translations(self):
        """加载翻译文本"""
        return {
            'zh': {
                'window_title': 'PyInstaller 打包工具',
                'menu_language': '语言',
                'lang_chinese': '中文',
                'lang_english': 'English',
                'menu_help': '帮助',
                'menu_help_usage': '使用说明',
                'menu_help_about': '关于',
                'file_section': '脚本设置',
                'python_path': 'Python路径:',
                'browse': '浏览...',
                'main_script': '主脚本文件:',
                'output_name': '输出名称:',
                'output_dir': '输出目录:',
                'options_section': '打包选项',
                'pack_mode': '打包模式:',
                'mode_onefile': '单文件模式 (-F)',
                'mode_dir': '目录模式 (-D)',
                'console': '控制台:',
                'console_show': '显示控制台 (-c)',
                'console_hide': '无控制台 (-w)',
                'app_icon': '应用图标:',
                'upx_compress': '使用UPX压缩 (推荐)',
                'upx_dir': 'UPX目录:',
                'advanced_section': '高级选项',
                'add_resources': '附加资源文件 (源路径:目标路径)',
                'add': '添加',
                'clear': '清除',
                'view_installed': '查看已安装库',
                'extra_args': '额外命令行参数:',
                'console_output': '打包日志',
                'start_pack': '开始打包',
                'clean_project': '清理项目',
                'exit': '退出',
                'about_title': '关于',
                'help_title': '使用说明',
                'error': '错误',
                'warning': '警告',
                'info': '信息',
                'success': '成功',
                'failed': '失败'
            },
            'en': {
                'window_title': 'PyInstaller Packager',
                'menu_language': 'Language',
                'lang_chinese': '中文',
                'lang_english': 'English',
                'menu_help': 'Help',
                'menu_help_usage': 'Usage Instructions',
                'menu_help_about': 'About',
                'file_section': 'Script Settings',
                'python_path': 'Python Path:',
                'browse': 'Browse...',
                'main_script': 'Main Script:',
                'output_name': 'Output Name:',
                'output_dir': 'Output Directory:',
                'options_section': 'Packaging Options',
                'pack_mode': 'Packaging Mode:',
                'mode_onefile': 'Single File Mode (-F)',
                'mode_dir': 'Directory Mode (-D)',
                'console': 'Console:',
                'console_show': 'Show Console (-c)',
                'console_hide': 'No Console (-w)',
                'app_icon': 'Application Icon:',
                'upx_compress': 'Use UPX Compression (Recommended)',
                'upx_dir': 'UPX Directory:',
                'advanced_section': 'Advanced Options',
                'add_resources': 'Additional Resource Files (Source:Target)',
                'add': 'Add',
                'clear': 'Clear',
                'view_installed': 'View Installed Libraries',
                'extra_args': 'Extra Command Line Arguments:',
                'console_output': 'Packaging Log',
                'start_pack': 'Start Packaging',
                'clean_project': 'Clean Project',
                'exit': 'Exit',
                'about_title': 'About',
                'help_title': 'Usage Instructions',
                'error': 'Error',
                'warning': 'Warning',
                'info': 'Information',
                'success': 'Success',
                'failed': 'Failed'
            }
        }
    
    def switch_language(self, lang):
        """切换语言"""
        self.current_language = lang
        # 重新创建界面以应用新语言
        self.recreate_ui()
    
    def recreate_ui(self):
        """重新创建界面"""
        # 清除现有界面
        for widget in self.left_main_frame.winfo_children():
            widget.destroy()
        for widget in self.right_main_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_main_frame.winfo_children():
            widget.destroy()
        
        # 重新创建界面
        self.create_file_section()
        self.create_options_section()
        self.create_console_output()
        self.create_advanced_section()
        self.create_action_buttons()
        
        # 更新窗口标题
        self.root.title(self.translations[self.current_language]["window_title"])
        
        # 更新菜单
        self.create_menu()
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 语言菜单
        lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translations[self.current_language]["menu_language"], menu=lang_menu)
        lang_menu.add_command(label=self.translations[self.current_language]["lang_chinese"], command=lambda: self.switch_language("zh"))
        lang_menu.add_command(label=self.translations[self.current_language]["lang_english"], command=lambda: self.switch_language("en"))
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translations[self.current_language]["menu_help"], menu=help_menu)
        help_menu.add_command(label=self.translations[self.current_language]["menu_help_usage"], command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label=self.translations[self.current_language]["menu_help_about"], command=self.show_about)
        
    def show_about(self):
        """显示关于对话框"""
        about_text = """
PyInstaller 打包工具
版本: 1.2.1

一个基于PyInstaller的图形界面打包工具，
可帮助您轻松地将Python脚本打包为可执行文件。

功能特性:
- 图形化界面操作
- 支持单文件/目录打包
- 可自定义图标和输出目录
- 支持附加资源文件
- 实时日志输出
- 一键清理功能
- UPX压缩支持
- 可指定Python解释器路径

系统要求:
- Python 3.6+
- PyInstaller 4.0+
- UPX (可选，用于压缩)

注意事项:
- 请确保已安装PyInstaller: pip install pyinstaller
- 某些杀毒软件可能会误报生成的exe文件
- 打包过程可能需要一些时间，请耐心等待
        """
        messagebox.showinfo("关于", about_text)
    
    def save_config(self):
        """保存当前配置到文件 - 已移除此功能"""
        pass
    
    def load_config(self):
        """从文件加载配置 - 已移除此功能"""
        pass
        
    def show_help(self):
        """显示帮助信息"""
        help_text = """
使用说明:
1. 选择Python解释器路径(可选)
   - 如果系统PATH中没有python或需要使用特定版本，可以指定Python解释器路径
2. 选择要打包的Python脚本文件
3. 根据需要设置打包选项
   - 单文件打包: 将所有内容打包到一个exe文件中
   - 目录模式: 将程序打包为目录形式
   - 显示控制台: 适用于命令行程序
   - 无控制台: 适用于GUI程序，避免显示命令行窗口
   - UPX压缩: 减小可执行文件大小(推荐)
4. 设置高级选项(可选)
   - 输出名称: 指定生成的exe文件名称
   - 输出目录: 指定生成文件的存放位置
   - 应用图标: 为exe文件设置自定义图标
   - UPX目录: 如果UPX不在系统PATH中，可以指定UPX工具的目录
   - 附加资源: 添加程序运行所需的额外文件(格式: 源路径:目标路径)
   - 额外参数: 添加其他PyInstaller支持的命令行参数
5. 点击"开始打包"按钮执行打包过程
6. 打包完成后可点击"清理项目"删除临时文件

注意事项:
- 确保已安装PyInstaller: pip install pyinstaller
- 某些杀毒软件可能会误报生成的exe文件
- 打包过程可能需要一些时间，请耐心等待
- 如果需要UPX压缩功能请单独安装UPX工具
- 生成的exe文件可能会被杀毒软件误报，请在需要时添加信任
        """
        messagebox.showinfo("使用说明", help_text)
        
    def create_file_section(self):
        """创建文件选择区域"""
        frame = ttk.LabelFrame(self.left_main_frame, text=self.translations[self.current_language]["file_section"], padding=(10, 5))
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Python解释器路径
        ttk.Label(frame, text=self.translations[self.current_language]["python_path"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.python_path_entry = ttk.Entry(frame, width=50)
        self.python_path_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text=self.translations[self.current_language]["browse"], command=self.select_python_path).grid(row=0, column=2, padx=5, pady=5)
        
        # 脚本文件选择
        ttk.Label(frame, text=self.translations[self.current_language]["main_script"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.script_entry = ttk.Entry(frame, width=50)
        self.script_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text=self.translations[self.current_language]["browse"], command=self.select_script).grid(row=1, column=2, padx=5, pady=5)
        
        # 为脚本路径输入框添加拖放支持
        if dnd_available:
            try:
                self.script_entry.drop_target_register(DND_FILES)
                self.script_entry.dnd_bind('<<Drop>>', self.on_script_drop)
            except Exception as e:
                # 如果拖放功能无法启用，忽略错误
                pass
        
        # 输出名称
        ttk.Label(frame, text=self.translations[self.current_language]["output_name"]).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(frame, width=50)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # 输出路径
        ttk.Label(frame, text=self.translations[self.current_language]["output_dir"]).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.distpath_entry = ttk.Entry(frame, width=50)
        self.distpath_entry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(frame, text=self.translations[self.current_language]["browse"], command=self.select_distpath).grid(row=3, column=2, padx=5, pady=5)
        
        # 设置默认输出路径为当前目录/dist
        self.distpath_entry.insert(0, os.path.abspath("dist"))
    
    def create_options_section(self):
        """创建主要选项区域"""
        frame = ttk.LabelFrame(self.left_main_frame, text=self.translations[self.current_language]["options_section"], padding=(10, 5))
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 打包模式
        ttk.Label(frame, text=self.translations[self.current_language]["pack_mode"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.mode_var = tk.StringVar()
        self.mode_var.set("-F")  # 默认单文件模式
        ttk.Radiobutton(frame, text=self.translations[self.current_language]["mode_onefile"], variable=self.mode_var, value="-F").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(frame, text=self.translations[self.current_language]["mode_dir"], variable=self.mode_var, value="-D").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        
        # 控制台选项
        ttk.Label(frame, text=self.translations[self.current_language]["console"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.console_var = tk.StringVar()
        self.console_var.set("-c")  # 默认显示控制台
        ttk.Radiobutton(frame, text=self.translations[self.current_language]["console_show"], variable=self.console_var, value="-c").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(frame, text=self.translations[self.current_language]["console_hide"], variable=self.console_var, value="-w").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        
        # 图标设置
        ttk.Label(frame, text=self.translations[self.current_language]["app_icon"]).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.icon_entry = ttk.Entry(frame, width=50)
        self.icon_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frame, text=self.translations[self.current_language]["browse"], command=self.select_icon).grid(row=2, column=2, padx=5, pady=5)
        
        # UPX压缩
        self.upx_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text=self.translations[self.current_language]["upx_compress"], variable=self.upx_var).grid(
            row=3, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        
        # UPX目录
        ttk.Label(frame, text=self.translations[self.current_language]["upx_dir"]).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.upx_dir_entry = ttk.Entry(frame, width=50)
        self.upx_dir_entry.grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(frame, text=self.translations[self.current_language]["browse"], command=self.select_upx_dir).grid(row=4, column=2, padx=5, pady=5)
    
    def create_advanced_section(self):
        """创建高级选项区域"""
        # 创建标签框架
        frame = ttk.LabelFrame(self.bottom_main_frame, text=self.translations[self.current_language]["advanced_section"], padding=(10, 5))
        frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # 附加资源文件
        ttk.Label(frame, text=self.translations[self.current_language]["add_resources"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        resource_frame = ttk.Frame(frame)
        resource_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        resource_frame.columnconfigure(1, weight=1)
        
        self.resource_source_entry = ttk.Entry(resource_frame, width=30)
        self.resource_source_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Label(resource_frame, text=":").grid(row=0, column=1, padx=2, pady=5)
        
        self.resource_target_entry = ttk.Entry(resource_frame, width=20)
        self.resource_target_entry.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        
        button_frame = ttk.Frame(resource_frame)
        button_frame.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(button_frame, text=self.translations[self.current_language]["add"], command=self.add_resource).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text=self.translations[self.current_language]["clear"], command=self.clear_resources).pack(side=tk.LEFT, padx=2)
        
        # 显示已添加的资源
        self.resource_listbox = tk.Listbox(frame, height=4)
        self.resource_listbox.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # 额外Python库
        ttk.Label(frame, text="额外Python库:").grid(row=3, column=0, sticky="w", padx=5, pady=(10, 5))
        
        library_frame = ttk.Frame(frame)
        library_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        library_frame.columnconfigure(1, weight=1)
        
        self.library_entry = ttk.Entry(library_frame, width=30)
        self.library_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        library_button_frame = ttk.Frame(library_frame)
        library_button_frame.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(library_button_frame, text=self.translations[self.current_language]["add"], command=self.add_library).pack(side=tk.LEFT, padx=2)
        ttk.Button(library_button_frame, text="自动检测", command=self.auto_detect_libraries).pack(side=tk.LEFT, padx=2)
        ttk.Button(library_button_frame, text=self.translations[self.current_language]["clear"], command=self.clear_libraries).pack(side=tk.LEFT, padx=2)
        ttk.Button(library_button_frame, text=self.translations[self.current_language]["view_installed"], command=self.show_installed_libraries).pack(side=tk.LEFT, padx=2)
        
        # 显示已添加的库
        self.library_listbox = tk.Listbox(frame, height=4)
        self.library_listbox.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # 额外命令行参数
        ttk.Label(frame, text=self.translations[self.current_language]["extra_args"]).grid(row=6, column=0, sticky="w", padx=5, pady=(10, 5))
        self.extra_args_entry = ttk.Entry(frame, width=50)
        self.extra_args_entry.grid(row=7, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
    
    def create_console_output(self):
        """创建控制台输出区域"""
        frame = ttk.LabelFrame(self.right_main_frame, text=self.translations[self.current_language]["console_output"], padding=(10, 5))
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.console_output = scrolledtext.ScrolledText(
            frame, wrap=tk.WORD, bg='#23272A', fg='white')
        self.console_output.grid(row=0, column=0, padx=5, pady=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0, pady=(5, 0))
        self.progress_bar.grid_remove()  # 默认隐藏进度条
        
        # 添加开始消息
        self.add_to_console("PyInstaller GUI打包工具已就绪\n")
        self.add_to_console("请选择Python脚本并配置打包选项\n")
    
    def create_action_buttons(self):
        """创建操作按钮区域"""
        frame = ttk.Frame(self.left_main_frame)
        frame.pack(fill=tk.X, padx=5, pady=10)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(side=tk.RIGHT)
        
        # 配置突出的按钮样式
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078d4", 
                       font=("Arial", 10, "bold"))
        
        # 使用突出样式创建开始打包按钮
        ttk.Button(button_frame, text=self.translations[self.current_language]["start_pack"], 
                  command=self.start_build, width=15, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.translations[self.current_language]["clean_project"], 
                  command=self.clean_project, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.translations[self.current_language]["exit"], 
                  command=self.root.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
    def enable_buttons(self, enabled=True):
        """启用或禁用操作按钮"""
        state = tk.NORMAL if enabled else tk.DISABLED
        for widget in self.left_main_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button) and child.cget('text') in ['开始打包', '清理项目']:
                        child.config(state=state)
    
    def select_script(self):
        """选择要打包的Python脚本"""
        script_path = filedialog.askopenfilename(
            filetypes=[("Python脚本", "*.py"), ("所有文件", "*.*")],
            initialdir=os.path.expanduser("~")
        )
        if script_path:
            self.set_script_path(script_path)
    
    def on_script_drop(self, event):
        """处理脚本文件拖放事件"""
        # 获取拖放的文件路径
        files = self.root.tk.splitlist(event.data)
        if files:
            # 取第一个文件
            file_path = files[0]
            # 检查是否为Python文件
            if file_path.lower().endswith('.py'):
                self.set_script_path(file_path)
            else:
                messagebox.showwarning(self.translations[self.current_language]["warning"], "请选择Python脚本文件(.py)")
    
    def set_script_path(self, script_path):
        """设置脚本路径并更新相关字段"""
        self.script_path = os.path.abspath(script_path)
        self.script_entry.delete(0, tk.END)
        self.script_entry.insert(0, self.script_path)
        
        # 自动设置默认输出名称
        if not self.name_entry.get():
            file_name = os.path.splitext(os.path.basename(script_path))[0]
            self.name_entry.insert(0, file_name)
    
    def select_python_path(self):
        """选择Python解释器路径"""
        file_path = filedialog.askopenfilename(
            title="选择Python解释器",
            filetypes=[("Executable files", "python.exe"), ("All files", "*")],
            initialdir=os.path.expanduser("~")
        )
        if file_path:
            self.python_path_entry.delete(0, tk.END)
            self.python_path_entry.insert(0, file_path)
    
    def select_distpath(self):
        """选择输出目录"""
        dir_path = filedialog.askdirectory(
            title="选择输出目录",
            initialdir=os.path.expanduser("~")
        )
        if dir_path:
            self.distpath_entry.delete(0, tk.END)
            self.distpath_entry.insert(0, dir_path)
    
    def select_icon(self):
        """选择应用图标"""
        file_path = filedialog.askopenfilename(
            title="选择图标文件",
            filetypes=[("Icon files", "*.ico"), ("All files", "*")],
            initialdir=os.path.expanduser("~")
        )
        if file_path:
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, file_path)
    
    def select_upx_dir(self):
        """选择UPX目录"""
        dir_path = filedialog.askdirectory(
            title="选择UPX目录",
            initialdir=os.path.expanduser("~")
        )
        if dir_path:
            self.upx_dir_entry.delete(0, tk.END)
            self.upx_dir_entry.insert(0, dir_path)
    
    def add_resource(self):
        """添加资源文件"""
        source = self.resource_source_entry.get().strip()
        target = self.resource_target_entry.get().strip()
        
        if source and target:
            resource = f"{source}:{target}"
            self.resource_listbox.insert(tk.END, resource)
            self.resource_source_entry.delete(0, tk.END)
            self.resource_target_entry.delete(0, tk.END)
    
    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def clear_resources(self):
        """清除所有资源文件"""
        self.resource_listbox.delete(0, tk.END)
    
    def add_library(self):
        """添加Python库"""
        library = self.library_entry.get().strip()
        if library:
            # 检查库是否已添加
            existing_libraries = list(self.library_listbox.get(0, tk.END))
            if library not in existing_libraries:
                self.library_listbox.insert(tk.END, library)
                self.additional_libraries.append(library)  # 添加到存储列表中
            self.library_entry.delete(0, tk.END)
    
    def auto_detect_libraries(self):
        """自动检测脚本中导入的库"""
        if not self.script_path or not os.path.exists(self.script_path):
            messagebox.showwarning(self.translations[self.current_language]["warning"], "请先选择主脚本文件")
            return
        
        try:
            # 读取脚本内容
            with open(self.script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单的库检测（实际项目中可能需要更复杂的解析）
            import re
            import_statements = re.findall(r'^\s*(?:import|from)\s+([\w\.]+)', content, re.MULTILINE)
            
            # 过滤标准库和已添加的库
            existing_libraries = list(self.library_listbox.get(0, tk.END))
            standard_libs = {'os', 'sys', 'json', 're', 'time', 'datetime', 'math', 'random', 'collections', 'itertools', 'functools'}
            
            for lib in import_statements:
                # 只取顶层模块名
                top_level = lib.split('.')[0]
                if top_level not in standard_libs and top_level not in existing_libraries:
                    self.library_listbox.insert(tk.END, top_level)
                    self.additional_libraries.append(top_level)  # 添加到存储列表中
            
            messagebox.showinfo(self.translations[self.current_language]["info"], f"已检测到{len(import_statements)}个导入语句")
        except Exception as e:
            messagebox.showerror(self.translations[self.current_language]["error"], f"检测库时出错: {str(e)}")
    
    def clear_libraries(self):
        """清除所有额外的Python库"""
        self.library_listbox.delete(0, tk.END)
        self.additional_libraries.clear()  # 清空存储列表
    
    def show_installed_libraries(self):
        """显示当前Python环境中已安装的库"""
        try:
            # 获取当前Python路径
            python_path = self.python_path_entry.get().strip()
            if not python_path:
                python_path = sys.executable
            
            # 运行pip list命令获取已安装的库
            result = subprocess.run([python_path, "-m", "pip", "list"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # 创建新窗口显示库列表
                lib_window = tk.Toplevel(self.root)
                lib_window.title("已安装的Python库")
                lib_window.geometry("600x400")
                lib_window.minsize(400, 300)
                
                # 创建文本框和滚动条
                text_frame = ttk.Frame(lib_window)
                text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                text_widget = tk.Text(text_frame, wrap=tk.NONE)
                vsb = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
                hsb = ttk.Scrollbar(text_frame, orient="horizontal", command=text_widget.xview)
                text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
                
                text_widget.grid(row=0, column=0, sticky="nsew")
                vsb.grid(row=0, column=1, sticky="ns")
                hsb.grid(row=1, column=0, sticky="ew")
                text_frame.columnconfigure(0, weight=1)
                text_frame.rowconfigure(0, weight=1)
                
                # 插入库列表
                text_widget.insert(tk.END, result.stdout)
                text_widget.config(state=tk.DISABLED)  # 设置为只读
                
                # 添加关闭按钮
                button_frame = ttk.Frame(lib_window)
                button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
                
                ttk.Button(button_frame, text="关闭", command=lib_window.destroy).pack(side=tk.RIGHT)
            else:
                messagebox.showerror(self.translations[self.current_language]["error"], 
                                   f"获取库列表失败: {result.stderr}")
        except subprocess.TimeoutExpired:
            messagebox.showerror(self.translations[self.current_language]["error"], 
                               "获取库列表超时")
        except Exception as e:
            messagebox.showerror(self.translations[self.current_language]["error"], 
                               f"获取库列表时出错: {str(e)}")
    
    def add_data_item(self):
        """添加附加资源文件"""
        data_item = self.add_data_entry.get()
        if data_item and ':' in data_item:
            source, dest = data_item.split(':', 1)
            if source and dest:
                # 规范化路径并确保绝对路径
                source = os.path.abspath(source) if not os.path.isabs(source) else source
                self.add_data_list.append((source, dest))
                self.data_listbox.insert(tk.END, f"{source} → {dest}")
                self.add_data_entry.delete(0, tk.END)
        elif data_item:  # 用户可能忘记添加冒号
            messagebox.showwarning("格式错误", "请使用正确的格式: 源路径:目标路径")
            
    def clean_project(self):
        """清理项目生成的文件"""
        try:
            cleaned_count = 0
            
            # 清理build目录
            build_dir = os.path.join(os.getcwd(), "build")
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
                self.add_to_console(f"已清理build目录: {build_dir}\n")
                cleaned_count += 1
            
            # 清理dist目录
            dist_dir = self.distpath_entry.get().strip()
            if dist_dir and os.path.exists(dist_dir):
                shutil.rmtree(dist_dir)
                self.add_to_console(f"已清理dist目录: {dist_dir}\n")
                cleaned_count += 1
            elif not dist_dir:
                # 如果没有指定dist目录，清理默认的dist目录
                default_dist = os.path.join(os.getcwd(), "dist")
                if os.path.exists(default_dist):
                    shutil.rmtree(default_dist)
                    self.add_to_console(f"已清理默认dist目录: {default_dist}\n")
                    cleaned_count += 1
            
            # 清理spec文件
            if self.script_path and os.path.exists(self.script_path):
                script_name = os.path.splitext(os.path.basename(self.script_path))[0]
                spec_file = os.path.join(os.getcwd(), f"{script_name}.spec")
                if os.path.exists(spec_file):
                    os.remove(spec_file)
                    self.add_to_console(f"已清理spec文件: {spec_file}\n")
                    cleaned_count += 1
            
            # 清理__pycache__目录
            for root, dirs, files in os.walk("."):
                if "__pycache__" in dirs:
                    pycache_path = os.path.join(root, "__pycache__")
                    shutil.rmtree(pycache_path)
                    self.add_to_console(f"已清理__pycache__目录: {pycache_path}\n")
                    cleaned_count += 1
            
            self.add_to_console(f"清理完成，共清理了 {cleaned_count} 项\n")
            
        except Exception as e:
            self.add_to_console(f"清理过程中发生错误: {str(e)}\n")
    
    def clear_data_items(self):
        """清除所有附加资源文件"""
        self.add_data_list = []
        self.data_listbox.delete(0, tk.END)
    
    def add_to_console(self, text):
        """向控制台输出区域添加文本"""
        self.console_output.insert(tk.END, text)
        self.console_output.see(tk.END)
        self.console_output.update_idletasks()
    
    def build_command_list(self):
        """构建PyInstaller命令列表"""
        if not self.script_path:
            messagebox.showerror("错误", "请先选择要打包的Python脚本文件")
            return None
        
        # 基本命令 (注意：Python路径和模块参数在execute_command方法中添加)
        command = ["PyInstaller"]
        
        # 打包选项
        if self.mode_var.get() == "-F":
            command.append("--onefile")
        if self.console_var.get() == "-w":
            command.append("--noconsole")
        if self.upx_var.get():
            upx_dir = self.upx_dir_entry.get().strip()
            if upx_dir:
                command.extend(["--upx-dir", upx_dir])
        
        # 高级选项
        if self.name_entry.get().strip():
            command.extend(["--name", self.name_entry.get().strip()])
        if self.distpath_entry.get().strip():
            command.extend(["--distpath", self.distpath_entry.get().strip()])
        if self.icon_entry.get().strip():
            command.extend(["--icon", self.icon_entry.get().strip()])
        
        # 附加资源文件
        for source, dest in self.add_data_list:
            # 处理路径中的空格
            source = f'"{source}"' if ' ' in source else source
            command.extend(["--add-data", f"{source}{os.pathsep}{dest}"])
        
        # 额外Python库
        for library in self.additional_libraries:
            command.extend(["--hidden-import", library])
        
        # 额外参数
        extra_args = self.extra_args_entry.get().strip()
        if extra_args:
            # 分割参数时考虑引号
            import shlex
            try:
                command.extend(shlex.split(extra_args))
            except ValueError as e:
                messagebox.showerror("参数错误", f"额外参数格式错误: {str(e)}")
                return None
        
        # 脚本路径
        command.append(self.script_path)
        
        return command
    
    def execute_command(self, command_list):
        """执行打包命令（使用安全的命令列表方式）"""
        # 先安装依赖库
        self.install_dependencies()
        
        self.add_to_console("=" * 60 + "\n")
        self.add_to_console("开始打包过程...\n")
        
        # 禁用操作按钮
        self.enable_buttons(False)
        
        # 显示进度条
        self.progress_bar.grid()
        self.progress_var.set(0)
        
        try:
            # 检查PyInstaller是否已安装
            python_path = self.python_path_entry.get().strip()
            if not python_path:
                python_path = sys.executable  # 使用当前Python解释器
            
            try:
                subprocess.run([python_path, "-m", "PyInstaller", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.add_to_console("错误: 未找到Python解释器或PyInstaller，请确保路径正确且已安装PyInstaller。\n")
                self.add_to_console("请运行 'pip install pyinstaller' 安装PyInstaller。\n")
                return -1
            
            # 使用列表传递命令参数，避免shell=True
            # 在命令列表前添加Python解释器路径
            full_command = [python_path, "-m"] + command_list
            process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 实时读取输出并显示
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.add_to_console(line)
                    # 简单的进度模拟（实际进度监控需要更复杂的实现）
                    current_progress = self.progress_var.get()
                    if current_progress < 90:  # 限制在90%以内，剩余10%留给最终处理
                        self.progress_var.set(current_progress + 0.5)
                self.root.update_idletasks()  # 更新GUI
            
            # 等待进程完成
            return_code = process.wait()
            
            # 设置进度条为100%
            self.progress_var.set(100)
            
            if return_code == 0:
                self.add_to_console("\n打包成功完成! ✓\n")
                distpath = self.distpath_entry.get()
                if distpath:
                    distpath = os.path.abspath(distpath)
                    self.add_to_console(f"输出目录: {distpath}\n")
                    
                    # 尝试打开输出目录
                    try:
                        if sys.platform.startswith('win'):
                            os.startfile(distpath)
                        elif sys.platform.startswith('darwin'):
                            subprocess.Popen(['open', distpath])
                        else:
                            subprocess.Popen(['xdg-open', distpath])
                    except Exception as e:
                        self.add_to_console(f"提示: 无法自动打开输出目录 - {str(e)}\n")
                
                # 打包成功后自动清理项目，特别是删除build文件夹
                self.add_to_console("\n开始自动清理项目...\n")
                self.clean_project()
            else:
                self.add_to_console(f"\n打包失败! 错误代码: {return_code}\n")
                self.add_to_console("请检查日志输出以获取更多信息。\n")
            
            return return_code
                
        except Exception as e:
            self.add_to_console(f"\n执行过程中发生错误: {str(e)}\n")
            return -1
        finally:
            # 隐藏进度条
            self.progress_bar.grid_remove()
            # 重新启用打包按钮
            self.enable_buttons(True)
    
    def start_build(self):
        """开始打包过程"""
        # 验证输入
        if not self.validate_inputs():
            return
        
        command_list = self.build_command_list()
        if not command_list:
            return
        
        # 禁用按钮防止重复点击
        self.enable_buttons(False)
        self.add_to_console("打包中...\n")
        
        # 在子线程中运行打包命令
        thread = threading.Thread(target=self.execute_command, args=(command_list,))
        thread.daemon = True
        thread.start()
    
    def validate_inputs(self):
        """验证用户输入"""
        # 检查是否选择了脚本文件
        if not self.script_path:
            messagebox.showerror("错误", "请选择Python脚本文件")
            return False
        
        if not os.path.exists(self.script_path):
            messagebox.showerror("错误", f"脚本文件不存在: {self.script_path}")
            return False
        
        # 检查输出目录是否存在，如果不存在则创建
        dist_path = self.distpath_entry.get().strip()
        if dist_path:
            try:
                os.makedirs(dist_path, exist_ok=True)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出目录 {dist_path}: {str(e)}")
                return False
        
        # 检查图标文件是否存在
        icon_path = self.icon_entry.get().strip()
        if icon_path and not os.path.exists(icon_path):
            messagebox.showwarning("警告", f"图标文件不存在: {icon_path}")
            
        # 检查UPX目录是否存在
        upx_dir = self.upx_dir_entry.get().strip()
        if upx_dir and not os.path.exists(upx_dir):
            messagebox.showwarning("警告", f"UPX目录不存在: {upx_dir}")
            
        return True
    
    def clean_project(self):
        """清理项目"""
        if not self.script_path or not os.path.exists(self.script_path):
            messagebox.showerror("错误", "请先选择有效的脚本文件")
            return
            
        self.add_to_console("\n清理构建文件...\n")
        cleaned_items = 0
        
        try:
            # 删除build目录
            build_dir = "build"
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
                self.add_to_console(f"已删除: {build_dir}\n")
                cleaned_items += 1
            
            # 删除spec文件
            script_name = os.path.splitext(os.path.basename(self.script_path))[0]
            spec_file = f"{script_name}.spec"
            if os.path.exists(spec_file):
                os.remove(spec_file)
                self.add_to_console(f"已删除: {spec_file}\n")
                cleaned_items += 1
                
            # 删除生成的__pycache__
            cache_dir = "__pycache__"
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                self.add_to_console(f"已删除: {cache_dir}\n")
                cleaned_items += 1
                
            # 删除dist目录
            dist_dir = self.distpath_entry.get().strip()
            if dist_dir and os.path.exists(dist_dir) and dist_dir != os.path.abspath("dist"):
                shutil.rmtree(dist_dir)
                self.add_to_console(f"已删除: {dist_dir}\n")
                cleaned_items += 1
                
            self.add_to_console(f"清理完成，共清理了 {cleaned_items} 项\n")
        except Exception as e:
            self.add_to_console(f"清理时出错: {str(e)}\n")
    
    def install_dependencies(self):
        """自动安装PyInstaller依赖库"""
        self.add_to_console("检查并安装必要的依赖库...\n")
        
        # 获取当前Python路径
        python_path = self.python_path_entry.get().strip()
        if not python_path:
            python_path = self.current_python_path  # 使用初始化时获取的路径
        
        # 需要安装的依赖库列表
        required_packages = ["pyinstaller"]
        
        for package in required_packages:
            try:
                # 检查是否已安装
                result = subprocess.run([python_path, "-m", "pip", "show", package], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    # 未安装，尝试安装
                    self.add_to_console(f"正在安装 {package}...\n")
                    install_result = subprocess.run([python_path, "-m", "pip", "install", package], 
                                                  capture_output=True, text=True)
                    if install_result.returncode == 0:
                        self.add_to_console(f"{package} 安装成功!\n")
                    else:
                        self.add_to_console(f"{package} 安装失败: {install_result.stderr}\n")
                        messagebox.showwarning("安装失败", f"{package} 安装失败，请手动安装。")
                else:
                    self.add_to_console(f"{package} 已安装\n")
            except Exception as e:
                self.add_to_console(f"检查/安装 {package} 时出错: {str(e)}\n")
                messagebox.showwarning("安装错误", f"检查/安装 {package} 时出错，请手动安装。")
        
        self.add_to_console("依赖库检查完成\n")
    
    def enable_buttons(self, state):
        """启用或禁用按钮"""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.config(state=tk.NORMAL if state else tk.DISABLED)

if __name__ == "__main__":
    # 检查是否指定了Python路径
    python_path = None
    if len(sys.argv) > 1:
        python_path = sys.argv[1]
    
    # 根据tkinterdnd2库的可用性创建根窗口
    if dnd_available:
        try:
            root = TkinterDnD.Tk()
        except Exception as e:
            root = tk.Tk()
    else:
        root = tk.Tk()
    
    app = PyInstallerGUI(root)
    # 如果指定了Python路径，则设置到界面中
    if python_path:
        app.python_path_entry.delete(0, tk.END)
        app.python_path_entry.insert(0, python_path)
    root.mainloop()
