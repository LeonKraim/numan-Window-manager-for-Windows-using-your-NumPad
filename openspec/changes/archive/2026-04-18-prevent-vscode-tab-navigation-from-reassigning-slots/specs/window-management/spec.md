## MODIFIED Requirements

### Requirement: Focus assigned window via numpad slot

The system SHALL bring the assigned window to the foreground when NumLock is OFF and the user presses the corresponding numpad key. If the focus attempt fails for a live assigned window, the existing slot assignment SHALL be preserved.

#### Scenario: Focus failure preserves the existing slot assignment

- **Given** NumaN is running and slot `3` is assigned to a live window
- **And** NumLock is OFF
- **And** the current foreground window is Visual Studio Code
- **And** the attempt to focus the assigned window fails
- **When** the user presses numpad `3`
- **Then** slot `3` remains assigned to the previously stored window
- **And** the Visual Studio Code window is not assigned into slot `3`

## ADDED Requirements

### Requirement: Empty or stale slot press assigns the current window

The system SHALL assign the current foreground window when NumLock is OFF and the user presses a slot that is empty or stale.

#### Scenario: User presses an empty slot

- **Given** NumaN is running and slot `5` has no window assigned
- **And** NumLock is OFF
- **When** the user presses numpad `5`
- **Then** the current foreground window is assigned to slot `5`

#### Scenario: User presses a stale slot

- **Given** NumaN is running and slot `5` points to a window that no longer exists
- **And** NumLock is OFF
- **When** the user presses numpad `5`
- **Then** slot `5` is cleared and the current foreground window is assigned to slot `5`
