# Filename: manually_hide_taskbar.py

import ctypes
import sys
import os
import time
from ctypes import wintypes

try:
    import keyboard
except ImportError:
    print("Error: The 'keyboard' library is not installed in your active environment.")
    print("Please activate your virtual environment ('venv\\Scripts\\Activate.ps1' or 'source venv/bin/activate')")
    print("and then run: pip install keyboard")
    sys.exit(1)

# --- Configuration ---
HOTKEY = 'ctrl+alt+t' # Your chosen keybind
# --------------------

# --- Windows API Setup ---
user32 = ctypes.windll.user32
shell32 = ctypes.windll.shell32

# Constants for SHAppBarMessage
ABM_GETSTATE = 4
ABM_SETSTATE = 10
ABS_AUTOHIDE = 1
ABS_ALWAYSONTOP = 2 # Note: We are only toggling AUTOHIDE

# APPBARDATA structure
class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", wintypes.RECT),
        ("lParam", wintypes.LPARAM),
    ]

FindWindowW = user32.FindWindowW
TASKBAR_CLASS = "Shell_TrayWnd"
# --- End Windows API Setup ---

def is_admin():
    """Checks if the script is running with administrator privileges."""
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return False
    except Exception as e:
        print(f"Could not check admin status: {e}")
        return False

def set_taskbar_state(autohide: bool, always_on_top: bool = False):
    """Sets the taskbar's AutoHide and AlwaysOnTop state."""
    hwnd_taskbar = FindWindowW(TASKBAR_CLASS, None)
    if not hwnd_taskbar:
        print(f"Error: Could not find the main taskbar window ('{TASKBAR_CLASS}').")
        return False

    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd_taskbar
    # Note: Getting the current AlwaysOnTop state to preserve it is complex,
    # so this version might force AlwaysOnTop off if it was on.
    # A more robust version would call ABM_GETSTATE first.

    current_state = shell32.SHAppBarMessage(ABM_GETSTATE, ctypes.byref(abd))
    is_currently_autohide = bool(current_state & ABS_AUTOHIDE)
    is_currently_alwaysontop = bool(current_state & ABS_ALWAYSONTOP) # Read current AlwaysOnTop

    # Prepare the desired state, preserving the current AlwaysOnTop state
    lParam = 0
    if autohide:
        lParam |= ABS_AUTOHIDE
    if is_currently_alwaysontop: # Preserve existing AlwaysOnTop state
        lParam |= ABS_ALWAYSONTOP

    abd.lParam = wintypes.LPARAM(lParam)

    print(f"Setting Taskbar State: AutoHide={autohide}, AlwaysOnTop={is_currently_alwaysontop}")
    result = shell32.SHAppBarMessage(ABM_SETSTATE, ctypes.byref(abd))
    # print(f"SHAppBarMessage(ABM_SETSTATE) result: {result}") # Optional debug

    # Sometimes a refresh is needed
    time.sleep(0.1)
    user32.UpdateWindow(hwnd_taskbar)

    return result != 0


def toggle_taskbar_autohide():
    """Toggles the taskbar's AutoHide property."""
    print(f"Hotkey '{HOTKEY}' pressed! Toggling taskbar AutoHide...")

    if os.name != 'nt':
        print("Error: This script uses Windows-specific functions.")
        return

    hwnd_taskbar = FindWindowW(TASKBAR_CLASS, None)
    if not hwnd_taskbar:
        print(f"Error: Could not find the main taskbar window ('{TASKBAR_CLASS}').")
        return

    # Get current state
    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd_taskbar
    current_state = shell32.SHAppBarMessage(ABM_GETSTATE, ctypes.byref(abd))

    is_currently_autohide = bool(current_state & ABS_AUTOHIDE)
    is_currently_alwaysontop = bool(current_state & ABS_ALWAYSONTOP) # Preserve this

    target_autohide_state = not is_currently_autohide

    if target_autohide_state:
        print("Enabling AutoHide...")
    else:
        print("Disabling AutoHide (Taskbar always visible)...")

    if set_taskbar_state(target_autohide_state, is_currently_alwaysontop):
        print("Toggle complete.")
    else:
        print("Error setting taskbar state.")


# --- Main Execution ---
if __name__ == "__main__":
    print("--- Taskbar AutoHide Toggle Script ---")

    if os.name != 'nt':
         print("Error: This script requires Windows to function.")
         sys.exit(1)

    # Note: Modifying AppBar state might require Admin more often than just ShowWindow
    if not is_admin():
        print("\nWARNING:")
        print("This script modifies system settings (Taskbar AutoHide).")
        print("It might require Administrator privileges to work reliably.")
        print("If it doesn't work, try running from a terminal launched 'As Administrator'.\n")
        time.sleep(3)

    print(f"Press '{HOTKEY}' to toggle the taskbar AutoHide setting.")
    print("The script will run in the background.")
    print("Press Ctrl+C in this window (or close it) to stop the script.")

    try:
        keyboard.add_hotkey(HOTKEY, toggle_taskbar_autohide, suppress=False)
        print("\nListening for hotkey...")
        keyboard.wait()

    except PermissionError:
         print("\nError: Permission denied.")
         print("This likely means you need to run the script as Administrator")
         print("to allow keyboard hooking or modifying system settings.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("\nTroubleshooting:")
        print("- Ensure 'keyboard' library is installed (`pip install keyboard`).")
        print("- Try running this script as an Administrator.")
        print(f"- Ensure '{HOTKEY}' isn't exclusively used elsewhere.")

    finally:
        print("\nScript stopping.")
        keyboard.unhook_all()
         # Attempt to restore taskbar to non-autohide state on exit? Optional.
        # print("Attempting to restore taskbar to always visible...")
        # set_taskbar_state(False) # Might leave it always on top if it was before
        print("Script stopped.")