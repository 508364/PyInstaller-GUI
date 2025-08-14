STRINGS = {
    # ---- App / Tabs ----
    "app_title": "PyInstaller GUI",
    "tab_basic": "Basic",
    "tab_assets": "Assets",
    "tab_advanced": "Advanced",
    "tab_logs": "Logs",

    # ---- Groups / Sections ----
    "group_script_settings": "Script & Output",
    "group_build_options": "Build Options",
    "group_data": "Additional Data (files/dirs)",
    "group_hidden_imports": "Hidden Imports",
    "group_excludes": "Exclude Modules",
    "group_hooks_dir": "Extra hooks dir (--additional-hooks-dir)",
    "group_runtime_hooks": "Runtime hooks (--runtime-hook)",
    "group_upx_exclude": "UPX Excludes (--upx-exclude)",
    "group_other_switches": "Other Switches",

    # ---- Labels / Inputs ----
    "label_main_script": "Entry script (.py):",
    "label_output_name": "Output name:",
    "label_output_dir": "Output directory:",
    "label_pack_mode": "Packaging mode:",
    "radio_onefile": "One-file (-F)",
    "radio_onedir": "One-dir (-D)",
    "label_console": "Run mode:",
    "radio_console": "Console (-c)",
    "radio_windowed": "Windowed (-w)",
    "label_app_icon": "App icon (.ico):",
    "label_version_file": "Version file:",

    # UPX
    "check_use_upx": "Use UPX compression",
    "check_upx_internal": "Use PyInstaller built-in UPX",
    "label_upx_level": "UPX level (external):",
    "check_upx_force": "Use --force (external)",
    "check_upx_only_libs": "DLL/PYD only, skip main EXE (one-dir only)",

    # Debug
    "label_debug_level": "Debug level (--debug):",
    "debug_off": "off",
    "debug_all": "all",
    "debug_imports": "imports",
    "debug_noarchive": "noarchive",

    # Advanced
    "label_runtime_tmpdir": "Runtime tmp dir (--runtime-tmpdir):",
    "label_extra_args": "Extra CLI args:",

    # Buttons
    "btn_browse": "Browse…",
    "btn_browse_file": "File",
    "btn_browse_dir": "Folder",
    "btn_add": "Add",
    "btn_clear": "Clear",
    "btn_build": "Build",
    "btn_clean_tmp": "Clean temp",
    "btn_exit": "Exit",
    "btn_cancel": "Cancel",

    # File dialogs / filters
    "title_select_resource_file": "Select resource file",
    "title_select_resource_dir": "Select resource folder",
    "title_select_version_file": "Select version file",
    "filter_py": "Python script (*.py)",
    "filter_ico": "Icon (*.ico)",
    "filter_version": "Version file (*.txt;*.ver;*.version)",
    "filter_all": "All files (*.*)",

    # Tooltips
    "tip_main_script": "Path to the entry .py file, e.g. C:\\Project\\main.py.",
    "tip_browse_script": "Pick the Python script as build entry.",
    "tip_output_name": "Executable/folder name (maps to -n). Leave blank to use script name.",
    "tip_distpath": "PyInstaller output directory (--distpath). Default: dist/.",
    "tip_browse_dist": "Select build output directory.",
    "tip_onefile": "One-file (-F): everything in a single EXE; startup may be slower.",
    "tip_onedir": "One-dir (-D): outputs a folder; starts faster; can combine with DLL/PYD-only compression.",
    "tip_console": "Console mode: keeps a console window for logs and errors.",
    "tip_windowed": "Windowed mode: no console; suitable for GUI apps.",
    "tip_icon": "Application icon (.ico).",
    "tip_browse_icon": "Pick an .ico file.",
    "tip_version_file": "Version info file (--version-file). Commonly *.txt / *.ver.",
    "tip_browse_version": "Select a version info file.",

    "tip_use_upx": "Master switch for UPX compression. Disables all UPX controls when off.",
    "tip_upx_internal": "Use PyInstaller’s built-in UPX (if available). Disables external post-compression.",
    "tip_upx_level": "External UPX compression level 1–10 (higher compresses more; may be slower).",
    "tip_upx_force": "Force-compress PE files with CFG/GuardCF (risky; may break executables).",
    "tip_upx_only_libs": "Visible only in one-dir (-D), to the right of \"Use --force\". Compress DLL/PYD only and skip main EXE.",

    "tip_debug": "Choose PyInstaller --debug value; usually keep it off.",
    "tip_data_add": "Enter ‘src|dst’ or ‘src=>dst’. Example: assets|assets or data\\cfg=>cfg.",
    "tip_browse_res_file": "Pick a resource file and fill the input.",
    "tip_browse_res_dir": "Pick a resource folder and fill the input.",
    "tip_add_res": "Add the resource item above into the list.",
    "tip_clear_res": "Clear the resource list.",
    "tip_data_list": "Will be added via --add-data (src→dst).",

    "tip_hidden_imports": "Add modules for hidden imports, e.g. PyQt5.sip.",
    "tip_add_hidden": "Add the module above into hidden imports list.",
    "tip_clear_hidden": "Clear the hidden imports list.",
    "tip_hidden_list": "Each item becomes a --hidden-import.",

    "tip_excludes": "Exclude modules from build, e.g. tkinter, tests.",
    "tip_add_exclude": "Add the module above into exclude list.",
    "tip_clear_exclude": "Clear the exclude list.",
    "tip_excludes_list": "Each item becomes an --exclude-module.",

    "tip_hooks_dir": "Extra hooks directory path (with hook-*.py).",
    "tip_add_hooks_dir": "Add hooks dir to the list.",
    "tip_clear_hooks_dir": "Clear the hooks dir list.",
    "tip_hooks_list": "Each item becomes an --additional-hooks-dir.",

    "tip_runtime_hook": "Runtime hook script path (executed at app start).",
    "tip_add_runtime_hook": "Add the runtime hook above to the list.",
    "tip_clear_runtime_hook": "Clear the runtime hook list.",
    "tip_runtime_list": "Each item becomes a --runtime-hook.",

    "tip_upx_exclude": "Patterns to skip in external UPX, e.g. *.dll or vcruntime*.dll.",
    "tip_add_upx_exclude": "Add the pattern above into UPX excludes list.",
    "tip_clear_upx_exclude": "Clear the UPX excludes list.",
    "tip_upx_excl_list": "Files matching these patterns will be skipped by external UPX.",

    "tip_disable_windowed_tb": "In windowed mode, disable Tk’s windowed traceback and print to logs instead.",

    "tip_runtime_tmpdir": "Directory used for unpacking at runtime (--runtime-tmpdir). Example: C:\\Temp\\myapp.",
    "tip_extra_args": "Additional PyInstaller args separated by spaces. Example: --collect-data pkg --clean.",

    "tip_btn_build": "Start the build pipeline.",
    "tip_btn_clean": "Remove build/, __pycache__, .spec and related temp files.",
    "tip_btn_exit": "Exit the application.",

    # ---- Notes / Version conditional ----
    "check_win_no_prefer_redirects": "win-no-prefer-redirects",
    "check_win_private_assemblies": "win-private-assemblies",
    "note_winsxs_removed": "Note: WinSxS switches are removed in PyInstaller 6+.",

    # ---- Errors / Warnings / Logs ----
    "title_error": "Error",
    "error_select_script": "Please select an entry script (.py) first.",
    "warn_icon_missing": "Icon file not found: {path}",
    "warn_version_missing": "Version file not found: {path}",
    "err_extra_args": "Failed to parse extra args: {err}",
    "err_script_missing": "Entry script does not exist: {path}",

    "log_ready": "Environment ready.",
    "log_select_script": "Select your entry script before building.",
    "log_full_cmd": "Full command:",
    "log_start_build": "Starting build...",
    "log_building": "Running PyInstaller build, please wait…",
    "log_build_success": "Build success",
    "log_output_dir": "Output directory: {path}",
    "log_open_dir_failed": "Failed to open output directory: {err}",
    "log_build_failed": "Build failed with exit code: {code}",
    "log_cleaning": "Cleaning temp files and caches…",
    "log_deleted": "Deleted: {name}",
    "log_clean_done": "Clean done.",
    "log_clean_error": "Clean failed: {err}",
    "log_only_libs_hint_singlefile": "“DLL/PYD only” is enabled but one-file (-F) is selected; this setting will not take effect.",

    "msg_tip_windowed": "Tip: In windowed (-w) mode, exceptions may not show a traceback. Consider enabling “disable windowed traceback” or use console mode (-c).",

    # ---- UPX availability / messages ----
    "upx_not_found_try_install": "UPX not found. Trying to install Python package 'upx' via pip…",
    "upx_unavailable_disable": "UPX still unavailable. External compression will be skipped.",
    "upx_installed_ok": "UPX installation finished.",
    "upx_added_to_path": "Added UPX directory to PATH: {path}",
    "upx_cfg_unsupported_skip": "[UPX] Skipped (CFG/GuardCF): {name} (PE with GUARD_CF not supported)",
    "upx_cfg_hint_enable_force": "Hint: If you must compress it, enable “Use --force” in Basic settings and retry (risky; may break the app).",

    # ---- PyInstaller installation flow ----
    "ask_install_pyinstaller_title": "Install PyInstaller?",
    "ask_install_pyinstaller": "PyInstaller is not detected. This tool depends on PyInstaller to build executables; without it the app cannot be used. Install now? (Internet required)",
    "msg_dependency_required": "This tool requires PyInstaller and cannot be used without it.",
    "msg_install_failed": "Installing PyInstaller failed or it cannot be imported.",
    "install_window_title": "Installing PyInstaller",
    "install_progress_label_wait": "Installing PyInstaller (this window will close automatically). Speed depends on your network…",
}
