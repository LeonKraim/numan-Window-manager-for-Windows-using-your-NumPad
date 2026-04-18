# Installer and Distribution

## ADDED Requirements

### Requirement: Windows installer

The system SHALL provide an Inno Setup-based Windows installer that installs the application to Program Files, creates Start Menu shortcuts, and registers an uninstaller.

#### Scenario: User installs NumaN

- **Given** the user has downloaded the NumaN installer
- **When** the user runs the installer and follows the wizard
- **Then** numan.exe is installed to the chosen directory
- **And** a Start Menu shortcut is created
- **And** an uninstaller is registered in Windows Add/Remove Programs

### Requirement: Clean uninstall

The system SHALL remove all installed files, shortcuts, registry entries, and user config on uninstall.

#### Scenario: User uninstalls NumaN

- **Given** NumaN is installed
- **When** the user runs the uninstaller
- **Then** the application files are removed
- **And** the Start Menu shortcut is removed
- **And** the startup registry entry is removed
- **And** the %APPDATA%\numan config directory is removed
