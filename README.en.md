PyInstaller GUI Packaging Tool
This is a Python-based graphical user interface tool for quickly packaging Python scripts using PyInstaller. It allows users to configure common packaging options through a simple interface without having to remember complex command-line arguments.

Features
​​Easy to use​​: Intuitive graphical interface, no command-line knowledge required
​​Common options​​: Support for single-file package, directory package, console window settings
​​Icon setting​​: Customize the application icon
​​Resource management​​: Add additional data and binary files
​​Real-time logging​​: Display output during packaging process
​​Cleanup function​​: One-click removal of temporary files

Installation
Ensure Python is installed (recommended Python 3.8+)
Install dependencies:
pip install pyinstaller
Download the repository or copy the PyInstallerGUI.py file
Using Pre-compiled Version (No Installation)
For Windows users, you can directly use the pre-compiled executable:

Download PyInstallerGUI.exe from Releases page
Usage
Run the program:
python PyInstallerGUI.py
Or simply double-click PyInstallerGUI.exe
In the interface:
Select the Python script to package
Set output name and output directory
Choose packaging mode (Single File/Directory)
Select console option (Show/Hide)
Set application icon (optional)
Add additional resource files (optional)
Click "Start Build" button
After packaging completes, find the generated executable in the output directory
Notes
Packaging may take several minutes depending on project size
Ensure any additional files (icons, data files) have correct paths
Programs packaged in single-file mode have longer startup time
If packaging fails, check log output for error information
FAQ
Why is the packaged program so large?
PyInstaller packages include the Python interpreter and dependencies, which is normal
To reduce size:

Use UPX compression (enabled by default)
Minimize dependency usage
Package in a virtual environment
Why doesn't the packaged program run on other computers?
This may be due to missing runtime dependencies (e.g., VC++ runtime)
Try:

Installing necessary runtime environments on target machines
Adding missing dependency files to resources
Why is my program flagged as a virus?
PyInstaller-packaged programs are sometimes falsely flagged
Try:

Reporting false positives to antivirus vendors
Digitally signing the program with a certificate
Is cross-platform supported?
Core features support cross-platform (Windows/macOS/Linux) though some options are platform-specific:

Windows: Icons and console-less mode supported
macOS: Supports creating .app bundles
Linux: Basic packaging functionality supported
