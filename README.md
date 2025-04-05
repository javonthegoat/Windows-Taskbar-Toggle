# Windows Taskbar Auto-Hide Toggle Script

A simple Python script to manually toggle the Windows taskbar "Automatically hide the taskbar" setting using a global hotkey (`Ctrl+Alt+T` by default). This allows you to quickly reclaim screen space when needed and bring the taskbar back just as easily, without needing to go into Windows settings each time.

## Features

*   Toggles the actual Windows taskbar auto-hide setting on/off.
*   Uses a configurable global hotkey.
*   Helps maximize screen real estate for applications or a cleaner desktop view.
*   Runs discreetly in the background via the terminal.

## Requirements

*   **Operating System:** Windows (Uses Windows-specific API calls)
*   **Python:** Version 3.x recommended
*   **Python Libraries:**
    *   `keyboard` (for global hotkey detection)

## Installation

1.  **Clone or Download:**
    *   Clone the repository:
        ```bash
        git clone https://github.com/javonthegoat/Windows-Taskbar-Toggle.git
        ```
    *   Or download the ZIP file from the GitHub page and extract it.

2.  **Navigate to Folder:**
    Open a terminal (Command Prompt, PowerShell, Git Bash, VS Code Terminal) and change directory into the project folder:
    ```bash
    cd path/to/Windows-Taskbar-Toggle
    ```

3.  **Set up Virtual Environment (Recommended):**
    *   Create a virtual environment:
        ```bash
        python -m venv venv
        ```
    *   Activate the virtual environment:
        *   Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
        *   Windows (Command Prompt): `.\venv\Scripts\activate.bat`
        *   macOS/Linux (Bash/Zsh): `source venv/bin/activate`

4.  **Install Dependencies:**
    With the virtual environment active, install the required library:
    ```bash
    pip install keyboard
    ```

## Usage

1.  **Run the Script:**
    *   Make sure your virtual environment is activated (you should see `(venv)` in your terminal prompt).
    *   **Important:** You might need to run this script with **Administrator privileges** (not required) for it to reliably detect global hotkeys and modify system settings. To do this, open your terminal (PowerShell/Command Prompt) "As Administrator", navigate to the project folder, activate the virtual environment, and then run the script.
    *   Execute the script:
        ```bash
        python manually_hide_taskbar_autohide.py
        ```

2.  **Toggle the Taskbar:**
    *   The script will print "Listening for hotkey..." and run in the background.
    *   Press the configured hotkey (`Ctrl+Alt+T` by default). The taskbar should toggle between being always visible and automatically hiding.

3.  **Stop the Script:**
    *   Go back to the terminal window where the script is running and press `Ctrl+C`.

## Configuration

*   **Hotkey:** The hotkey can be changed by editing the `HOTKEY` variable near the top of the `manually_hide_taskbar.py` script file. Follow the format expected by the `keyboard` library (e.g., `'win+shift+h'`, `'f9'`).

## Notes & Troubleshooting

*   **Administrator Privileges:** As mentioned, running as Administrator often solves issues with the hotkey not being detected or the taskbar state not changing.
*   **Windows Only:** This script will not work on macOS or Linux.
*   **Hotkey Conflicts:** Ensure the hotkey you choose doesn't conflict with other applications or system shortcuts.

## License

(Optional - You can choose a license if you want)

*   You can add a license file (e.g., `LICENSE`) and state the license here. The [MIT License](https://opensource.org/licenses/MIT) is a common and permissive choice for small projects like this. Example text:
    ```markdown
    This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
    ```
*   If you don't add a license, standard copyright laws apply by default.