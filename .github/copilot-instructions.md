# GitHub Copilot Instructions

## General Guidelines
- Generate clean, readable, production-ready code
- Follow SOLID principles
- Avoid hard-coded values
- Prefer configuration-driven logic

## Code Style
- Use meaningful variable and function names
- Follow language-specific best practices
- Add comments only where business logic exists

## Error Handling
- Handle all edge cases
- Never suppress exceptions silently
- Return meaningful error messages

## Testing
- Always generate unit-testable code
- Prefer pure functions where possible

## Backend Instructions

### API Design
- Use RESTful conventions
- Validate all request inputs
- Return proper HTTP status codes

### Security
- Do not expose sensitive data
- Sanitize user inputs
- Follow OWASP best practices

### Logging
- Log errors and critical business events
- Do not log PII or secrets

### Performance
- Avoid unnecessary database calls
- Prefer pagination for list APIs