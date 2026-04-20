# Coding Standards

## Python Conventions
- **Naming**: Use `snake_case` for variables and functions, `PascalCase` for classes.
- **Docstrings**: All modules and public functions should have docstrings.
- **Type Hints**: Use type hints for function parameters and return values.

## Project-Specific Conventions
- **Configuration**: Use `config/config.yaml` for all configurable parameters.
- **Logging**: Use the `logger` module for all logging operations.
- **Error Handling**: Use specific exceptions and log errors appropriately.

## File Structure
- **Scripts**: All CLI scripts are located in `scripts/`.
- **Modules**: All reusable modules are located in `src/`.
- **Data**: Runtime data (models, corpus) are stored in `data/` (gitignored).

## Testing
- **Unit Tests**: Use `pytest` for unit testing.
- **Coverage**: Aim for at least 80% test coverage.
- **Test Data**: Store test data in `tests/data/`.

## Documentation
- **Docstrings**: Follow Google-style docstrings.
- **Comments**: Use comments sparingly, only for complex logic.
- **README**: Keep the README updated with usage examples and configuration details.
