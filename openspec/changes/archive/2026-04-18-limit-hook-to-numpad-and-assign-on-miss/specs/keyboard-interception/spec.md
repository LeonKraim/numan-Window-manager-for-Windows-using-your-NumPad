## MODIFIED Requirements

### Requirement: Global numpad key suppression

The system SHALL intercept and suppress only numpad keys `1` through `9` globally while NumaN is running. The system SHALL NOT suppress top-row digits or non-numpad navigation keys.

#### Scenario: Top-row digits are not affected

- **Given** NumaN is running
- **And** the user has a text editor focused
- **When** the user presses the `1` key on the main number row
- **Then** the character `1` is typed into the text editor normally
- **And** NumaN does not process the keypress as a slot action

#### Scenario: Numpad digits remain suppressed

- **Given** NumaN is running
- **And** the user has a text editor focused
- **When** the user presses numpad `7`
- **Then** the corresponding numpad input is not typed into the text editor
- **And** NumaN processes the keypress according to NumLock state

### Requirement: NumLock state determines mode

The system SHALL use the NumLock toggle state to determine whether a numpad press triggers assign mode (NumLock ON) or focus mode (NumLock OFF). When focus mode targets an empty or stale slot, the system SHALL assign the current foreground window to that slot instead of ignoring the keypress.

#### Scenario: NumLock off assigns when the slot is empty

- **Given** NumaN is running
- **And** NumLock is OFF
- **And** slot `3` is not assigned
- **When** the user presses numpad `3`
- **Then** the current foreground window is assigned to slot `3`

#### Scenario: NumLock off focuses an assigned slot

- **Given** NumaN is running
- **And** NumLock is OFF
- **And** slot `3` is assigned to a live window
- **When** the user presses numpad `3`
- **Then** the assigned window is focused
