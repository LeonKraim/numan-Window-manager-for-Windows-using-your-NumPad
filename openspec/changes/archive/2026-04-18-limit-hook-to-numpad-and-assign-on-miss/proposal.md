# Change: limit-hook-to-numpad-and-assign-on-miss

## Summary

Restrict NumaN's low-level keyboard handling to explicit numpad `1` through `9` presses and improve the NumLock-off flow so an unassigned slot assigns the current foreground window instead of doing nothing.

## Problem

The current behavior is broader than intended and makes the application feel like it is capturing too much keyboard input. It also makes focus mode feel broken when a slot has not been assigned yet.

## Acceptance Criteria

1. Pressing top-row digits or unrelated keys does not trigger or suppress any NumaN action.
2. Pressing numpad `1` through `9` with NumLock on assigns the current foreground window to the matching slot.
3. Pressing numpad `1` through `9` with NumLock off focuses the assigned window, and if the slot is empty or stale it assigns the current foreground window to that slot instead.
