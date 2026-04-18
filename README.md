# NumaN: Window Manager for Windows using you Numpad

An app that turns your numpad into a window switcher. Assign any window to keys 1–9, then jump between them instantly.


## How it works

NumaN sits in your system tray and intercepts numpad keypresses:

- **NumLock ON** — press a numpad key to *assign* the current window to that slot
- **NumLock OFF** — press a numpad key to *switch to* the window in that slot
- If you press a number on your numpad thats unassigned it always defines the current selected window.

The numpad keys are intercepted by NumaN while it's running, so you won't accidentally type numbers into whatever you're working on.

When a window gets closed, its slot clears automatically. No stale references, no crashes.

## Install

Grab the latest installer from [Releases](../../releases) and run it. Takes about 10 seconds.

The installer gives you the option to start NumaN on boot. You can also toggle that later from the settings.

### Building from source

You'll need Python 3.10+ and the dependencies:

```
pip install -r requirements.txt
```

Run it directly:

```
python src/numan/main.py
```

Or build the exe:

```
pip install pyinstaller
build.bat
```

The executable lands in `dist/numan.exe`. If you have [Inno Setup](https://jrsoftware.org/isinfo.php) installed, open `installer/numan_setup.iss` to create a proper installer.

## Usage

1. Launch NumaN (or let it start on boot)
2. A small grid icon appears in your system tray
3. Focus the window you want to pin, make sure NumLock is on, press a numpad key (1–9)
4. You'll see a notification confirming the assignment
5. Turn NumLock off, press that same key — the window pops to the front

Right-click the tray icon to see your current slot assignments, open settings, or quit.

## Configuration

Settings are stored in `%APPDATA%\numan\config.json`. There's one setting right now:

| Setting | Default | What it does |
|---------|---------|--------------|
| `start_on_startup` | `false` | Register NumaN to launch when Windows starts |

You can edit the file directly or use the Settings window from the tray menu.

## System requirements

- Windows 10 or later


## Project structure

```
src/numan/
├── main.py             # Entry point
├── keyboard_hook.py    # Low-level keyboard hook (numpad interception)
├── window_manager.py   # Window assignment, focus, dead-window cleanup
├── tray.py             # System tray icon and menu
├── settings.py         # Settings UI + Windows startup registration
├── config.py           # Config file read/write
└── icon.py             # Generates the tray icon programmatically
```

## Known limitations

- Only works on Windows (relies on Win32 APIs for keyboard hooks and window management)
- Some fullscreen/exclusive apps may resist being focused via `SetForegroundWindow` — this is a Windows limitation, not a NumaN bug


