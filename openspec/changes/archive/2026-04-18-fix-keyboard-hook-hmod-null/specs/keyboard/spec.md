## ADDED Requirements

### Requirement: Keyboard hook SHALL pass NULL as hMod to SetWindowsHookExW
The keyboard hook installation SHALL pass `None` (NULL) as the `hMod` parameter to `SetWindowsHookExW` when installing a `WH_KEYBOARD_LL` low-level hook. Per MSDN, for low-level hooks the `hMod` parameter is ignored by the system and MUST be set to NULL; passing a non-NULL handle causes Error 126 (ERROR_MOD_NOT_FOUND).

#### Scenario: Keyboard hook installs without error
- **Given** the NumaN application starts
- **When** the keyboard hook thread calls SetWindowsHookExW
- **Then** the hook is installed successfully (no Error 126) and "Keyboard hook installed" is logged
