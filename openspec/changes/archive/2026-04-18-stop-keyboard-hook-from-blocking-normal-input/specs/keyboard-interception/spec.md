## MODIFIED Requirements

### Requirement: Non-numpad keys are not affected

The system SHALL forward non-target keyboard input normally while NumaN is running. Only intended numpad slot keypresses may be suppressed.

#### Scenario: Regular typing still works

- **Given** NumaN is running
- **And** the user has a text field focused
- **When** the user types letters or top-row digits on the main keyboard
- **Then** the typed characters appear normally in the text field
- **And** NumaN does not suppress those keypresses

#### Scenario: NumLock can still be toggled

- **Given** NumaN is running
- **When** the user presses the NumLock key
- **Then** the NumLock state changes normally
- **And** NumaN does not suppress the NumLock keypress
