# window-management Specification

## Purpose
TBD - created by archiving change numan-numpad-window-manager. Update Purpose after archive.
## Requirements
### Requirement: Assign window to numpad slot

The system SHALL allow the user to assign the currently foreground window to a numpad slot (1–9) when NumLock is ON and a numpad key is pressed.

#### Scenario: User assigns a window to slot 3

- **Given** NumaN is running and NumLock is ON
- **And** the user has a browser window in the foreground
- **When** the user presses numpad 3
- **Then** the browser window handle is stored in slot 3
- **And** a tray notification displays "Slot 3 → <window title>"

### Requirement: Focus assigned window via numpad slot

The system SHALL bring the assigned window to the foreground when NumLock is OFF and the user presses the corresponding numpad key. The system SHALL only report focus success when the target window actually becomes the foreground window.

#### Scenario: Covered target window is raised and activated

- **Given** NumaN is running and slot `2` is assigned to a live window
- **And** NumLock is OFF
- **And** another normal window is currently in front of the assigned window
- **When** the user presses numpad `2`
- **Then** the window assigned to slot `2` becomes the foreground window
- **And** it is no longer left behind the previously frontmost window

### Requirement: Empty slot press does nothing

The system SHALL silently ignore numpad presses for slots that have no window assigned.

#### Scenario: User presses an empty slot

- **Given** NumaN is running and slot 5 has no window assigned
- **And** NumLock is OFF
- **When** the user presses numpad 5
- **Then** nothing happens and no error is shown

### Requirement: Graceful dead window cleanup

The system SHALL automatically remove a window from its slot when that window is closed or destroyed.

#### Scenario: Assigned window is closed by the user

- **Given** a window is assigned to slot 2
- **When** the user closes that window
- **Then** within 2 seconds, slot 2 is cleared automatically
- **And** the tray menu reflects the empty slot

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

