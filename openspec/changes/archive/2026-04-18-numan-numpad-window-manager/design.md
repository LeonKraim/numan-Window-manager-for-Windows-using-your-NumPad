# Design: NumaN — Numpad Window Manager

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    main.py                          │
│  (entry point — starts tray + keyboard on threads)  │
├──────────┬──────────┬──────────┬────────────────────┤
│ tray.py  │ keyboard │ window   │ settings.py        │
│ (pystray │ _hook.py │ _manager │ (tkinter UI +      │
│  icon +  │ (pynput  │ .py      │  config persist +  │
│  menu)   │  global  │ (assign, │  registry startup) │
│          │  hook,   │  focus,  │                    │
│          │  numlock │  enum,   │                    │
│          │  detect) │  detect  │                    │
│          │          │  close)  │                    │
└──────────┴──────────┴──────────┴────────────────────┘
                        │
                   config.py
              (JSON load/save)
```

## Threading Model

- **Main thread:** Runs `pystray.Icon.run()` — this is required by pystray (blocks the main thread).
- **Keyboard listener thread:** pynput's `Listener` runs in its own daemon thread. It is started from pystray's `setup` callback.
- **Window close watcher thread:** A daemon thread that polls assigned window handles every 2 seconds using `win32gui.IsWindow(hwnd)`. Removes dead handles.
- **Settings UI:** Launched on-demand in a new thread. Uses tkinter — `Tk()` is created fresh each time (tkinter wants to own its thread).

## Module Details

### `main.py` — Entry Point

```python
def main():
    config = Config.load()
    wm = WindowManager()
    hook = KeyboardHook(wm, config)
    tray = TrayApp(wm, hook, config)
    tray.run()  # blocks on main thread
```

- Loads config from `%APPDATA%/numan/config.json`
- Creates `WindowManager`, `KeyboardHook`, `TrayApp` instances
- `tray.run()` starts pystray; its `setup` callback starts the keyboard listener + window watcher

### `keyboard_hook.py` — Global Numpad Interception

**Key decisions:**
- Use `pynput.keyboard.Listener(suppress=True)` for global hook with key suppression.
- Problem: `suppress=True` blocks ALL keys. Solution: In the `on_press` callback, return `None` to suppress only numpad 1–9 keys; for all other keys, use `pynput.keyboard.Controller().press(key)` to re-emit them immediately.
- Alternative (if pynput suppression is unreliable): Use `ctypes` to install a low-level keyboard hook via `SetWindowsHookEx(WH_KEYBOARD_LL, ...)` directly, which gives per-key suppress control by returning 1 from the hook proc.

**NumLock detection:**
```python
import ctypes
def is_numlock_on():
    return ctypes.windll.user32.GetKeyState(0x90) & 1
```

**Numpad key mapping (VK codes):**
| Key | VK Code (NumLock ON) | VK Code (NumLock OFF) |
|-----|---------------------|----------------------|
| Numpad 1 | 0x61 (VK_NUMPAD1) | 0x23 (VK_END) |
| Numpad 2 | 0x62 (VK_NUMPAD2) | 0x28 (VK_DOWN) |
| ... | ... | ... |
| Numpad 9 | 0x69 (VK_NUMPAD9) | 0x21 (VK_PRIOR) |

Since pynput provides scan codes and VK codes, we identify numpad keys by their `vk` attribute. When NumLock is OFF, the numpad emits navigation keys (End, Down, PgDn, etc.) — we need to intercept based on scan code, not VK code, to distinguish numpad from real arrow keys.

**Approach: Low-level Windows hook via ctypes** (chosen over pynput suppress due to selective suppression needs):

```python
# WH_KEYBOARD_LL = 13
# The hook callback receives KBDLLHOOKSTRUCT which includes:
# - vkCode: virtual key code
# - scanCode: hardware scan code
# - flags: LLKHF_EXTENDED (bit 0) — numpad keys do NOT have this flag
#          when they produce number VK codes
```

By checking both vkCode and the extended-key flag, we can reliably identify numpad 1–9 regardless of NumLock state:
- NumLock ON: vkCode = VK_NUMPAD1..9 (0x61–0x69), not extended
- NumLock OFF: vkCode = VK_END/VK_DOWN/etc., but scanCode is numpad-specific and extended flag is NOT set

This approach lets us suppress (return 1) only numpad keys while forwarding everything else via `CallNextHookEx`.

### `window_manager.py` — Window Slot Management

```python
class WindowManager:
    def __init__(self):
        self.slots: dict[int, int] = {}  # slot_number -> hwnd
        self._lock = threading.Lock()
    
    def assign(self, slot: int) -> tuple[int, str] | None:
        """Assign current foreground window to slot. Returns (hwnd, title) or None."""
        hwnd = win32gui.GetForegroundWindow()
        if hwnd and win32gui.IsWindow(hwnd):
            title = win32gui.GetWindowText(hwnd)
            with self._lock:
                self.slots[slot] = hwnd
            return (hwnd, title)
        return None
    
    def focus(self, slot: int) -> bool:
        """Focus the window in the given slot. Returns success."""
        with self._lock:
            hwnd = self.slots.get(slot)
        if hwnd and win32gui.IsWindow(hwnd):
            # Workaround for SetForegroundWindow restriction:
            # 1. If window is minimized, restore it
            # 2. Use SetForegroundWindow
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
        else:
            # Window no longer exists — clean up
            with self._lock:
                self.slots.pop(slot, None)
            return False
    
    def cleanup_dead(self):
        """Remove slots pointing to dead windows."""
        with self._lock:
            dead = [s for s, h in self.slots.items() if not win32gui.IsWindow(h)]
            for s in dead:
                del self.slots[s]
```

**Focus-steal workaround:** Windows prevents `SetForegroundWindow` unless the calling process is the foreground process. Workarounds:
1. `win32gui.ShowWindow(hwnd, SW_MINIMIZE)` then `SW_RESTORE` (flash trick)
2. Use `ctypes.windll.user32.AllowSetForegroundWindow(ASFW_ANY=-1)` at startup
3. Attach to the foreground thread input via `AttachThreadInput`

We'll use approach #2 at startup + #1 as fallback.

### `tray.py` — System Tray

```python
class TrayApp:
    def __init__(self, wm, hook, config):
        self.wm = wm
        self.hook = hook
        self.config = config
        self.icon = pystray.Icon("numan", self._create_icon(), "NumaN", self._build_menu())
    
    def run(self):
        self.icon.run(setup=self._on_setup)
    
    def _on_setup(self, icon):
        icon.visible = True
        self.hook.start()  # start keyboard listener thread
        self._start_watcher()  # start dead-window watcher thread
    
    def _build_menu(self):
        return pystray.Menu(
            pystray.MenuItem("Slots", pystray.Menu(
                # Dynamic: show current slot assignments
                *[pystray.MenuItem(f"{i}: {self._slot_label(i)}", None) for i in range(1, 10)]
            )),
            pystray.MenuItem("Settings", self._open_settings),
            pystray.MenuItem("Quit", self._quit),
        )
    
    def _quit(self):
        self.hook.stop()
        self.icon.stop()
```

Menu is dynamically rebuilt on each right-click (pystray supports dynamic menu items via callables).

### `settings.py` — Settings UI + Startup Registry

A minimal tkinter window with:
- Checkbox: "Start on Windows startup"
- Info label showing config file path
- Save / Close buttons

**Startup registration:**
```python
import winreg

KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

def set_startup(enabled: bool, exe_path: str):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH, 0, winreg.KEY_SET_VALUE)
    if enabled:
        winreg.SetValueEx(key, "NumaN", 0, winreg.REG_SZ, exe_path)
    else:
        try:
            winreg.DeleteValue(key, "NumaN")
        except FileNotFoundError:
            pass
    winreg.CloseKey(key)
```

### `config.py` — Configuration Persistence

```python
CONFIG_DIR = os.path.join(os.environ.get("APPDATA", ""), "numan")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "start_on_startup": False,
}
```

- Creates `%APPDATA%/numan/` if it doesn't exist
- Loads/saves JSON
- Thread-safe reads (config is read-mostly)

### `icon.py` — Programmatic Icon Generation

Generate a simple grid icon using Pillow so there's no external image dependency:
```python
def create_icon(size=64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw a 3x3 grid of colored squares representing numpad
    # Each cell is a different shade/color
    ...
    return img
```

Also export a `.ico` file for the installer.

## Packaging & Installer

### PyInstaller

```
pyinstaller --onefile --noconsole --icon=assets/icon.ico --name=numan src/numan/main.py
```

- `--noconsole`: No terminal window on launch
- `--onefile`: Single .exe for simplicity
- Produces `dist/numan.exe`

### Inno Setup (`installer/numan_setup.iss`)

- Installs `numan.exe` to `{autopf}\NumaN\`
- Creates Start Menu entry under `NumaN`
- Registers uninstaller
- Optionally creates desktop shortcut
- Sets `{app}\numan.exe` as the value for the registry Run key if user enables startup

## Error Handling

- **Invalid hwnd on focus:** `IsWindow()` check before every `SetForegroundWindow`. If false, silently remove slot.
- **Keyboard hook failure:** If hook installation fails, show a tray notification and exit.
- **Config file corruption:** Fall back to defaults, overwrite with clean config.
- **Permissions:** The app runs as the current user. No admin needed for `HKCU` registry or user-level keyboard hooks.

## Security Considerations

- Global keyboard hooks have security implications. The app only intercepts numpad 1–9 and does not log or transmit any keystrokes.
- Config file is stored in user-scoped `%APPDATA%` — no system-wide writes.
- Registry writes are limited to `HKCU` — no admin elevation needed.
- The installer does not require admin if installed to user-scoped directories (though default Program Files does).
