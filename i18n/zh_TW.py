# i18n/zh_TW.py
# -*- coding: utf-8 -*-
STRINGS = {
    "app_title": "PyInstaller 快速打包工具",
    "tab_basic": "基本設定",
    "tab_assets": "資源與匯入",
    "tab_advanced": "進階選項",
    "tab_logs": "日誌",

    "group_script_settings": "腳本設定",
    "group_build_options": "打包選項",
    "group_data": "附加資源檔（來源路徑:目標路徑）",
    "group_binaries": "附加二進位（來源路徑:目標路徑）",
    "group_hidden_imports": "隱藏匯入模組",
    "group_excludes": "排除模組",
    "group_hooks_dir": "額外 Hooks 目錄",
    "group_runtime_hooks": "執行時 Hook 檔",
    "group_upx_exclude": "UPX 排除（模式）",
    "group_other_switches": "其他開關",

    "label_main_script": "主腳本檔:",
    "label_output_name": "輸出名稱:",
    "label_output_dir": "輸出目錄:",
    "label_pack_mode": "打包模式:",
    "label_console": "主控台:",
    "label_app_icon": "應用程式圖示:",
    "label_version_file": "版本資訊檔:",
    "label_debug_level": "偵錯等級:",
    "label_runtime_tmpdir": "執行時暫存目錄 (--runtime-tmpdir)",
    "label_extra_args": "額外命令列參數:",
    "label_upx_level": "UPX 壓縮等級",

    "radio_onefile": "單檔模式 (-F)",
    "radio_onedir": "目錄模式 (-D)",
    "radio_console": "顯示主控台 (-c)",
    "radio_windowed": "無主控台 (-w)",

    "check_use_upx": "使用 UPX 壓縮（建議）",
    "check_upx_force": "使用 --force（可能導致無法執行）",
    "check_upx_internal": "使用 PyInstaller 內建 UPX",
    "check_noarchive": "停用封存 (--noarchive)",
    "check_disable_windowed_tb": "停用視窗化回溯視窗 (--disable-windowed-traceback)",
    "check_win_no_prefer_redirects": "win-no-prefer-redirects",
    "check_win_private_assemblies": "win-private-assemblies",

    "debug_off": "關閉",
    "debug_all": "all",
    "debug_imports": "imports",
    "debug_noarchive": "noarchive",

    "btn_browse": "瀏覽...",
    "btn_add": "新增",
    "btn_clear": "清除",
    "btn_build": "開始建置",
    "btn_clean": "清理專案",
    "btn_clean_tmp": "清理暫存檔案",
    "btn_exit": "離開",

    "btn_browse_file": "選擇檔案",
    "btn_browse_dir": "選擇目錄",

    "title_select_version_file": "選擇版本資訊檔",
    "title_select_resource_file": "選擇資源檔",
    "title_select_resource_dir": "選擇資源目錄",

    "filter_py": "Python 腳本",
    "filter_all": "所有檔案",
    "filter_ico": "圖示檔",
    "filter_version": "版本資訊檔",

    "title_error": "錯誤",
    "error_select_script": "請選擇要打包的 Python 腳本",

    "warn_icon_missing": "警告: 圖示檔不存在，已忽略 - {path}",
    "warn_version_missing": "警告: 版本資訊檔不存在，已忽略 - {path}",

    "err_extra_args": "錯誤: 無法解析額外參數 - {err}",
    "err_script_missing": "錯誤: 腳本檔不存在 - {path}",

    "log_ready": "PyInstaller GUI 打包工具已就緒",
    "log_select_script": "請選擇 Python 腳本並配置打包選項",
    "log_building": "打包中...",
    "log_start_build": "開始打包流程...",
    "log_build_success": "打包成功完成!",
    "log_output_dir": "輸出目錄: {path}",
    "log_open_dir_failed": "開啟輸出目錄失敗: {err}",
    "log_build_failed": "打包失敗! 錯誤代碼: {code}",
    "log_full_cmd": "完整命令列表:",

    "msg_tip_windowed": "提示：目前為無主控台模式，若執行期發生例外將以視窗顯示回溯。",

    "log_cleaning": "清理建置檔案...",
    "log_deleted": "已刪除: {name}",
    "log_clean_done": "清理完成",
    "log_clean_error": "清理時發生錯誤: {err}",

    "upx_not_found_try_install": "未偵測到 UPX，嘗試自動安裝：pip install upx",
    "upx_installed_ok": "UPX 安裝成功，已可用。",
    "upx_added_to_path": "已定位並加入 UPX 至 PATH: {path}",
    "upx_unavailable_disable": "無法自動配置 UPX，將停用 UPX 壓縮（等同 --noupx）。",

    # 懸停提示（精簡說明 + 小範例）
    "tip_main_script": "選擇入口 .py 腳本。例：main.py。更換後將自動以檔名作為輸出名預設值。",
    "tip_browse_script": "瀏覽並選擇入口腳本（如 src/app.py）。",
    "tip_output_name": "可留白以使用腳本檔名。例：MyApp、工具箱。",
    "tip_distpath": "建置產物輸出目錄（預設 dist）。例：D:\\builds\\MyApp。",
    "tip_browse_dist": "瀏覽並選擇輸出目錄（不存在將自動建立）。",
    "tip_icon": "可選 .ico 圖示（僅 Windows 生效）。例：assets\\app.ico。",
    "tip_browse_icon": "瀏覽 .ico 圖示檔；可用線上工具由 png 轉 .ico。",
    "tip_version_file": "供 --version-file 使用的資訊檔，可含公司/版本等中繼資料。",
    "tip_browse_version": "選擇 version 檔（如 version.txt / version.ini）。",

    "tip_onefile": "單檔可執行；啟動時解壓至暫存目錄，體積較大、啟動較慢。",
    "tip_onedir": "輸出到資料夾；啟動較快、易於除錯，發布時整個資料夾一併複製。",
    "tip_console": "顯示主控台視窗，適合 CLI 或需查看 print/log 的程式。",
    "tip_windowed": "隱藏主控台，適合 GUI 程式。例外回溯將以視窗顯示。",

    "tip_use_upx": "建置成功後使用 UPX 壓縮輸出檔（外壓）。",
    "tip_upx_force": "僅用於外壓：對不受支援的 PE（如啟用 CFG）強行壓縮。高風險，可能導致無法執行。",
    "tip_upx_internal": "由 PyInstaller 內建流程呼叫 UPX（較保守，可能跳過主 EXE，特別是啟用 CFG 時）。選擇後將停用等級滑桿與 --force。",
    "tip_upx_level": "UPX 等級 1–9：1=最快/壓縮弱；9=最小/最慢。建議 5~7。",
    "tip_debug": "PyInstaller 偵錯：imports=列印匯入；noarchive=不打包封存；all=更詳細。",

    "hint_resources_input": "輸入後點「新增」。支援：來源（檔案/目錄），或 來源|目標 指定封裝內相對路徑。\n例：assets|assets   C:\\img\\logo.png|images\\logo.png",

    "tip_data_add": "將額外檔案/目錄打入封裝。例：data|data、config.json|cfg\\config.json。",
    "tip_browse_res_file": "選擇要打包的資源檔（如圖片、設定等）。",
    "tip_browse_res_dir": "選擇要打包的資源目錄（會以相同目錄名放入封裝）。",
    "tip_add_res": "把上方路徑加入資源清單（支援 來源|目標）。",
    "tip_clear_res": "清空資源清單。",
    "tip_data_list": "已新增的資源對映（來源 → 目標）。",

    "tip_hidden_imports": "顯式宣告匯入不到的模組。例：pkg.submod。",
    "tip_add_hidden": "新增一個隱藏匯入（Enter 後可繼續新增）。",
    "tip_clear_hidden": "清空隱藏匯入清單。",
    "tip_hidden_list": "將以 --hidden-import 傳給 PyInstaller 的模組。",

    "tip_excludes": "打包時要排除的模組。例：tkinter、torch.tests。",
    "tip_add_exclude": "新增一個排除模組（支援套件或子模組）。",
    "tip_clear_exclude": "清空排除模組清單。",
    "tip_excludes_list": "將以 --exclude-module 排除的模組。",

    "tip_hooks_dir": "額外 hooks 搜尋目錄（內含 hook-*.py），適用自訂收集邏輯。",
    "tip_add_hooks_dir": "新增 hooks 目錄。",
    "tip_clear_hooks_dir": "清空 hooks 目錄清單。",
    "tip_hooks_list": "已新增的 hooks 目錄。",

    "tip_runtime_hook": "啟動時先執行的腳本（調整環境變數、搜尋路徑等）。例：fix_paths.py。",
    "tip_add_runtime_hook": "新增一個 runtime hook 檔。",
    "tip_clear_runtime_hook": "清空 runtime hook 清單。",
    "tip_runtime_list": "已新增的 runtime hooks。",

    "tip_upx_exclude": "避免特定檔案被 UPX。支援萬用字元：*.dll、*_debug.pyd。",
    "tip_add_upx_exclude": "新增一條 UPX 排除模式。",
    "tip_clear_upx_exclude": "清空 UPX 排除清單。",
    "tip_upx_excl_list": "UPX 將跳過這些匹配的檔案。",

    "tip_disable_windowed_tb": "Windowed 下停用回溯視窗（例外將不再以視窗顯示）。",
    "tip_runtime_tmpdir": "one-file 模式解壓與執行用的暫存目錄。可自訂到可寫位置。\n例：%TEMP%\\myapp 或 D:\\tmp\\myapp。",
    "tip_extra_args": "直接傳給 PyInstaller 的原始參數。\n例：--collect-all pkg --paths C:\\py\\libs。\n注意：--add-data 在 Windows 用「來源;目標」，Linux/macOS 用「來源:目標」。",

    "tip_btn_build": "開始建置（自動切換到「日誌」檢視輸出）。",
    "tip_btn_clean": "刪除 build、同名 .spec、__pycache__ 等暫存檔。",
    "tip_btn_exit": "離開程式。",

    "note_winsxs_removed": "提示：PyInstaller 6 起已移除 WinSxS 相關參數。",

    "upx_cfg_unsupported_skip": "[UPX] 跳過（CFG/GuardCF）：{name}（啟用 GUARD_CF 的 PE 目前不受支援）",
    "upx_cfg_hint_exclude": "提示：將該檔名或匹配模式加入「UPX 排除（模式）」，之後不再嘗試壓縮；若必須壓縮，可手動使用 --force（有風險，可能導致無法執行）。",
    "upx_cfg_hint_enable_force": "提示：若確認需要強行壓縮，可在「基本設定」勾選「使用 --force（可能導致無法執行）」後重新建置。",
}
