# Design

## Root Cause

The current low-level hook uses a generic C callback type instead of the Windows `CALLBACK` calling convention, and it declares hook-related types with incorrect pointer-sized fields. For `WH_KEYBOARD_LL`, the callback signature must match `LRESULT CALLBACK LowLevelKeyboardProc(int, WPARAM, LPARAM)`. If it does not, the hook can return corrupted values and interfere with unrelated keyboard input.

## Approach

- Replace the callback declaration with a Windows callback signature.
- Use pointer-sized types for `LRESULT`, `HHOOK`, and `dwExtraInfo`.
- Set the relevant `user32` function prototypes so hook chaining and return values are not truncated.

## Scope

This change is limited to the low-level keyboard hook definitions and does not change slot storage, tray behavior, or installer behavior.
