# -*- coding: utf-8 -*-
STRINGS = {
    # ---- App / Tabs ----
    "app_title": "PyInstaller 打包工具",
    "tab_basic": "基本設定",
    "tab_assets": "附加資源",
    "tab_advanced": "進階選項",
    "tab_logs": "日誌輸出",

    # ---- Groups / Sections ----
    "group_script_settings": "腳本與輸出",
    "group_build_options": "建置選項",
    "group_data": "附加資料（檔案/目錄）",
    "group_hidden_imports": "隱藏匯入（hiddenimports）",
    "group_excludes": "排除模組（excludes）",
    "group_hooks_dir": "額外 hooks 目錄（--additional-hooks-dir）",
    "group_runtime_hooks": "執行時 hooks（--runtime-hook）",
    "group_upx_exclude": "UPX 排除（--upx-exclude）",
    "group_other_switches": "其他開關",

    # ---- Labels / Inputs ----
    "label_main_script": "主腳本 (.py)：",
    "label_output_name": "輸出名稱：",
    "label_output_dir": "輸出目錄：",
    "label_pack_mode": "打包模式：",
    "radio_onefile": "單檔（-F）",
    "radio_onedir": "目錄模式（-D）",
    "label_console": "執行方式：",
    "radio_console": "主控台（-c）",
    "radio_windowed": "視窗（-w）",
    "label_app_icon": "應用圖示 (.ico)：",
    "label_version_file": "版本資訊檔：",

    # UPX
    "check_use_upx": "使用 UPX 壓縮",
    "check_upx_internal": "使用 PyInstaller 內建 UPX",
    "label_upx_level": "UPX 壓縮等級（外壓）：",
    "check_upx_force": "使用 --force（外壓）",
    "check_upx_only_libs": "僅壓 DLL/PYD，不壓主 EXE（僅目錄模式）",

    # Debug
    "label_debug_level": "除錯等級（--debug）：",
    "debug_off": "關閉",
    "debug_all": "all",
    "debug_imports": "imports",
    "debug_noarchive": "noarchive",

    # Advanced
    "label_runtime_tmpdir": "執行時暫存目錄（--runtime-tmpdir）：",
    "label_extra_args": "額外命令列參數：",

    # Buttons
    "btn_browse": "瀏覽…",
    "btn_browse_file": "選檔",
    "btn_browse_dir": "選目錄",
    "btn_add": "新增",
    "btn_clear": "清空",
    "btn_build": "開始建置",
    "btn_clean_tmp": "清理暫存檔案",
    "btn_exit": "離開",
    "btn_cancel": "取消",

    # File dialogs / filters
    "title_select_resource_file": "選擇資源檔",
    "title_select_resource_dir": "選擇資源目錄",
    "title_select_version_file": "選擇版本資訊檔",
    "filter_py": "Python 腳本 (*.py)",
    "filter_ico": "圖示檔 (*.ico)",
    "filter_version": "版本檔 (*.txt;*.ver;*.version)",
    "filter_all": "所有檔案 (*.*)",

    # Tooltips
    "tip_main_script": "入口 .py 檔案路徑。例如：C:\\專案\\main.py。",
    "tip_browse_script": "選擇作為打包入口的 Python 腳本。",
    "tip_output_name": "生成之可執行檔/目錄名稱（對應 -n）。留白則使用腳本名。",
    "tip_distpath": "PyInstaller 輸出目錄（--distpath）。預設 dist/。",
    "tip_browse_dist": "選擇輸出目錄。",
    "tip_onefile": "單檔（-F）：所有相依打包成一個 EXE，啟動可能較慢。",
    "tip_onedir": "目錄（-D）：輸出資料夾，啟動較快；可搭配「僅壓 DLL/PYD」。",
    "tip_console": "主控台模式：保留主控台視窗，便於查看日誌與錯誤。",
    "tip_windowed": "視窗模式：無主控台，適合 GUI 程式。",
    "tip_icon": "應用圖示（.ico）。",
    "tip_browse_icon": "選擇 .ico 檔。",
    "tip_version_file": "版本資訊檔（--version-file）。常見為 *.txt / *.ver。",
    "tip_browse_version": "選擇版本資訊檔。",

    "tip_use_upx": "啟用 UPX 壓縮總開關。關閉後與 UPX 相關控件將停用。",
    "tip_upx_internal": "使用 PyInstaller 內建 UPX（若可用）。啟用後將不進行外部 UPX 後處理。",
    "tip_upx_level": "外部 UPX 壓縮等級 1–10（越高壓縮越強，耗時更久）。",
    "tip_upx_force": "對啟用 CFG/GuardCF 的 PE 強制壓縮（可能導致無法執行，請慎用）。",
    "tip_upx_only_libs": "僅在目錄模式（-D）可見，位於「使用 --force」右側。啟用後只壓 DLL/PYD，略過主 EXE。",

    "tip_debug": "選擇 PyInstaller 的 --debug 選項；一般建議保持「關閉」。",
    "tip_data_add": "輸入 ‘來源|目標’ 或 ‘來源=>目標’，例如：assets|assets 或 data\\cfg=>cfg。",
    "tip_browse_res_file": "選擇要打包的資源檔並填入輸入框。",
    "tip_browse_res_dir": "選擇要打包的資源目錄並填入輸入框。",
    "tip_add_res": "將上方輸入的資源條目加入列表。",
    "tip_clear_res": "清空資源列表。",
    "tip_data_list": "將以 --add-data 方式加入建置（來源→目標）。",

    "tip_hidden_imports": "缺少隱式匯入時填寫模組名，例如：PyQt5.sip。",
    "tip_add_hidden": "將上方模組名加入隱藏匯入列表。",
    "tip_clear_hidden": "清空隱藏匯入列表。",
    "tip_hidden_list": "打包時為每一項附加 --hidden-import。",

    "tip_excludes": "需要從建置中排除的模組名，例如：tkinter, tests。",
    "tip_add_exclude": "將上方模組名加入排除列表。",
    "tip_clear_exclude": "清空排除列表。",
    "tip_excludes_list": "打包時為每一項附加 --exclude-module。",

    "tip_hooks_dir": "額外 hooks 目錄路徑（放置 hook-*.py）。",
    "tip_add_hooks_dir": "加入 hooks 目錄到列表。",
    "tip_clear_hooks_dir": "清空 hooks 目錄列表。",
    "tip_hooks_list": "打包時為每一項附加 --additional-hooks-dir。",

    "tip_runtime_hook": "執行時 hook 腳本路徑（程式啟動時會執行）。",
    "tip_add_runtime_hook": "加入執行時 hook 到列表。",
    "tip_clear_runtime_hook": "清空執行時 hook 列表。",
    "tip_runtime_list": "打包時為每一項附加 --runtime-hook。",

    "tip_upx_exclude": "外部 UPX 時要排除的檔名或模式，例如：*.dll 或 vcruntime*.dll。",
    "tip_add_upx_exclude": "將上方模式加入 UPX 排除列表。",
    "tip_clear_upx_exclude": "清空 UPX 排除列表。",
    "tip_upx_excl_list": "外部 UPX 壓縮時，匹配的檔案會被略過。",

    "tip_disable_windowed_tb": "視窗模式下停用 Tk 的視窗化回溯，改為輸出到日誌。",

    "tip_runtime_tmpdir": "指定解壓時使用的暫存目錄（--runtime-tmpdir）。例如：C:\\Temp\\myapp。",
    "tip_extra_args": "其他 PyInstaller 參數，以空白分隔。例如：--collect-data 套件 --clean。",

    "tip_btn_build": "開始執行打包流程。",
    "tip_btn_clean": "刪除 build/、__pycache__、.spec 等暫存產物。",
    "tip_btn_exit": "離開程式。",

    # ---- Notes / Version conditional ----
    "check_win_no_prefer_redirects": "win-no-prefer-redirects",
    "check_win_private_assemblies": "win-private-assemblies",
    "note_winsxs_removed": "提示：在 PyInstaller 6+ 中，WinSxS 相關選項已移除。",

    # ---- Errors / Warnings / Logs ----
    "title_error": "錯誤",
    "error_select_script": "請先選擇主腳本（.py）。",
    "warn_icon_missing": "圖示檔不存在：{path}",
    "warn_version_missing": "版本資訊檔不存在：{path}",
    "err_extra_args": "額外參數解析失敗：{err}",
    "err_script_missing": "入口腳本不存在：{path}",

    "log_ready": "環境就緒。",
    "log_select_script": "請先選擇主腳本再開始建置。",
    "log_full_cmd": "完整命令：",
    "log_start_build": "開始建置...",
    "log_building": "正在執行 PyInstaller 建置，請稍候…",
    "log_build_success": "建置完成",
    "log_output_dir": "輸出目錄：{path}",
    "log_open_dir_failed": "嘗試開啟輸出目錄失敗：{err}",
    "log_build_failed": "建置失敗，返回碼：{code}",
    "log_cleaning": "正在清理暫存檔與快取…",
    "log_deleted": "已刪除：{name}",
    "log_clean_done": "清理完成。",
    "log_clean_error": "清理失敗：{err}",
    "log_only_libs_hint_singlefile": "已啟用「僅壓 DLL/PYD」，但目前為單檔模式（-F），此設定不會生效。",

    "msg_tip_windowed": "提示：視窗模式（-w）下異常可能不顯示堆疊，請考慮啟用「停用視窗化回溯」或改用主控台模式（-c）。",

    # ---- UPX availability / messages ----
    "upx_not_found_try_install": "未偵測到 upx，正在嘗試以 pip 安裝 Python 套件「upx」…",
    "upx_unavailable_disable": "upx 仍不可用，將略過外部 UPX 壓縮。",
    "upx_installed_ok": "upx 安裝完成。",
    "upx_added_to_path": "已將 upx 所在目錄加入 PATH：{path}",
    "upx_cfg_unsupported_skip": "[UPX] 略過（CFG/GuardCF）：{name}（啟用 GUARD_CF 的 PE 目前不受支援）",
    "upx_cfg_hint_enable_force": "提示：如必須壓縮，可在基本設定勾選「使用 --force」後重試（有風險，可能導致程式無法執行）。",

    # ---- PyInstaller installation flow ----
    "ask_install_pyinstaller_title": "安裝 PyInstaller？",
    "ask_install_pyinstaller": "未偵測到 PyInstaller。本工具仰賴 PyInstaller 打包可執行檔；若不安裝將無法使用。是否現在自動安裝？（需網路）",
    "msg_dependency_required": "本工具依賴 PyInstaller，未安裝將無法使用。",
    "msg_install_failed": "安裝 PyInstaller 失敗或無法匯入。",
    "install_window_title": "正在安裝 PyInstaller",
    "install_progress_label_wait": "正在安裝 PyInstaller（視窗將自動關閉）。速度取決於網路，請耐心等待…",
}
