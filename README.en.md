# PyInstaller GUI Packaging Tool

A Python-based graphical user interface for quickly packaging Python scripts with PyInstaller. Configure common options through an intuitive UI without memorizing complex CLI arguments.

## Features

- Easy to use： No command-line knowledge required.
- Common options：
  - One-file (-F) and one-folder (-D) packaging.
  - Console mode： show console or windowed (no console).
  - Set executable icon (-i).
  - Custom output directory (--distpath).
  - Custom output name (-n). When you select the main script， the name auto-fills to the script filename.
- Unified Additional Resources：
  - Add files or directories in one place.
  - Default placement：
    - Directories are placed as a same-named folder in the runtime temp root.
    - Files are placed directly in the runtime temp root (keeping original filename).
  - Custom destination mapping：
    - Use “source|dest” or “source＝>dest” (e.g.， C：\\data\\assets|res or images\\logo.png|res\\img).
- Real-time logging：
  - Live output during build.
  - Automatically switches to the Logs tab after starting the build.
  - Opens the output directory on success.
- Cleanup：
  - One-click removal of build artifacts (build folder， spec file， _ _pycache_ _， etc.).
- UPX support with adjustable level：
  - Slider from 1–10 (10 is treated as 9).
  - Performed as a post-build step to avoid conflicts with PyInstaller’s built-in UPX (we force --noupx in the build command).
  - Auto-detects／installs UPX when possible； gracefully skips with a log note if unavailable.
  - Supports an exclude list (filenames or patterns) to skip specific binaries.
- Compatibility adjustments：
  - Automatically detects the local PyInstaller version.
  - Windows WinSxS options are only shown when PyInstaller ＜ 6.0 (these options were removed in v6+).
  - Removed the standalone --noarchive switch； the Debug level still supports “noarchive” via -d noarchive.

## Installation

1. Ensure Python is installed (recommended Python 3.8+).
2. Install PyInstaller：
  ```bash
  pip install pyinstaller
  ```
3. Download and run the GUI tool from this repository， or use the precompiled version (Windows).

Using the precompiled version (Windows)：
- Download the .exe from the Releases page.
- Double-click to run (no Python environment required).

## Usage

Run the program
- Python script：
  ```bash
  python ＜your_gui_script>.py
  ```
- Precompiled version： double-click the .exe.

Configure build options
- Click “Browse” to choose the Python script (.py). Output name auto-fills with the script filename (you can edit it).
- Set output directory (optional)， default is dist in the current directory.
- Select packaging mode：
  - One-file： produces a single executable (.exe).
  - One-folder： produces a folder with the executable and dependencies.
- Console options：
  - Show console： for CLI apps.
  - No console： for GUI apps (e.g.， pygame， PyQt).
- Icon： click “Browse” next to Icon to select a .ico file (optional).

Additional resources
- Enter a source path (file or directory) and click “Add”：
  - Directories become same-named folders at runtime temp root.
  - Files go directly under the runtime temp root (keep filename).
- Custom destination examples：
  - C：\\data\\assets|res
  - images\\logo.png|res\\img
  - Also supports “＝>”： src＝>dest
- You can still add any extra PyInstaller arguments in “Extra arguments” (e.g.， more --add-data).

UPX compression
- Choose a level 1–10 (default 5； 10 acts as 9).
- After a successful build， the tool runs UPX compression； if UPX is not found， it attempts installation or logs a skip.
- Add patterns to the “UPX exclude” list to skip specific files (e.g.， *.dll).

Start build
- Click “Start Build”； the UI switches to the Logs tab to show real-time output.
- On success， the output directory is opened.

Clean project
- Click “Clean Project” to remove build， spec， and _ _pycache_ _.

## Notes

- Build time depends on project size and dependencies. One-file mode has longer startup due to extraction to a temp directory.
- Ensure paths for any additional files are correct.
- WinSxS-related options on Windows appear only when PyInstaller ＜ 6.0 (removed in v6+).

## FAQ

Why is the packaged program large？
- PyInstaller bundles the Python interpreter and all dependencies. To reduce size：
  - Use UPX compression (enabled here with adjustable level).
  - Trim unnecessary dependencies.
  - Build in a virtual environment to avoid bundling unrelated packages.

Why doesn’t the packaged program run on another computer？
- The target machine may lack required runtimes (e.g.， VC++). Try：
  - Installing Microsoft Visual C++ Redistributable.
  - Adding missing files via --add-data.

Why is the program flagged by antivirus？
- Packaged executables can be false-flagged. Consider：
  - Submitting a false-positive report.
  - Code-signing the executable (requires a certificate).

Supported operating systems？
- Primarily developed and tested on Windows； core features should work cross-platform (macOS／Linux). Feedback is welcome.
