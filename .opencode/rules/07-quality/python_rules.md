# Python Quality Rules

## Mandatory Rules

### Docstrings
- **All public functions and classes must have docstrings.**
- **Follow Google-style docstrings** for consistency.
- **Include parameter types and return values** in docstrings.

### Type Hints
- **All function parameters and return values must have type hints.**
- **Use `typing` module** for complex types (e.g., `List`, `Dict`, `Optional`).
- **Avoid `Any` type** unless absolutely necessary.

### Testing
- **All new features must include unit tests.**
- **Aim for at least 80% test coverage.**
- **Use `pytest` for writing tests.**
- **Store test data in `tests/data/`.**

### Code Style
- **Follow PEP 8** for Python code style.
- **Use `snake_case` for variables and functions.**
- **Use `PascalCase` for classes.**
- **Limit line length to 100 characters.**

### Error Handling
- **Use specific exceptions** instead of generic `Exception`.
- **Log errors appropriately** using the `logger` module.
- **Include error messages** that are descriptive and helpful.

### Logging
- **Use the `logger` module** for all logging operations.
- **Log levels**: Use `DEBUG` for development, `INFO` for production, `ERROR` for errors.
- **Log format**: Include timestamp, log level, and message.

### Configuration
- **Use `config/config.yaml`** for all configurable parameters.
- **Validate configuration** before using it in the code.
- **Document configuration options** in the README.

### Code Review Checklist
- [ ] Docstrings are present and descriptive.
- [ ] Type hints are used consistently.
- [ ] No duplicate code.
- [ ] Error handling is appropriate.
- [ ] Logging is used effectively.
- [ ] Configuration is validated.
- [ ] Tests are included and passing.
- [ ] Code follows PEP 8.

## Recommended Practices

### Modularity
- **Keep modules small and focused.**
- **Separate concerns** into different modules.
- **Avoid circular imports.**

### Performance
- **Optimize critical paths** for performance.
- **Use efficient data structures** (e.g., sets for membership tests).
- **Avoid premature optimization.**

### Documentation
- **Keep the README updated** with usage examples and configuration details.
- **Document complex logic** with comments.
- **Use examples** to illustrate usage.

### Version Control
- **Use Git** for version control.
- **Commit messages**: Use descriptive commit messages.
- **Branching**: Use feature branches for new features.

### Security
- **Avoid hardcoding secrets** in the code.
- **Use environment variables** for sensitive data.
- **Validate inputs** to prevent injection attacks.
