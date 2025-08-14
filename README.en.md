## 英文版 README.en.md

```markdown
# PyInstaller GUI Packaging Tool

This is a Python-based graphical user interface tool for quickly packaging Python scripts using PyInstaller. It allows users to configure common packaging options through a simple interface without having to remember complex command-line arguments.

## Features

- **Improved user interface**: Single-column layout design with overall scrollbar and mouse wheel support for a better user experience.
- **Common options**:
  - Support for one-file packaging (-F) and directory packaging (-D).
  - Console window settings (show console or no console).
  - Set the icon for the generated executable (-i).
  - Custom output directory (--distpath).
  - Custom output filename (-n).
- **Resource management**: Add additional data files (--add-data) and binary files (--add-binary).
- **Real-time logging**: Real-time output display during the packaging process for easy debugging.
- **Cleanup function**: One-click cleanup of temporary build files (build directory, spec files, etc.).
- **UPX support**: UPX compression enabled by default, can be manually disabled.

## Installation

1. Ensure Python (recommended Python 3.8+) is installed.
2. Install PyInstaller:
   ```bash
   pip install pyinstaller
Download the PyInstallerGUI.py file from this repository.
Using Precompiled Version (for Windows)
We provide a precompiled executable that does not require a Python environment:

Visit the releases page to download PyInstallerGUI.exe.
Double-click to run.
Usage
​​Run the program​​:
If using the Python script:
python PyInstallerGUI.py
If using the precompiled version, double-click PyInstallerGUI.exe.
​​Configure packaging options​​:
Click the "Browse" button to select the Python script (.py file) to package.
Set the output name (optional, default is the script filename).
Set the output directory (optional, default is the dist folder in the current directory).
Select packaging mode:
​​One-file mode​​: Generates a single executable file (.exe).
​​Directory mode​​: Generates a directory containing the executable and dependent files.
Console options:
​​Show console​​: Suitable for command-line programs.
​​No console​​: Suitable for GUI programs (e.g., pygame, PyQt).
Click the "Browse" button next to the icon to select an icon file (.ico format, optional).
(Optional) Add data files (e.g., images, config files) in the advanced options, in the format source:destination.
(Optional) Enter other PyInstaller supported arguments in the "Extra command line arguments" field.
​​Start packaging​​:
Click the "Start Build" button and wait for the process to complete.
Monitor the real-time output in the log area at the bottom.
​​Get the output​​:
After successful packaging, find the generated executable in the output directory.
​​Clean project​​:
After packaging, you can click the "Clean Project" button to remove temporary files.
Notes
The packaging process may take several minutes, depending on the size and complexity of the project.
Ensure that any additional files (e.g., icons, data files) have correct paths.
Programs packaged in one-file mode have a longer startup time (due to extraction to a temporary directory).
If packaging fails, check the log output for error information.
FAQ
Why is the packaged program so large?
PyInstaller includes the Python interpreter and all dependency libraries. This is normal. To reduce the size:

Use UPX compression (enabled by default in this tool).
Minimize the use of dependency libraries (avoid large libraries).
Use a virtual environment to avoid including unnecessary libraries.
Why doesn't the packaged program run on another computer?
The target machine may be missing necessary runtime environments (e.g., VC++ runtime libraries). Try:

Installing the appropriate runtime environment on the target machine (e.g., Microsoft Visual C++ Redistributable).
If missing specific files, try adding them using --add-data.
Why is the program detected as a virus?
Due to PyInstaller's packaging mechanism, the generated executable may sometimes be falsely flagged by antivirus software. You can:

Submit a false positive report to the antivirus vendor.
Code-sign the generated executable (requires purchasing a digital certificate).
Supported operating systems?
Currently developed and tested mainly on Windows, but core features should support cross-platform (macOS/Linux). Feedback for other platforms is welcome.
