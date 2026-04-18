# Change: make-focused-slot-window-actually-foreground

## Why

NumaN can fail to bring an assigned window to the actual foreground when another window is currently on top. Recent runtime logs show repeated `SetForegroundWindow` failures for some slots.

## What Changes

- Strengthen the slot focus path so it raises and foregrounds the target window using a verified Win32 activation sequence
- Only log a slot as focused when the target window is actually the foreground window
- Add clearer diagnostic logging for failed foreground requests

## Acceptance Criteria

1. When a live slot is invoked with NumLock OFF, the assigned window becomes the foreground window.
2. If another normal window is currently in front of the target, the target window is raised and activated instead of staying behind it.
3. Runtime logs clearly show the result of the foreground request, including whether the target actually became the foreground window.
