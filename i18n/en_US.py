# i18n/en_US.py
# -*- coding: utf-8 -*-
STRINGS = {
    "app_title": "PyInstaller Quick Pack Tool",
    "tab_basic": "Basic",
    "tab_assets": "Assets & Imports",
    "tab_advanced": "Advanced",
    "tab_logs": "Logs",

    "group_script_settings": "Script Settings",
    "group_build_options": "Build Options",
    "group_data": "Additional Data (source:dest)",
    "group_binaries": "Additional Binaries (source:dest)",
    "group_hidden_imports": "Hidden Imports",
    "group_excludes": "Excluded Modules",
    "group_hooks_dir": "Additional Hooks Dirs",
    "group_runtime_hooks": "Runtime Hook Files",
    "group_upx_exclude": "UPX Exclude (pattern)",
    "group_other_switches": "Other Switches",

    "label_main_script": "Main script:",
    "label_output_name": "Output name:",
    "label_output_dir": "Output dir:",
    "label_pack_mode": "Packaging mode:",
    "label_console": "Console:",
    "label_app_icon": "App icon:",
    "label_version_file": "Version info file:",
    "label_debug_level": "Debug level:",
    "label_runtime_tmpdir": "Runtime temp dir (--runtime-tmpdir)",
    "label_extra_args": "Extra CLI args:",
    "label_upx_level": "UPX level",

    "radio_onefile": "One-file (-F)",
    "radio_onedir": "One-dir (-D)",
    "radio_console": "Console (-c)",
    "radio_windowed": "Windowed (-w)",

    "check_use_upx": "Use UPX compression (recommended)",
    "check_upx_force": "Use --force (may break the binary)",
    "check_upx_internal": "Use PyInstaller internal UPX",
    "check_noarchive": "Disable archive (--noarchive)",
    "check_disable_windowed_tb": "Disable windowed traceback (--disable-windowed-traceback)",
    "check_win_no_prefer_redirects": "win-no-prefer-redirects",
    "check_win_private_assemblies": "win-private-assemblies",

    "debug_off": "Off",
    "debug_all": "all",
    "debug_imports": "imports",
    "debug_noarchive": "noarchive",

    "btn_browse": "Browse...",
    "btn_add": "Add",
    "btn_clear": "Clear",
    "btn_build": "Build",
    "btn_clean": "Clean",
    "btn_clean_tmp": "Clean temp files",
    "btn_exit": "Exit",

    "btn_browse_file": "Choose file",
    "btn_browse_dir": "Choose folder",

    "title_select_version_file": "Select version info file",
    "title_select_resource_file": "Select resource file",
    "title_select_resource_dir": "Select resource folder",

    "filter_py": "Python script",
    "filter_all": "All files",
    "filter_ico": "Icon file",
    "filter_version": "Version info file",

    "title_error": "Error",
    "error_select_script": "Please select the Python script to build",

    "warn_icon_missing": "Warning: icon file not found, skipped - {path}",
    "warn_version_missing": "Warning: version info file not found, skipped - {path}",

    "err_extra_args": "Error: cannot parse extra args - {err}",
    "err_script_missing": "Error: script file not found - {path}",

    "log_ready": "PyInstaller GUI is ready",
    "log_select_script": "Select a Python script and configure build options",
    "log_building": "Building...",
    "log_start_build": "Start building...",
    "log_build_success": "Build finished successfully!",
    "log_output_dir": "Output dir: {path}",
    "log_open_dir_failed": "Failed to open output dir: {err}",
    "log_build_failed": "Build failed! Exit code: {code}",
    "log_full_cmd": "Full command:",

    "msg_tip_windowed": "Tip: running in windowed mode; exceptions will show in a message box.",

    "log_cleaning": "Cleaning build files...",
    "log_deleted": "Deleted: {name}",
    "log_clean_done": "Clean finished",
    "log_clean_error": "Error during clean: {err}",

    "upx_not_found_try_install": "UPX not found, trying to install automatically: pip install upx",
    "upx_installed_ok": "UPX installed and available.",
    "upx_added_to_path": "Found UPX and added to PATH: {path}",
    "upx_unavailable_disable": "Could not configure UPX; UPX compression will be disabled (--noupx).",

    # Tooltips (concise + tiny examples)
    "tip_main_script": "Pick the entry .py script. e.g. main.py. Output name defaults to the script name.",
    "tip_browse_script": "Browse and choose the entry script (e.g. src/app.py).",
    "tip_output_name": "Leave empty to use script name. Examples: MyApp, Toolbox.",
    "tip_distpath": "Directory for build outputs (default: dist). Example: D:\\builds\\MyApp.",
    "tip_browse_dist": "Browse and choose the output directory (created if missing).",
    "tip_icon": "Optional .ico for Windows EXE icon. Example: assets\\app.ico.",
    "tip_browse_version": "Choose a version file (e.g. version.txt / version.ini).",
    "tip_version_file": "File for --version-file; may include company/name/version metadata.",

    "tip_onefile": "Single executable; extracts to a temp dir at runtime. Larger/slower to start.",
    "tip_onedir": "Folder output; faster start and easier to debug. Ship the whole folder.",
    "tip_console": "Show console window (good for CLI or debugging prints/logs).",
    "tip_windowed": "No console (good for GUI). Exceptions show in a message box.",

    "tip_use_upx": "Run UPX on outputs after a successful build (external pass).",
    "tip_upx_force": "External UPX only: force-compress unsupported PE (e.g., with CFG). Risky; may break the binary.",
    "tip_upx_internal": "Let PyInstaller invoke UPX (more conservative; may skip main EXE, esp. with CFG). Disables level slider and --force.",
    "tip_upx_level": "UPX level 1–9: 1=fastest/least compression; 9=smallest/slowest. Suggest 5–7.",
    "tip_debug": "PyInstaller debug: imports=log imports; noarchive=unpack archive; all=more verbose.",

    "hint_resources_input": "Enter then Add. Support: src (file/dir), or src|dest for package path.\nExamples: assets|assets   C:\\img\\logo.png|images\\logo.png",

    "tip_data_add": "Bundle extra files/dirs. Examples: data|data, config.json|cfg\\config.json.",
    "tip_browse_res_file": "Pick a resource file (images, config, etc.).",
    "tip_browse_res_dir": "Pick a resource folder (kept under the same folder name).",
    "tip_add_res": "Add the path above to the list (supports src|dest).",
    "tip_clear_res": "Clear the resource list.",
    "tip_data_list": "Added resource mappings (src → dest).",

    "tip_hidden_imports": "Explicit modules PyInstaller can’t discover. Example: pkg.submod.",
    "tip_add_hidden": "Add a hidden import (press Enter to continue adding).",
    "tip_clear_hidden": "Clear the hidden-import list.",
    "tip_hidden_list": "Modules passed via --hidden-import.",

    "tip_excludes": "Modules to exclude from the build. Examples: tkinter, torch.tests.",
    "tip_add_exclude": "Add an excluded module (package or submodule).",
    "tip_clear_exclude": "Clear the exclude list.",
    "tip_excludes_list": "Modules passed via --exclude-module.",

    "tip_hooks_dir": "Extra hooks search directories (containing hook-*.py).",
    "tip_add_hooks_dir": "Add a hooks directory.",
    "tip_clear_hooks_dir": "Clear the hooks-dir list.",
    "tip_hooks_list": "Added hooks directories.",

    "tip_runtime_hook": "Script executed at startup (set env vars, adjust paths). Example: fix_paths.py.",
    "tip_add_runtime_hook": "Add a runtime hook file.",
    "tip_clear_runtime_hook": "Clear the runtime-hook list.",
    "tip_runtime_list": "Added runtime hooks.",

    "tip_upx_exclude": "Prevent certain files from UPX. Globs supported: *.dll, *_debug.pyd.",
    "tip_add_upx_exclude": "Add one UPX exclude pattern.",
    "tip_clear_upx_exclude": "Clear the UPX exclude list.",
    "tip_upx_excl_list": "Files matched here will be skipped by UPX.",

    "tip_disable_windowed_tb": "In windowed mode, disable the traceback message box.",
    "tip_runtime_tmpdir": "Temp dir used by one-file at runtime. Must be writable.\nExamples: %TEMP%\\myapp or D:\\tmp\\myapp.",
    "tip_extra_args": "Raw args passed directly to PyInstaller.\nExamples: --collect-all pkg --paths C:\\py\\libs.\nNote: --add-data uses 'src;dest' on Windows, 'src:dest' on Linux/macOS.",

    "tip_btn_build": "Start build (auto-switch to Logs tab).",
    "tip_btn_clean": "Delete build, .spec (same name as script), and __pycache__.",
    "tip_btn_exit": "Quit the app.",

    "note_winsxs_removed": "Note: WinSxS-related flags were removed since PyInstaller 6.",

    "upx_cfg_unsupported_skip": "[UPX] Skipped (CFG/GuardCF): {name} (PE with GUARD_CF is not supported)",
    "upx_cfg_hint_exclude": "Hint: add this filename or a pattern to 'UPX Exclude (pattern)' to avoid future attempts; if you must compress, you can try --force at your own risk (may break the binary).",
    "upx_cfg_hint_enable_force": "Hint: if you really need to compress it, tick 'Use --force (may break the binary)' in Basic settings and rebuild.",
}
