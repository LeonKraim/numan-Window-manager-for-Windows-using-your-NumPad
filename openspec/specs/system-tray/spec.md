# system-tray Specification

## Purpose
TBD - created by archiving change numan-numpad-window-manager. Update Purpose after archive.
## Requirements
### Requirement: System tray icon presence

The system SHALL display an icon in the Windows notification area (system tray) while running.

#### Scenario: App appears in system tray on launch

- **Given** the user launches NumaN
- **Then** a NumaN icon appears in the Windows system tray
- **And** hovering over it shows "NumaN — Numpad Window Manager"

### Requirement: Context menu with slot assignments

The system SHALL show a right-click context menu on the tray icon displaying current slot assignments, a Settings option, and a Quit option.

#### Scenario: User right-clicks tray icon

- **Given** NumaN is running with slot 1 assigned to "Chrome"
- **When** the user right-clicks the tray icon
- **Then** a menu appears showing "1: Chrome", other slots as "(empty)", "Settings", and "Quit"

### Requirement: Quit via context menu

The system SHALL cleanly shut down when the user selects "Quit" from the tray context menu.

#### Scenario: User quits via tray menu

- **Given** NumaN is running
- **When** the user right-clicks the tray icon and selects "Quit"
- **Then** the keyboard hook is removed
- **And** the tray icon disappears
- **And** the process exits

### Requirement: Settings window with startup toggle

The system SHALL provide a Settings window accessible from the tray menu with a "Start on Windows startup" checkbox that persists the setting.

#### Scenario: User enables start on startup

- **Given** NumaN is running
- **When** the user opens Settings from the tray menu
- **And** checks "Start NumaN when Windows starts"
- **And** clicks Save
- **Then** the setting is saved to config.json
- **And** a registry entry is created in HKCU\Software\Microsoft\Windows\CurrentVersion\Run

### Requirement: Start on Windows startup

The system SHALL launch automatically when Windows starts if the user has enabled the startup setting.

#### Scenario: NumaN starts on boot

- **Given** the user has enabled "Start on Windows startup"
- **When** the user restarts Windows and logs in
- **Then** NumaN starts automatically and appears in the system tray

### Requirement: No tray notifications on slot assignment

The system SHALL NOT display any toast or pop-up notification when a window is assigned to a numpad slot. Assignment SHALL be confirmed only via console log output.

#### Scenario: User assigns a window — no notification appears

- **Given** NumaN is running with NumLock ON (assign mode)
- **When** the user presses a numpad key and a window is successfully assigned to that slot
- **Then** no toast notification or pop-up appears in the Windows notification area
- **And** the assignment event is logged to the console only

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

