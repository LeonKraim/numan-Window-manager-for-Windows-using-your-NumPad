# Tasks: NumaN — Numpad Window Manager

## Phase 1: Core Infrastructure

- [x] Task 1: Create project structure — `src/numan/` package, `__init__.py`, `requirements.txt`, `setup.py`, `.gitignore`
- [x] Task 2: Implement `config.py` — JSON config load/save to `%APPDATA%/numan/config.json` with defaults
- [x] Task 3: Implement `icon.py` — programmatic 3x3 grid icon generation with Pillow, export `.ico`

## Phase 2: Window Management

- [x] Task 4: Implement `window_manager.py` — `WindowManager` class with assign, focus, cleanup_dead, slot listing
- [x] Task 5: Implement dead-window watcher — background thread polling `IsWindow()` every 2 seconds

## Phase 3: Keyboard Hook

- [x] Task 6: Implement `keyboard_hook.py` — low-level Windows keyboard hook via ctypes (`SetWindowsHookEx` + `WH_KEYBOARD_LL`) with numpad-only suppression
- [x] Task 7: Implement NumLock state detection and mode switching — `GetKeyState(VK_NUMLOCK)`, assign on NumLock ON, focus on NumLock OFF

## Phase 4: System Tray + Settings

- [x] Task 8: Implement `tray.py` — pystray system tray icon with dynamic context menu (slot list, Settings, Quit)
- [x] Task 9: Implement `settings.py` — tkinter settings window with "Start on startup" toggle + `winreg` startup registration
- [x] Task 10: Implement `main.py` — entry point wiring all components together, thread orchestration

## Phase 5: Packaging & Installer

- [x] Task 11: Create PyInstaller spec file (`numan.spec`) and build script for `--onefile --noconsole` .exe
- [x] Task 12: Create Inno Setup script (`installer/numan_setup.iss`) — installer with Start Menu shortcut, uninstaller, optional desktop shortcut

## Phase 6: GitHub Repo Files

- [x] Task 13: Write `README.md` — natural tone, following jehna/readme-best-practices; sections: what it does, screenshot/demo, install, usage, config, build from source, license
- [x] Task 14: Write `LICENSE` (MIT), `CONTRIBUTING.md`, finalize `.gitignore`

## Phase 7: Verification

- [ ] Task 15: Run the app, verify all 10 acceptance criteria with screenshots/output
