# PyInstaller GUI Pack Tool

A Python GUI to build executables with PyInstaller quickly.Configure common options via an intuitive interface-no need to memorize CLI flags.Ships with localized tooltips(i18n,auto-detected,single-language display)and High-DPI awareness.

---

## Features

- Easy to use:no CLI knowledge required.  
- Common build options:  
 - One-file(-F)/ One-dir(-D)  
 - Console:Console/Windowed(-w)  
 - Icon(-i),Output dir(--distpath),Output name(-n,auto-filled from main script)  
- Unified additional data input:  
 - Add files or folders in one place;default rule:folder → copied under the same folder name;file → copied to temp root(keep filename)  
 - Custom mapping:`src|dest` or `src=>dest`(e.g. `C:\data\assets|res`,`images\logo.png|res\img`)  
- UPX compression(post-processing):  
 - Level 1-10(10 treated as 9),run after build(build command always uses `--noupx` to avoid conflicts)  
 - Auto detect/install UPX;if unavailable,log and skip  
 - Support exclude list(file names or globs,e.g. `*.dll`,`*_debug.pyd`)  
- Localization(i18n)& tooltips:  
 - Auto detect system language;show a single language(currently `zh_CN/zh_TW/en_US`,extensible)  
 - Concise explanations+tiny examples for major controls:  
  - Runtime temp dir:one-file extraction/run dir(e.g. `%TEMP%\myapp`,`D:\tmp\myapp`)  
  - Extra CLI args:passed through to PyInstaller(e.g. `--collect-all pkg --paths C:\py\libs`;note `--add-data` uses `src;dest` on Windows and `src:dest` on Linux/macOS)  
- Compatibility&conditional UI:  
 - Detect local PyInstaller;only show WinSxS options when PyInstaller < 6.0(removed since v6)  
- High-DPI(Windows):  
 - Enable Per-Monitor V2 before Tk;sync `tk scaling` after creating Tk  
- Live logs:  
 - Realtime output;auto-switch to “Logs” tab;open output directory on success  
 - Dark background log view  
- Clean temp files:  
 - One click to remove `build/`,same-name `.spec`,and `__pycache__/`

---

## Install

1. Install Python(3.8+ recommended)  
2. Install PyInstaller:  
 `pip install pyinstaller`  
3. Run the GUI script from repo;or use the prebuilt exe(Windows)

---

## Usage

1. Run  
 `python PyInstaller打包工具.py`  
 or double-click the prebuilt .exe

2. Basics  
 - Choose main script(output name auto-filled;editable)  
 - Output dir(default `dist`)  
 - Packaging mode:one-file(extracts at runtime;bigger/slower start)/one-dir(faster start)  
 - Console options:Console/Windowed(exceptions shown in a message box)

3. Additional data  
 - Enter source path(file/folder),click Add  
 - Custom mapping:`src|dest` or `src=>dest`  
  Examples:  
  - `assets|assets`  
  - `C:\img\logo.png|images\logo.png`

4. UPX  
 - Tick “Use UPX compression(recommended)”  
 - Choose level via slider(1=fastest/least compression;9=smallest/slowest;10 treated as 9)  
 - Add patterns to “UPX exclude(pattern)” if needed(e.g. `*.dll`,`*_debug.pyd`)

5. Advanced(optional)  
 - Hidden imports(--hidden-import),excludes(--exclude-module)  
 - Extra hooks dirs,runtime hooks  
 - Runtime temp dir(--runtime-tmpdir):e.g. `%TEMP%\myapp`,`D:\tmp\myapp`  
 - Extra CLI args:passed to PyInstaller(e.g. `--collect-all pkg --paths C:\py\libs`)  
  > Note:`--add-data` uses `src;dest` on Windows,and `src:dest` on Linux/macOS

6. Build/Clean temp/Exit  
 - “Build”:auto switches to Logs;opens output dir on success  
 - “Clean temp files”:remove `build/`,same-name `.spec`,and `__pycache__/`  
	- “Exit”:quit app

---

## i18n extension

- Provided `zh_CN.py`,`zh_TW.py`,`en_US.py`.  
- To add a new locale:copy `en_US.py` to a new file(e.g. `ja_JP.py`)and translate keys;no app changes needed.  
- Tooltip keys start with `tip_*`(e.g. `tip_runtime_tmpdir`,`tip_extra_args`).

---

## Notes on compatibility

- PyInstaller 6+:WinSxS flags removed;UI shows them only when version < 6.0.  
- UPX:the app will try to install/configure;if it fails,it will log and skip.  
- High-DPI:enable Per-Monitor V2 on Windows and call `tk scaling` after Tk init.

---

## Changes since previous version

- Added:full set of localized tooltips(single language,with tiny examples)  
- Added:two previously missing tooltips-runtime temp dir,extra CLI args  
- Added:High-DPI awareness and `tk scaling` sync  
- Improved:UPX as post-processing(build always uses `--noupx`)  
- Kept:original UI layout/control positions;UPX slider remains un-tickmarked `ttk.Scale` with a numeric label on the right  
- Rename:“Clean” → “Clean temp files”  
- Conditional:WinSxS options shown only when PyInstaller < 6
