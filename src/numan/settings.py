import os
import sys
import threading
import tkinter as tk
from tkinter import ttk
import winreg
import logging

logger = logging.getLogger(__name__)

REG_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "NumaN"


def _get_exe_path():
    if getattr(sys, "frozen", False):
        return sys.executable
    return os.path.abspath(sys.argv[0])


def get_startup_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN_KEY, 0, winreg.KEY_READ)
        try:
            winreg.QueryValueEx(key, APP_NAME)
            return True
        except FileNotFoundError:
            return False
        finally:
            winreg.CloseKey(key)
    except OSError:
        return False


def set_startup(enabled):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN_KEY, 0, winreg.KEY_SET_VALUE)
        try:
            if enabled:
                exe_path = _get_exe_path()
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
                logger.info("Startup enabled: %s", exe_path)
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
                logger.info("Startup disabled")
        finally:
            winreg.CloseKey(key)
    except OSError as e:
        logger.error("Failed to set startup: %s", e)


class SettingsWindow:
    def __init__(self, config):
        self.config = config
        self._window = None
        self._lock = threading.Lock()

    def open(self):
        with self._lock:
            if self._window is not None:
                return
        t = threading.Thread(target=self._create_window, daemon=True, name="settings-ui")
        t.start()

    def _create_window(self):
        root = tk.Tk()
        root.title("NumaN Settings")
        root.geometry("350x180")
        root.resizable(False, False)

        with self._lock:
            self._window = root

        root.protocol("WM_DELETE_WINDOW", lambda: self._close(root))

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(frame, text="NumaN Settings", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W)
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 10))

        # Start on startup checkbox
        startup_var = tk.BooleanVar(value=self.config.start_on_startup)
        startup_cb = ttk.Checkbutton(
            frame,
            text="Start NumaN when Windows starts",
            variable=startup_var,
        )
        startup_cb.pack(anchor=tk.W, pady=(0, 10))

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Save", command=lambda: self._save(root, startup_var)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="Cancel", command=lambda: self._close(root)).pack(side=tk.RIGHT)

        root.mainloop()

    def _save(self, root, startup_var):
        enabled = startup_var.get()
        self.config.start_on_startup = enabled
        self.config.save()
        set_startup(enabled)
        self._close(root)

    def _close(self, root):
        with self._lock:
            self._window = None
        root.destroy()
