# Change: stop-keyboard-hook-from-blocking-normal-input

## Why

NumaN is still blocking normal keyboard input and preventing NumLock from being toggled reliably, which makes the application unusable during normal typing.

## What Changes

- Correct the low-level keyboard hook callback and structure definitions to match the Windows API ABI for `WH_KEYBOARD_LL`
- Preserve the existing slot-key behavior while ensuring non-target keys are forwarded normally
- Rebuild and verify the executable after the fix

## Acceptance Criteria

1. Normal typing on the main keyboard works while NumaN is running.
2. NumLock can still be toggled while NumaN is running.
3. Only intended numpad `1` through `9` slot keypresses are suppressed and handled by NumaN.
