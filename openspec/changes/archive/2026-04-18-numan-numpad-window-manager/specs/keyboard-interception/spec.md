# Keyboard Interception

## ADDED Requirements

### Requirement: Global numpad key suppression

The system SHALL intercept and suppress numpad keys 1–9 globally while NumaN is running, preventing the keypresses from reaching other applications.

#### Scenario: Numpad key is suppressed during normal use

- **Given** NumaN is running
- **And** the user has a text editor focused
- **When** the user presses numpad 7
- **Then** the character "7" is NOT typed into the text editor
- **And** NumaN processes the keypress according to NumLock state

### Requirement: Non-numpad keys are not affected

The system SHALL forward all non-numpad keypresses normally without interference.

#### Scenario: Regular keyboard input is unaffected

- **Given** NumaN is running
- **And** the user has a text editor focused
- **When** the user presses the letter "A" on the main keyboard
- **Then** the character "A" is typed into the text editor normally

### Requirement: NumLock state determines mode

The system SHALL use the NumLock toggle state to determine whether a numpad press triggers assign mode (NumLock ON) or focus mode (NumLock OFF).

#### Scenario: Mode switches when NumLock is toggled

- **Given** NumaN is running and NumLock is ON
- **When** the user presses numpad 1
- **Then** the current window is assigned to slot 1
- **When** the user toggles NumLock OFF
- **And** presses numpad 1
- **Then** the window assigned to slot 1 is focused
