# System Tray and Settings

## ADDED Requirements

### Requirement: No tray notifications on slot assignment

The system SHALL NOT display any toast or pop-up notification when a window is assigned to a numpad slot. Assignment SHALL be confirmed only via console log output.

#### Scenario: User assigns a window — no notification appears

- **Given** NumaN is running with NumLock ON (assign mode)
- **When** the user presses a numpad key and a window is successfully assigned to that slot
- **Then** no toast notification or pop-up appears in the Windows notification area
- **And** the assignment event is logged to the console only
