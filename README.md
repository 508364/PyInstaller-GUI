# PyInstaller GUI 打包工具

一個基於 Python 的圖形介面工具,用於快速以 PyInstaller 打包 Python 腳本.透過直觀的 UI 配置常用選項,無需記憶複雜命令列參數.支援本地化懸停提示(i18n,依系統語言自動顯示單一語言)與高 DPI 感知.

---

## 功能特性

- 簡單易用:直觀 UI,無需命令列經驗.  
- 常用打包選項:  
 - 單檔(-F)/目錄(-D)  
 - 主控台:顯示主控台/無主控台(-w)  
 - 圖示(-i)、輸出目錄(--distpath)、輸出名稱(-n,選擇主腳本時自動填入腳本名)  
- 統一的附加資源入口:  
 - 一處新增檔案或目錄;預設規則:目錄 → 以同名資料夾放入執行期臨時根;檔案 → 直接放入臨時根(保留檔名)  
 - 自訂目標對映:支援 來源|目標 或 來源=>目標(例:C:\data\assets|res、images\logo.png|res\img)  
- UPX 壓縮(構建後處理):  
 - 等級 1~10(10按9處理),以後處理執行(構建命令固定 --noupx,避免衝突)  
 - 自動偵測/安裝 UPX;不可用則在日誌提示並跳過  
 - 支援排除清單(檔名或萬用字元,例:*.dll、*_debug.pyd)  
- 本地化(i18n)與懸停提示(Tooltip):  
 - 自動偵測系統語言,僅顯示單一語言(目前含 zh_CN/zh_TW/en_US,可擴充)  
 - 每個提示為「精簡說明+小範例」,覆蓋主要控制項:  
  - 執行時臨時目錄:one-file 解壓與執行目錄(例:%TEMP%\myapp、D:\tmp\myapp)  
  - 額外命令列參數:原樣傳給 PyInstaller(例:--collect-all pkg --paths C:\py\libs;注意 --add-data 在 Windows 用 src;dest,Linux/macOS 用 src:dest)  
- 相容性與條件顯示:  
 - 自動偵測本機 PyInstaller 版本;僅當 PyInstaller < 6.0 時顯示 WinSxS 相關選項(v6+已移除)  
- 高 DPI 感知(Windows):  
 - 啟動前啟用 Per-Monitor V2;建立 Tk 後依 DPI 同步 `tk scaling`  
- 即時日誌:  
 - 構建時即時輸出;按「開始構建」後自動切到「日誌」頁;成功後嘗試開啟輸出目錄  
 - 深色背景日誌視圖  
- 清理臨時檔案:  
 - 一鍵刪除 `build/`、腳本同名 `.spec`、`__pycache__/` 等

---

## 安裝

1. 安裝 Python(建議 3.8+)  
2. 安裝 PyInstaller:  
 `pip install pyinstaller`  
3. 執行倉庫中的 GUI 腳本;或使用預編譯版(Windows,雙擊 .exe)

---

## 使用方法

1. 執行程式  
 `python PyInstaller打包工具.py`  
 或雙擊預編譯 .exe

2. 基本配置  
 - 選擇主腳本(自動填充輸出名,可修改)  
 - 輸出目錄(預設 `dist`)  
 - 打包模式:單檔(啟動時會解壓,體積較大、啟動稍慢)/目錄(啟動較快)  
 - 主控台選項:顯示/隱藏(Windowed 模式例外以彈窗顯示)

3. 附加資源  
 - 輸入「來源(檔案/目錄)」後按「新增」  
 - 自訂目標:`來源|目標` 或 `來源=>目標`  
  範例:  
  - `assets|assets`  
	- `C:\img\logo.png|images\logo.png`

4. UPX 壓縮  
 - 勾選「使用 UPX 壓縮(推薦)」  
	- 透過滑桿選擇等級(1=最快/壓縮弱;9=最小/最慢;10 視為9)  
	- 如需排除特定檔案,於「UPX 排除(模式)」新增匹配(例:`*.dll`、`*_debug.pyd`)

5. 進階設定(可選)  
 - 隱藏匯入(--hidden-import)、排除模組(--exclude-module)  
 - 額外 hooks 目錄、runtime hook 檔  
 - 執行時臨時目錄(--runtime-tmpdir):如 `%TEMP%\myapp`、`D:\tmp\myapp`  
 - 額外命令列參數:直接傳給 PyInstaller(例:`--collect-all pkg --paths C:\py\libs`)  
  > 注意:`--add-data` 在 Windows 用 `來源;目標`,在 Linux/macOS 用 `來源:目標`

6. 開始構建/清理臨時檔案/退出  
 - 「開始構建」:自動切到「日誌」頁,成功後嘗試開啟輸出目錄  
 - 「清理臨時檔案」:刪除 `build/`、同名 `.spec`、`__pycache__/`  
 - 「退出」:關閉程式

---

## 本地化(i18n)擴充

- 目前提供 `zh_CN.py`、`zh_TW.py`、`en_US.py` 三份翻譯表.  
- 若需新增語言:複製 `en_US.py` 為新檔(如 `ja_JP.py`),翻譯所有鍵即可,主程式不需改動.  
- 懸停提示鍵以 `tip_*` 命名(如 `tip_runtime_tmpdir`、`tip_extra_args`).

---

## 相容性提示

- PyInstaller 6+:已移除 WinSxS 相關參數;GUI 僅在 < 6.0 時顯示對應選項.  
- UPX:程式會嘗試自動安裝與配置;若失敗將於日誌提示並跳過.  
- 高 DPI:Windows 下啟用 Per-Monitor V2,並在 Tk 建立後呼叫 `tk scaling`.

---

## 變更摘要(相對舊版)

- 新增:全量懸停提示(自動本地化、單語顯示;均含精簡範例)  
- 新增:兩處缺失提示 —— 執行時臨時目錄、額外命令列參數  
- 新增:高 DPI 感知與 `tk scaling` 同步  
- 優化:UPX 壓縮改為後處理(構建命令固定 `--noupx`)  
- 保持:UI 佈局與控制項位置與原版一致;UPX 滑桿仍為無刻度 `ttk.Scale`,右側獨立數字顯示等級  
- 調整:「清理」重命名為「清理臨時檔案」  
- 條件顯示:WinSxS 選項僅在 PyInstaller < 6 時出現
