# Change: prevent-vscode-tab-navigation-from-reassigning-slots

## Why

When VS Code is focused, using NumaN can overwrite an already assigned slot with the current VS Code window if a focus attempt fails. The executable also does not persist logs, which makes runtime diagnosis difficult.

## What Changes

- Distinguish empty or stale slots from focus failures on live assigned windows
- Preserve existing assignments when a focus attempt fails instead of reassigning the current foreground window
- Persist runtime logs to a rotating log file under `%APPDATA%/numan/`

## Acceptance Criteria

1. Pressing a slot with NumLock OFF does not overwrite an already assigned live slot just because a focus attempt fails.
2. Pressing a slot with NumLock OFF still assigns the current foreground window when the slot is empty or stale.
3. The executable writes recent runtime logs to `%APPDATA%/numan/numan.log`.
