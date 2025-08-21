import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import shlex
import sys

class PyInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyInstaller 快速打包工具")
        self.root.geometry("650x850")
        self.root.resizable(True, True)
        
        # 主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建带标签的分组框架
        self.create_file_section()
        self.create_options_section()
        self.create_advanced_section()
        self.create_console_output()
        self.create_action_buttons()
        
        # 存储用户数据
        self.script_path = ""
        self.icon_path = ""
        self.add_data_list = []
        self.add_binary_list = []
        
    def create_file_section(self):
        """创建文件选择区域"""
        frame = ttk.LabelFrame(self.main_frame, text="脚本设置", padding=(10, 5))
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        
        # 脚本文件选择
        ttk.Label(frame, text="主脚本文件:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.script_entry = ttk.Entry(frame, width=50)
        self.script_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(frame, text="浏览...", command=self.select_script).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出名称
        ttk.Label(frame, text="输出名称:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(frame, width=50)
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # 输出路径
        ttk.Label(frame, text="输出目录:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.distpath_entry = ttk.Entry(frame, width=50)
        self.distpath_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(frame, text="浏览...", command=self.select_distpath).grid(row=2, column=2, padx=5, pady=5)
        
        # 设置默认输出路径为当前目录/dist
        self.distpath_entry.insert(0, os.path.abspath("dist"))
    
    def create_options_section(self):
        """创建主要选项区域"""
        frame = ttk.LabelFrame(self.main_frame, text="打包选项", padding=(10, 5))
        frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        
        # 打包模式
        ttk.Label(frame, text="打包模式:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.mode_var = tk.StringVar()
        self.mode_var.set("-F")  # 默认单文件模式
        ttk.Radiobutton(frame, text="单文件模式 (-F)", variable=self.mode_var, value="-F").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(frame, text="目录模式 (-D)", variable=self.mode_var, value="-D").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        
        # 控制台选项
        ttk.Label(frame, text="控制台:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.console_var = tk.StringVar()
        self.console_var.set("-c")  # 默认显示控制台
        ttk.Radiobutton(frame, text="显示控制台 (-c)", variable=self.console_var, value="-c").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(frame, text="无控制台 (-w)", variable=self.console_var, value="-w").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        
        # 图标设置
        ttk.Label(frame, text="应用图标:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.icon_entry = ttk.Entry(frame, width=50)
        self.icon_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(frame, text="浏览...", command=self.select_icon).grid(row=2, column=2, padx=5, pady=5)
        
        # UPX压缩
        self.upx_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="使用UPX压缩 (推荐)", variable=self.upx_var).grid(
            row=3, column=1, columnspan=2, sticky="w", padx=5, pady=5)
    
    def create_advanced_section(self):
        """创建高级选项区域"""
        frame = ttk.LabelFrame(self.main_frame, text="高级选项", padding=(10, 5))
        frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        
        # 附加数据文件
        ttk.Label(frame, text="附加资源文件 (源路径:目标路径)").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.add_data_frame = ttk.Frame(frame)
        self.add_data_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.add_data_frame.columnconfigure(0, weight=1)
        
        self.add_data_entry = ttk.Entry(self.add_data_frame, width=30)
        self.add_data_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(self.add_data_frame, text="添加", width=8, command=self.add_data_item).grid(row=0, column=1, padx=5)
        ttk.Button(self.add_data_frame, text="清除", width=8, command=self.clear_data_items).grid(row=0, column=2)
        
        # 数据文件列表
        self.data_listbox = tk.Listbox(frame, height=4, bg='white')
        self.data_listbox.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        # 额外参数
        ttk.Label(frame, text="额外命令行参数:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.extra_args_entry = ttk.Entry(frame)
        self.extra_args_entry.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
    
    def create_console_output(self):
        """创建控制台输出区域"""
        frame = ttk.LabelFrame(self.main_frame, text="打包日志", padding=(10, 5))
        frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        self.console_output = scrolledtext.ScrolledText(
            frame, wrap=tk.WORD, height=10, bg='#23272A', fg='white')
        self.console_output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # 添加开始消息
        self.add_to_console("PyInstaller GUI打包工具已就绪\n")
        self.add_to_console("请选择Python脚本并配置打包选项\n")
    
    def create_action_buttons(self):
        """创建操作按钮区域"""
        frame = ttk.Frame(self.main_frame)
        frame.grid(row=4, column=0, sticky="e", padx=5, pady=10)
        
        ttk.Button(frame, text="开始打包", command=self.start_build, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="清理项目", command=self.clean_project, width=15).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="退出", command=self.root.destroy, width=15).grid(row=0, column=2, padx=5)
    
    def select_script(self):
        """选择要打包的Python脚本"""
        script_path = filedialog.askopenfilename(
            filetypes=[("Python脚本", "*.py"), ("所有文件", "*.*")]
        )
        if script_path:
            self.script_path = os.path.abspath(script_path)
            self.script_entry.delete(0, tk.END)
            self.script_entry.insert(0, self.script_path)
            
            # 自动设置默认输出名称
            if not self.name_entry.get():
                file_name = os.path.splitext(os.path.basename(script_path))[0]
                self.name_entry.insert(0, file_name)
    
    def select_distpath(self):
        """选择输出目录"""
        distpath = filedialog.askdirectory()
        if distpath:
            self.distpath_entry.delete(0, tk.END)
            self.distpath_entry.insert(0, os.path.abspath(distpath))
    
    def select_icon(self):
        """选择应用图标"""
        icon_path = filedialog.askopenfilename(
            filetypes=[("图标文件", "*.ico"), ("所有文件", "*.*")]
        )
        if icon_path:
            self.icon_path = os.path.abspath(icon_path)
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, self.icon_path)
    
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
        """构建PyInstaller命令列表（更安全的执行方式）"""
        if not self.script_path:
            messagebox.showerror("错误", "请选择要打包的Python脚本")
            return None
        
        command = ["pyinstaller"]
        
        # 添加基本选项
        command.append(self.mode_var.get())  # 打包模式
        command.append(self.console_var.get())  # 控制台设置
        
        # 应用图标
        if self.icon_entry.get() and os.path.exists(self.icon_path):
            command.append("-i")
            command.append(self.icon_path)
        
        # 输出名称
        if self.name_entry.get():
            command.append("-n")
            command.append(self.name_entry.get())
        
        # 输出目录
        distpath = self.distpath_entry.get().strip()
        if distpath:
            command.append("--distpath")
            command.append(distpath)
        
        # UPX压缩
        if not self.upx_var.get():
            command.append("--noupx")
        
        # 附加数据文件
        for source, dest in self.add_data_list:
            command.append("--add-data")
            command.append(f"{source}{os.pathsep}{dest}")
        
        # 额外参数
        extra_args = self.extra_args_entry.get().strip()
        if extra_args:
            try:
                # 使用shlex正确拆分带空格和引号的参数
                command.extend(shlex.split(extra_args))
            except Exception as e:
                self.add_to_console(f"错误: 无法解析额外参数 - {str(e)}\n")
        
        # 添加主脚本（确保绝对路径）
        if os.path.exists(self.script_path):
            command.append(self.script_path)
        else:
            self.add_to_console(f"错误: 脚本文件不存在 - {self.script_path}\n")
            return None
            
        self.add_to_console(f"完整命令列表: {' '.join(command)}\n")
        return command
    
    def execute_command(self, command_list):
        """执行打包命令（使用安全的命令列表方式）"""
        self.add_to_console("=" * 60 + "\n")
        self.add_to_console("开始打包过程...\n")
        
        try:
            # 使用列表传递命令参数，避免shell=True
            process = subprocess.Popen(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 实时读取输出并显示
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.add_to_console(line)
            
            # 等待进程完成
            return_code = process.wait()
            
            if return_code == 0:
                self.add_to_console("\n打包成功完成! ✓\n")
                distpath = self.distpath_entry.get()
                if distpath:
                    distpath = os.path.abspath(distpath)
                    self.add_to_console(f"输出目录: {distpath}\n")
                    
                    # 尝试打开输出目录
                    if sys.platform.startswith('win'):
                        os.startfile(distpath)
                    elif sys.platform.startswith('darwin'):
                        subprocess.Popen(['open', distpath])
                    else:
                        subprocess.Popen(['xdg-open', distpath])
            else:
                self.add_to_console(f"\n打包失败! 错误代码: {return_code}\n")
            
            return return_code
                
        except Exception as e:
            self.add_to_console(f"\n执行过程中发生错误: {str(e)}\n")
            return -1
        finally:
            # 重新启用打包按钮
            self.enable_buttons(True)
    
    def start_build(self):
        """开始打包过程"""
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
    
    def clean_project(self):
        """清理项目"""
        if not self.script_path or not os.path.exists(self.script_path):
            messagebox.showerror("错误", "请先选择有效的脚本文件")
            return
            
        self.add_to_console("\n清理构建文件...\n")
        try:
            # 删除build目录
            build_dir = "build"
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
                self.add_to_console(f"已删除: {build_dir}\n")
            
            # 删除spec文件
            script_name = os.path.splitext(os.path.basename(self.script_path))[0]
            spec_file = f"{script_name}.spec"
            if os.path.exists(spec_file):
                os.remove(spec_file)
                self.add_to_console(f"已删除: {spec_file}\n")
                
            # 删除生成的__pycache__
            cache_dir = "__pycache__"
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                self.add_to_console(f"已删除: {cache_dir}\n")
                
            self.add_to_console("清理完成\n")
        except Exception as e:
            self.add_to_console(f"清理时出错: {str(e)}\n")
    
    def enable_buttons(self, state):
        """启用或禁用按钮"""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.config(state=tk.NORMAL if state else tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PyInstallerGUI(root)
    root.mainloop()
