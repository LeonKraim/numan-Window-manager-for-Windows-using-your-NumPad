# Design

## Root Cause

`KeyboardHook._handle_numpad()` currently treats every falsey result from `WindowManager.focus()` as if the slot were empty or stale. That means a transient or application-specific focus failure causes the current foreground window to be assigned into the slot, overwriting the existing assignment.

## Approach

- Change `WindowManager.focus()` to return an explicit result status instead of a boolean.
- Only trigger fallback assignment when the slot is genuinely missing or stale.
- Preserve the existing slot assignment when focus fails for a live assigned window.
- Configure root logging to write both to stdout and a rotating file in the existing AppData config directory.

## Scope

This change is limited to slot focus/assignment behavior and runtime logging. It does not change tray UI, installer behavior, or the numpad key matching rules.
