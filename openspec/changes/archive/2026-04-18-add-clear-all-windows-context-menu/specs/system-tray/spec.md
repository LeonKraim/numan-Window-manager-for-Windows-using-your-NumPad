## ADDED Requirements

### Requirement: Clear all windows from context menu

The system SHALL provide a "Clear All Windows" option in the system tray context menu that clears all assigned window slots when clicked.

#### Scenario: Clear all slots from context menu

- **Given** NumaN is running with multiple windows assigned to slots
- **When** the user right-clicks the NumaN system tray icon
- **Then** the context menu includes a "Clear All Windows" option
- **And** clicking "Clear All Windows" removes all window assignments from all slots

#### Scenario: Slots become empty after clearing

- **Given** slots 1, 2, and 3 are assigned to different windows
- **When** the user selects "Clear All Windows" from the context menu
- **Then** all slots become empty
- **And** pressing any numpad slot key will assign the current foreground window to that slot
