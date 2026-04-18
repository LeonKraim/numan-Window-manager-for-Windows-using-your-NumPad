# Window Slot Management

## ADDED Requirements

### Requirement: Assign window to numpad slot

The system SHALL allow the user to assign the currently foreground window to a numpad slot (1–9) when NumLock is ON and a numpad key is pressed.

#### Scenario: User assigns a window to slot 3

- **Given** NumaN is running and NumLock is ON
- **And** the user has a browser window in the foreground
- **When** the user presses numpad 3
- **Then** the browser window handle is stored in slot 3
- **And** a tray notification displays "Slot 3 → <window title>"

### Requirement: Focus assigned window via numpad slot

The system SHALL bring the assigned window to the foreground when NumLock is OFF and the user presses the corresponding numpad key.

#### Scenario: User focuses window in slot 3

- **Given** NumaN is running and a window is assigned to slot 3
- **And** NumLock is OFF
- **When** the user presses numpad 3
- **Then** the window assigned to slot 3 is brought to the foreground
- **And** if the window was minimized, it is restored first

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
