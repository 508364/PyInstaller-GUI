# -*- coding: utf-8 -*-
STRINGS = {
    # ---- App / Tabs ----
    "app_title": "PyInstaller 打包工具",
    "tab_basic": "基本设置",
    "tab_assets": "附加资源",
    "tab_advanced": "高级选项",
    "tab_logs": "日志输出",

    # ---- Groups / Sections ----
    "group_script_settings": "脚本与输出",
    "group_build_options": "构建选项",
    "group_data": "附加数据（文件/目录）",
    "group_hidden_imports": "隐藏导入（hiddenimports）",
    "group_excludes": "排除模块（excludes）",
    "group_hooks_dir": "额外 hooks 目录（--additional-hooks-dir）",
    "group_runtime_hooks": "运行时 hooks（--runtime-hook）",
    "group_upx_exclude": "UPX 排除（--upx-exclude）",
    "group_other_switches": "其他开关",

    # ---- Labels / Inputs ----
    "label_main_script": "主脚本 (.py)：",
    "label_output_name": "输出名称：",
    "label_output_dir": "输出目录：",
    "label_pack_mode": "打包模式：",
    "radio_onefile": "单文件（-F）",
    "radio_onedir": "目录模式（-D）",
    "label_console": "运行方式：",
    "radio_console": "控制台（-c）",
    "radio_windowed": "窗口（-w）",
    "label_app_icon": "应用图标 (.ico)：",
    "label_version_file": "版本信息文件：",

    # UPX
    "check_use_upx": "使用 UPX 压缩",
    "check_upx_internal": "使用 PyInstaller 内置 UPX",
    "label_upx_level": "UPX 压缩级别（外压）：",
    "check_upx_force": "使用 --force（外压）",
    "check_upx_only_libs": "仅压 DLL/PYD，不压主 EXE（仅目录模式）",

    # Debug
    "label_debug_level": "调试级别（--debug）：",
    "debug_off": "关闭",
    "debug_all": "all",
    "debug_imports": "imports",
    "debug_noarchive": "noarchive",

    # Advanced
    "label_runtime_tmpdir": "运行时临时目录（--runtime-tmpdir）：",
    "label_extra_args": "额外命令行参数：",

    # Buttons
    "btn_browse": "浏览…",
    "btn_browse_file": "选文件",
    "btn_browse_dir": "选目录",
    "btn_add": "添加",
    "btn_clear": "清空",
    "btn_build": "开始构建",
    "btn_clean_tmp": "清理临时文件",
    "btn_exit": "退出",
    "btn_cancel": "取消",

    # File dialogs / filters
    "title_select_resource_file": "选择资源文件",
    "title_select_resource_dir": "选择资源目录",
    "title_select_version_file": "选择版本信息文件",
    "filter_py": "Python 脚本 (*.py)",
    "filter_ico": "图标文件 (*.ico)",
    "filter_version": "版本文件 (*.txt;*.ver;*.version)",
    "filter_all": "所有文件 (*.*)",

    # Tooltips（适度示例）
    "tip_main_script": "入口 .py 文件路径。例如：C:\\项目\\main.py。",
    "tip_browse_script": "选择作为打包入口的 Python 脚本。",
    "tip_output_name": "生成的可执行文件/目录名称（对应 -n）。留空则使用脚本名。",
    "tip_distpath": "PyInstaller 输出目录（--distpath）。默认 dist/。",
    "tip_browse_dist": "选择产物输出目录。",
    "tip_onefile": "单文件（-F）：所有依赖打包成一个 EXE，启动可能稍慢。",
    "tip_onedir": "目录（-D）：输出文件夹，启动更快；可结合“仅压 DLL/PYD”。",
    "tip_console": "控制台模式：保留控制台窗口，便于查看日志和报错。",
    "tip_windowed": "窗口模式：无控制台，适合 GUI 程序。",
    "tip_icon": "应用图标（.ico）。",
    "tip_browse_icon": "选择 .ico 图标文件。",
    "tip_version_file": "版本信息文件（--version-file）。常见为 *.txt / *.ver。",
    "tip_browse_version": "选择版本信息文件。",

    "tip_use_upx": "启用 UPX 压缩开关。关闭后与 UPX 相关控件全部禁用。",
    "tip_upx_internal": "使用 PyInstaller 内置 UPX（如果可用）。启用后将不会进行构建后的外部 UPX 压缩。",
    "tip_upx_level": "外部 UPX 压缩级别 1–10（越高压缩越强，耗时可能更久）。",
    "tip_upx_force": "对启用 CFG/GuardCF 的 PE 强制压缩（可能导致不可运行，谨慎使用）。",
    "tip_upx_only_libs": "仅在目录模式（-D）可见，位于“使用 --force”的右侧。启用后只压 DLL/PYD，跳过主 EXE。",

    "tip_debug": "选择 PyInstaller 的 --debug 选项；一般保持“关闭”。",
    "tip_data_add": "填入 ‘源|目标’ 或 ‘源=>目标’，例如：assets|assets 或 data\\cfg=>cfg。",
    "tip_browse_res_file": "选择要打包的资源文件并填入输入框。",
    "tip_browse_res_dir": "选择要打包的资源目录并填入输入框。",
    "tip_add_res": "将上方输入框的资源条目添加到列表。",
    "tip_clear_res": "清空资源列表。",
    "tip_data_list": "将以 --add-data 形式加入构建（源→目标）。",

    "tip_hidden_imports": "缺少隐式导入时填写模块名，例如：PyQt5.sip。",
    "tip_add_hidden": "将上方模块名添加到隐藏导入列表。",
    "tip_clear_hidden": "清空隐藏导入列表。",
    "tip_hidden_list": "打包时为每一项附加 --hidden-import。",

    "tip_excludes": "需要从构建中排除的模块名，例如：tkinter, tests。",
    "tip_add_exclude": "将上方模块名添加到排除列表。",
    "tip_clear_exclude": "清空排除列表。",
    "tip_excludes_list": "打包时为每一项附加 --exclude-module。",

    "tip_hooks_dir": "额外 hooks 目录路径（存放 hook-*.py）。",
    "tip_add_hooks_dir": "添加 hooks 目录到列表。",
    "tip_clear_hooks_dir": "清空 hooks 目录列表。",
    "tip_hooks_list": "打包时为每一项附加 --additional-hooks-dir。",

    "tip_runtime_hook": "运行时 hook 脚本路径（会在程序启动时执行）。",
    "tip_add_runtime_hook": "添加运行时 hook 到列表。",
    "tip_clear_runtime_hook": "清空运行时 hook 列表。",
    "tip_runtime_list": "打包时为每一项附加 --runtime-hook。",

    "tip_upx_exclude": "UPX 外压时要排除的文件名或匹配模式，例如：*.dll 或 vcruntime*.dll。",
    "tip_add_upx_exclude": "将上方模式添加到 UPX 排除列表。",
    "tip_clear_upx_exclude": "清空 UPX 排除列表。",
    "tip_upx_excl_list": "外部 UPX 压缩时，匹配这些模式的文件将被跳过。",

    "tip_disable_windowed_tb": "窗口模式下禁用 Tk 的窗口化回溯，把异常打印到日志。",

    "tip_runtime_tmpdir": "指定解包时使用的临时目录（--runtime-tmpdir）。示例：C:\\Temp\\myapp。",
    "tip_extra_args": "其他 PyInstaller 参数，空格分隔。例如：--collect-data pkgname --clean。",

    "tip_btn_build": "开始执行打包流程。",
    "tip_btn_clean": "删除 build/、__pycache__、.spec 等临时产物。",
    "tip_btn_exit": "退出程序。",

    # ---- Notes / Version conditional ----
    "check_win_no_prefer_redirects": "win-no-prefer-redirects",
    "check_win_private_assemblies": "win-private-assemblies",
    "note_winsxs_removed": "提示：在 PyInstaller 6+ 中，WinSxS 相关选项已废弃。",

    # ---- Errors / Warnings / Logs ----
    "title_error": "错误",
    "error_select_script": "请先选择主脚本（.py）。",
    "warn_icon_missing": "图标文件不存在：{path}",
    "warn_version_missing": "版本信息文件不存在：{path}",
    "err_extra_args": "额外参数解析失败：{err}",
    "err_script_missing": "入口脚本不存在：{path}",

    "log_ready": "环境就绪。",
    "log_select_script": "请选择主脚本后再开始构建。",
    "log_full_cmd": "完整命令：",
    "log_start_build": "开始构建...",
    "log_building": "正在执行 PyInstaller 构建，请稍候…",
    "log_build_success": "构建完成",
    "log_output_dir": "输出目录：{path}",
    "log_open_dir_failed": "尝试打开输出目录失败：{err}",
    "log_build_failed": "构建失败，返回码：{code}",
    "log_cleaning": "正在清理临时文件与缓存…",
    "log_deleted": "已删除：{name}",
    "log_clean_done": "清理完成。",
    "log_clean_error": "清理失败：{err}",
    "log_only_libs_hint_singlefile": "已启用“仅压 DLL/PYD”，但当前为单文件模式（-F），此设置将不会生效。",

    "msg_tip_windowed": "提示：窗口模式（-w）下异常可能不弹出栈，请考虑启用“禁用窗口化回溯”或使用控制台模式（-c）。",

    # ---- UPX availability / messages ----
    "upx_not_found_try_install": "未检测到 upx，正在尝试通过 pip 安装 Python 包“upx”…",
    "upx_unavailable_disable": "upx 仍不可用，将跳过外部 UPX 压缩。",
    "upx_installed_ok": "upx 安装完成。",
    "upx_added_to_path": "已将 upx 所在目录加入 PATH：{path}",
    "upx_cfg_unsupported_skip": "[UPX] 跳过（CFG/GuardCF）：{name}（启用 GUARD_CF 的 PE 当前不受支持）",
    "upx_cfg_hint_enable_force": "提示：如必须压缩，可在基本设置勾选“使用 --force”后重试（存在风险，可能导致程序无法运行）。",

    # ---- PyInstaller installation flow ----
    "ask_install_pyinstaller_title": "安装 PyInstaller？",
    "ask_install_pyinstaller": "未检测到 PyInstaller。本工具依赖 PyInstaller 来打包可执行文件；若不安装将无法使用。是否现在自动安装？（需要联网）",
    "msg_dependency_required": "本工具依赖 PyInstaller，未安装将无法使用。",
    "msg_install_failed": "安装 PyInstaller 失败或无法导入。",
    "install_window_title": "正在安装 PyInstaller",
    "install_progress_label_wait": "正在安装 PyInstaller（窗口将自动关闭）。安装速度取决于网速，请耐心等待…",
}
