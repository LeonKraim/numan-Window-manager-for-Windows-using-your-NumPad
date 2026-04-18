# Change: add-clear-all-windows-context-menu

## Why

User requested a convenient way to clear all saved window assignments at once from the system tray context menu instead of manually removing each slot one by one.

## What Changes

- Add a "Clear All Windows" option to the system tray context menu
- Implement `clear_all_slots()` method in WindowManager to atomically clear all assigned slots
- Wire the menu item to the clear handler with automatic menu refresh

## Acceptance Criteria

1. Right-clicking the NumaN system tray icon displays a context menu with a "Clear All Windows" option
2. Clicking "Clear All Windows" removes all window assignments from all slots atomically
3. After clearing, pressing any numpad slot key assigns the current foreground window to that slot
4. The context menu continues to function correctly with no regressions to existing items (Settings, Quit)
5. The clear action is logged to the runtime log at `%APPDATA%/numan/numan.log` with a count of cleared slots
