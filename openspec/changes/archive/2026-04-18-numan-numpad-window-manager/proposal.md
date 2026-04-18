# Proposal: NumaN — Numpad Window Manager

## What

A Windows system-tray application that lets users assign any open window to numpad keys 1–9 and instantly switch between them. NumLock toggles the mode: **NumLock ON** = assign the currently focused window to the pressed numpad key; **NumLock OFF** = focus/bring-to-front the window assigned to that key. The app intercepts numpad keypresses globally so no stray characters leak into other applications.

## Why

Power users juggle many windows and Alt-Tab is slow. A dedicated numpad-based window switcher provides instant, muscle-memory access to 9 windows without learning complex shortcuts. The user wants something that "just works" — install it, it sits in the system tray, and optionally starts on boot.

## Research Sources (Principle 0)

| Area | Chosen Approach | Sources |
|------|----------------|---------|
| System Tray | **pystray** + Pillow | pystray official docs (pythonhosted.org), DEV Community tutorial, pythontutorial.net guide |
| Keyboard Hook | **pynput** `Listener(suppress=True)` + selective forwarding; fallback to `ctypes`/`SetWindowsHookEx` for numpad-only suppression | pynput 1.7.6 docs (readthedocs.io), pynput GitHub issues #526/#622, Stack Overflow answer on selective suppression |
| NumLock Detection | `ctypes.windll.user32.GetKeyState(VK_NUMLOCK=0x90)` — low-order bit = toggle state | Stack Overflow (Python 3.x GetKeyState), codeguru.com, thevbahelp.com |
| Window Focus | **pywin32** `win32gui.SetForegroundWindow(hwnd)` with `ShowWindow` workaround for focus-steal prevention | pywin32 docs on GitHub, Stack Overflow answers, Reddit r/learnpython |
| Window Enumeration | `win32gui.EnumWindows()` for listing, `win32gui.GetWindowText()` for titles | pywin32 docs, brunningonline.net tutorial |
| Exe Packaging | **PyInstaller** `--onefile --noconsole` | cx_Freeze vs PyInstaller comparison (ahmedsyntax.com 2026), Reddit r/Python, Stack Overflow |
| Installer | **Inno Setup** wrapping PyInstaller output | Stack Overflow (Inno Setup + Python), Medium tutorial, YouTube guide |
| README | jehna/readme-best-practices template, GitHub community discussion #176605, official GitHub guide | github.com/jehna/readme-best-practices, github.com/orgs/community/discussions/176605, coding-boot-camp.github.io |

## Acceptance Criteria

1. **Assign mode (NumLock ON):** Pressing numpad 1–9 while NumLock is active assigns the currently foreground window (hwnd) to that slot. A brief toast/tray notification confirms the assignment (e.g., "Slot 3 → Chrome").
2. **Focus mode (NumLock OFF):** Pressing numpad 1–9 while NumLock is off brings the assigned window to the foreground. If the slot is empty, nothing happens (no error).
3. **Key interception:** While the app is running, numpad 1–9 keypresses are suppressed (not forwarded to other apps) regardless of NumLock state.
4. **Graceful window close handling:** When an assigned window is closed/destroyed, its slot is automatically cleared — no stale references.
5. **System tray icon:** The app lives in the Windows notification area (system tray). Right-click shows a context menu with: current slot assignments, "Settings", and "Quit".
6. **Settings UI:** A simple config window accessible from the tray menu with a "Start on Windows startup" toggle. Setting is persisted to a JSON config file.
7. **Start on startup:** When enabled, the app registers itself in the Windows Registry Run key (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`).
8. **Clean exit:** Selecting "Quit" from the tray menu unhooks the keyboard listener, cleans up the tray icon, and exits gracefully.
9. **Windows installer:** An Inno Setup-based installer that installs the app to Program Files, creates a Start Menu shortcut, and registers an uninstaller.
10. **GitHub repo files:** Professional README.md, LICENSE, .gitignore, requirements.txt, CONTRIBUTING.md — written in a natural, non-AI tone following jehna/readme-best-practices conventions.

## Files Affected

This is a greenfield project. All files will be created:

- `src/numan/__init__.py` — package init
- `src/numan/main.py` — entry point, orchestrates tray + keyboard listener
- `src/numan/keyboard_hook.py` — pynput-based global keyboard hook with selective numpad suppression
- `src/numan/window_manager.py` — window assignment, focus, enumeration, close-detection via pywin32
- `src/numan/tray.py` — pystray system tray icon + context menu
- `src/numan/settings.py` — settings UI (tkinter) + JSON config persistence + startup registry
- `src/numan/config.py` — config file load/save logic
- `src/numan/icon.py` — programmatic icon generation (no external image dependency)
- `assets/icon.ico` — app icon for installer/tray
- `numan.spec` — PyInstaller spec file
- `installer/numan_setup.iss` — Inno Setup script
- `setup.py` — package setup for development installs
- `requirements.txt` — Python dependencies
- `README.md` — project README
- `LICENSE` — MIT license
- `.gitignore` — Python + build artifacts
- `CONTRIBUTING.md` — contribution guidelines
