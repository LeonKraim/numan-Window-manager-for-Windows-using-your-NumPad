## ADDED Requirements

### Requirement: Runtime logs are persisted to disk

The system SHALL persist runtime logs to `%APPDATA%/numan/numan.log` so recent executable behavior can be inspected after a no-console run.

#### Scenario: Executable startup creates or appends to the runtime log

- **Given** the NumaN executable starts successfully
- **When** startup logging is configured
- **Then** log output is written to `%APPDATA%/numan/numan.log`
- **And** recent startup and slot action messages can be read from that file
