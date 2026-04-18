# Design

## Approach

The hook will continue to run as a low-level keyboard hook, but slot detection will become stricter:

- When NumLock is on, only `VK_NUMPAD1` through `VK_NUMPAD9` are accepted.
- When NumLock is off, only the specific numpad navigation virtual keys that correspond to numpad `1` through `9` are accepted.
- The existing non-extended-key and scan-code checks remain in place so real navigation-cluster keys are not treated as numpad keys.

## Behavioral Change

When NumLock is off, slot lookup stays focus-first. If the slot has no live window, the hook immediately assigns the current foreground window to that slot. This keeps the single-key workflow intact without changing slot storage or tray behavior.

## Scope

This change is limited to keyboard-hook behavior. It does not change tray UI, persistence, installer logic, or window slot storage.
