## MODIFIED Requirements

### Requirement: Focus assigned window via numpad slot

The system SHALL bring the assigned window to the foreground when NumLock is OFF and the user presses the corresponding numpad key. The system SHALL only report focus success when the target window actually becomes the foreground window.

#### Scenario: Covered target window is raised and activated

- **Given** NumaN is running and slot `2` is assigned to a live window
- **And** NumLock is OFF
- **And** another normal window is currently in front of the assigned window
- **When** the user presses numpad `2`
- **Then** the window assigned to slot `2` becomes the foreground window
- **And** it is no longer left behind the previously frontmost window
