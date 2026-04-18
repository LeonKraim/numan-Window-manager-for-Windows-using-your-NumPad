# logging Specification

## Purpose
TBD - created by archiving change prevent-vscode-tab-navigation-from-reassigning-slots. Update Purpose after archive.
## Requirements
### Requirement: Runtime logs are persisted to disk

The system SHALL persist runtime logs to `%APPDATA%/numan/numan.log` so recent executable behavior can be inspected after a no-console run. Focus attempts SHALL log whether the target window actually became the foreground window.

#### Scenario: Focus failure includes foreground diagnostics

- **Given** a slot focus attempt does not bring the target window to the foreground
- **When** NumaN logs the focus failure
- **Then** the runtime log includes the target window handle
- **And** the actual foreground window handle
- **And** the result of the foreground request

