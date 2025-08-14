# -*- coding: utf-8 -*-
STRINGS = {
    "app_title": "PyInstaller 快速打包工具",
    "tab_basic": "基本设置",
    "tab_assets": "资源与导入",
    "tab_advanced": "高级选项",
    "tab_logs": "日志",

    "group_script_settings": "脚本设置",
    "group_build_options": "打包选项",
    "group_data": "附加资源文件（源路径:目标路径）",
    "group_binaries": "附加二进制（源路径:目标路径）",
    "group_hidden_imports": "隐藏导入模块",
    "group_excludes": "排除模块",
    "group_hooks_dir": "额外 Hooks 目录",
    "group_runtime_hooks": "运行时 Hook 文件",
    "group_upx_exclude": "UPX 排除（模式）",
    "group_other_switches": "其他开关",

    "label_main_script": "主脚本文件:",
    "label_output_name": "输出名称:",
    "label_output_dir": "输出目录:",
    "label_pack_mode": "打包模式:",
    "label_console": "控制台:",
    "label_app_icon": "应用图标:",
    "label_version_file": "版本信息文件:",
    "label_debug_level": "调试等级:",
    "label_runtime_tmpdir": "运行时临时目录 (--runtime-tmpdir)",
    "label_extra_args": "额外命令行参数:",
    "label_upx_level": "UPX 压缩级别",

    "radio_onefile": "单文件模式 (-F)",
    "radio_onedir": "目录模式 (-D)",
    "radio_console": "显示控制台 (-c)",
    "radio_windowed": "无控制台 (-w)",

    "check_use_upx": "使用 UPX 压缩（推荐）",
    "check_noarchive": "禁用归档 (--noarchive)",
    "check_disable_windowed_tb": "禁用 Windowed 回溯弹窗 (--disable-windowed-traceback)",
    "check_win_no_prefer_redirects": "win-no-prefer-redirects",
    "check_win_private_assemblies": "win-private-assemblies",

    "debug_off": "关闭",
    "debug_all": "all",
    "debug_imports": "imports",
    "debug_noarchive": "noarchive",

    "btn_browse": "浏览...",
    "btn_add": "添加",
    "btn_clear": "清除",
    "btn_build": "开始构建",
    "btn_clean": "清理项目",
    "btn_clean_tmp": "清理临时文件",
    "btn_exit": "退出",

    "btn_browse_file": "选择文件",
    "btn_browse_dir": "选择目录",

    "title_select_version_file": "选择版本信息文件",
    "title_select_resource_file": "选择资源文件",
    "title_select_resource_dir": "选择资源目录",

    "filter_py": "Python 脚本",
    "filter_all": "所有文件",
    "filter_ico": "图标文件",
    "filter_version": "版本信息文件",

    "title_error": "错误",
    "error_select_script": "请选择要打包的 Python 脚本",

    "warn_icon_missing": "警告: 图标文件不存在，已忽略 - {path}",
    "warn_version_missing": "警告: 版本信息文件不存在，已忽略 - {path}",

    "err_extra_args": "错误: 无法解析额外参数 - {err}",
    "err_script_missing": "错误: 脚本文件不存在 - {path}",

    "log_ready": "PyInstaller GUI 打包工具已就绪",
    "log_select_script": "请选择 Python 脚本并配置打包选项",
    "log_building": "打包中...",
    "log_start_build": "开始打包过程...",
    "log_build_success": "打包成功完成!",
    "log_output_dir": "输出目录: {path}",
    "log_open_dir_failed": "打开输出目录失败: {err}",
    "log_build_failed": "打包失败! 错误代码: {code}",
    "log_full_cmd": "完整命令列表:",

    "msg_tip_windowed": "提示：当前为无控制台模式，若运行期异常将以弹窗形式显示回溯。",

    "log_cleaning": "清理构建文件...",
    "log_deleted": "已删除: {name}",
    "log_clean_done": "清理完成",
    "log_clean_error": "清理时出错: {err}",

    "upx_not_found_try_install": "未检测到 UPX，尝试自动安装：pip install upx",
    "upx_install_default_failed": "通过默认源安装 UPX 失败：{err}\n尝试使用清华镜像...",
    "upx_install_ts_fail": "通过清华镜像安装 UPX 失败：{err}",
    "upx_installed_ok": "UPX 安装成功，已可用。",
    "upx_added_to_path": "已定位并添加 UPX 到 PATH: {path}",
    "upx_unavailable_disable": "未能自动配置 UPX，将禁用 UPX 压缩（等价 --noupx）。",

    # ---------- 悬停提示（精简说明 + 小范例） ----------
    "tip_main_script": "选择入口 .py 脚本。示例：main.py。更换后会自动以文件名作为默认输出名。",
    "tip_browse_script": "浏览并选择入口脚本（如 src/app.py）。",
    "tip_output_name": "可留空自动使用脚本文件名。示例：MyApp、工具箱。",
    "tip_distpath": "构建产物输出目录（默认 dist）。示例：D:\\builds\\MyApp。",
    "tip_browse_dist": "浏览并选择输出目录（不存在会自动创建）。",
    "tip_icon": "可选 .ico 图标（仅 Windows 生效）。示例：assets\\app.ico。",
    "tip_browse_icon": "浏览 .ico 图标文件；可用在线工具从 png 生成 .ico。",
    "tip_version_file": "用于 --version-file 的信息文件。可包含公司/版本等元数据。",
    "tip_browse_version": "选择 version 文件（如 version.txt / version.ini）。",

    "tip_onefile": "单文件可执行；启动时会解压到临时目录，体积略大，启动略慢。",
    "tip_onedir": "输出到文件夹；启动更快、便于调试，发布时拷贝整个目录即可。",
    "tip_console": "显示控制台窗口，适合 CLI 或需要查看 print/log 的程序。",
    "tip_windowed": "隐藏控制台，适合 GUI 程序。异常回溯将以弹窗显示。",

    "tip_use_upx": "构建成功后对 .exe/.dll/.pyd 执行 UPX 压缩以减小体积。",
    "tip_upx_level": "UPX 级别 1–9：1=最快/压缩弱；9=最小/最慢。示例：推荐 5~7。",
    "tip_debug": "PyInstaller 调试：imports=打印导入；noarchive=不打包归档；all=更详细。",

    "hint_resources_input": "输入后点“添加”。支持：源（文件/目录），或 源|目标 指定包内相对路径。\n示例：assets|assets   C:\\img\\logo.png|images\\logo.png",

    "tip_data_add": "把额外文件/目录打进包内。示例：data|data、config.json|cfg\\config.json。",
    "tip_browse_res_file": "选择要打包的资源文件（如图片、配置等）。",
    "tip_browse_res_dir": "选择要打包的资源目录（将以相同目录名放入包内）。",
    "tip_add_res": "将上方路径加入资源列表（支持 源|目标）。",
    "tip_clear_res": "清空已添加的资源。",
    "tip_data_list": "已添加的资源映射（源 → 目标）。",

    "tip_hidden_imports": "显式声明导入不到的模块。示例：pkg.submod。",
    "tip_add_hidden": "添加一个隐藏导入（回车后可继续添加）。",
    "tip_clear_hidden": "清空隐藏导入列表。",
    "tip_hidden_list": "当前将通过 --hidden-import 传入 PyInstaller 的模块。",

    "tip_excludes": "打包时排除的模块。示例：tkinter、torch.tests。",
    "tip_add_exclude": "添加一个排除模块（支持包名或子模块名）。",
    "tip_clear_exclude": "清空排除模块列表。",
    "tip_excludes_list": "将通过 --exclude-module 排除的模块。",

    "tip_hooks_dir": "额外 hooks 搜索目录（内含 hook-*.py）。适用于自定义收集逻辑。",
    "tip_add_hooks_dir": "添加一个 hooks 目录。",
    "tip_clear_hooks_dir": "清空 hooks 目录列表。",
    "tip_hooks_list": "已添加的 hooks 目录。",

    "tip_runtime_hook": "启动时先执行的脚本（调整环境变量、搜索路径等）。示例：fix_paths.py。",
    "tip_add_runtime_hook": "添加一个 runtime hook 文件。",
    "tip_clear_runtime_hook": "清空 runtime hook 列表。",
    "tip_runtime_list": "已添加的 runtime hooks。",

    "tip_upx_exclude": "防止某些文件被 UPX。支持通配符：*.dll、*_debug.pyd。",
    "tip_add_upx_exclude": "添加一条 UPX 排除模式。",
    "tip_clear_upx_exclude": "清空 UPX 排除列表。",
    "tip_upx_excl_list": "UPX 将跳过这些匹配的文件。",

    "tip_disable_windowed_tb": "Windowed 下禁用回溯弹窗（异常将不再以弹窗显示）。",

    # —— 新增：你提到的两处缺失（更有用的小范例） ——
    "tip_runtime_tmpdir": "one-file 模式解压与运行的临时目录。可自定义到可写路径。\n示例：%TEMP%\\myapp 或 D:\\tmp\\myapp。",
    "tip_extra_args": "直接透传给 PyInstaller 的原始参数。\n示例：--collect-all pkg --paths C:\\py\\libs。\n注意：--add-data 在 Windows 用“源;目标”，在 Linux/macOS 用“源:目标”。",

    "tip_btn_build": "开始构建（自动跳转到“日志”查看输出）。",
    "tip_btn_clean": "删除 build、脚本同名 .spec、__pycache__ 等临时文件。",
    "tip_btn_exit": "退出程序。",

    "note_winsxs_removed": "提示：PyInstaller 6 起已移除 WinSxS 相关参数。",
}
