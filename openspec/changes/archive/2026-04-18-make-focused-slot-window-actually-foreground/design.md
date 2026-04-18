# Design

## Root Cause

The current focus path only attaches the hook thread to the current foreground thread and then calls `SetForegroundWindow`. Logs show that this call can fail for some target windows. The code also treats the call as successful whenever no exception is raised, even if the target window never becomes foreground.

## Approach

- Attach the current thread to both the current foreground window thread and the target window thread when needed.
- Restore or show the target window, bring it to the top of the Z order, request foreground activation, and then verify the actual foreground window.
- Log the target and actual foreground window details when the request fails.

## Scope

This change is limited to the live-slot focus path and its diagnostic logging. It does not change slot assignment rules or tray behavior.
