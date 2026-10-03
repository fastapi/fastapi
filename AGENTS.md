# AGENTS.md

Context file for AI agents working on fastapi.

## Project Overview

fastapi is a Python project using Python (pip/setuptools).

**Key Info:**
- **Primary Language:** Python
- **Build System:** Python (pip/setuptools)
- **Test Framework:** pytest
- **Total Files:** 3181
- **Test Files:** 663
- **AI Readiness Score:** 93/100 (Agent-Optimized)

## Prerequisites

- **Python:** 3.9+ (or applicable language version)
- **Package Manager:** pip or uv (recommended)
- **Test Runner:** pytest

## Project Structure

```
fastapi/
├── pyproject.toml
├── src/                  # Source code
├── tests/                # Test suite (663 files)
└── README.md             # Project documentation
```

## Architecture Overview

### Key Components
- **Main Entry:** main.py, main.py, app.py, main.py, main.py
- **Test Suite:** 663 test files
- **Build Configuration:** pyproject.toml

### Design Principles

1. **Modularity** - Code organized by functionality with clear separation of concerns
2. **Testability** - Comprehensive test coverage across critical paths
3. **Clarity** - Explicit naming and structure for AI agent understanding
4. **Consistency** - Uniform patterns and conventions throughout codebase
5. **Maintainability** - Well-documented code with clear intent

## Repository Gotchas (Common Pitfalls)

- **Async Code Without Error Handling**: Async functions lack try/except blocks → Unhandled exceptions can crash the process

## Testing Patterns

- **Frameworks**: pytest
- **Test Files**: 663
- **Structure**: Tests organized in: async_tests, test_additional_responses, test_additional_status_codes, test_advanced_middleware, test_async_tests, test_authentication_error_status_code, test_background_tasks, test_behind_a_proxy, test_bigger_applications, test_body, test_body_fields, test_body_multiple_params, test_body_nested_models, test_body_updates, test_code_blocks, test_code_includes, test_complex_doc, test_conditional_openapi, test_configure_swagger_ui, test_cookie, test_cookie_param_models, test_cookie_params, test_cors, test_custom_docs_ui, test_custom_request_and_route, test_custom_response, test_dataclasses, test_debugging, test_dependencies, test_encoder, test_events, test_extending_openapi, test_extra_data_types, test_extra_models, test_file, test_first_steps, test_form, test_generate_clients, test_graphql, test_handling_errors, test_header, test_header_param_models, test_header_params, test_header_permalinks, test_html_links, test_json_base64_bytes, test_markdown_links, test_metadata, test_middleware, test_modules_same_name_body, test_openapi_callbacks, test_openapi_webhooks, test_opentelemetry, test_path, test_path_operation_advanced_configurations, test_path_operation_configurations, test_path_params, test_path_params_numeric_validations, test_python_types, test_query, test_query_param_models, test_query_params, test_query_params_str_validations, test_request_files, test_request_form_models, test_request_forms, test_request_forms_and_files, test_request_params, test_response_change_status_code, test_response_cookies, test_response_directly, test_response_headers, test_response_model, test_response_status_code, test_schema_extra_example, test_security, test_separate_openapi_schemas, test_server_sent_events, test_settings, test_sql_databases, test_static_files, test_stream_data, test_stream_json_lines, test_strict_content_type, test_sub_applications, test_telemetry, test_templates, test_testing, test_testing_dependencies, test_translation_fixer, test_tutorial, test_using_request_directly, test_validate_response_recursive, test_websockets, test_wsgi, tests
- **Coverage Tools**: Yes


## Development Workflow

### Initial Setup

```bash
git clone https://github.com/<owner>/fastapi.git
cd fastapi
pip install -e .              # Install in development mode
# or
uv sync --all-groups          # Using uv (recommended)
```

### Development Commands

#### Running Tests
```bash
pytest                        # Run all tests
pytest tests/                 # Run specific test directory
pytest -v                     # Verbose output with test names
pytest -x                     # Stop on first failure
pytest --cov                  # With coverage report
```

#### Code Quality
```bash
ruff check .                  # Lint with ruff
ruff format .                 # Format code
mypy .                        # Type checking (if configured)
```

## Code Style & Conventions

- **Naming:** Use Python conventions (snake_case for functions, PascalCase for classes)
- **Type Hints:** Yes (strongly encouraged)
- **Error Handling:** Yes
- **Logging:** No
- **Testing:** Yes - write tests alongside code changes

## Testing Strategy

**Framework:** pytest
**Test Files:** 663 found

Before committing:
1. Run the full test suite: `pytest`
2. Ensure all tests pass
3. Check type hints: `mypy .`
4. Format code: `ruff format .`

## Common Patterns

When contributing to this project:
1. Read existing code in the area you're modifying
2. Follow the established patterns and style
3. Write tests for new functionality
4. Use clear, descriptive variable and function names
5. Add docstrings for public APIs
6. Update tests when changing behavior

## What We Value

✅ Well-tested code with clear intent
✅ Consistent code style and naming conventions
✅ Code that is easy for AI agents to understand
✅ Clear, descriptive commit messages
✅ Modular, reusable components
✅ Comprehensive documentation

## What We Avoid

❌ Large functions doing multiple things
❌ Commented-out dead code
❌ Inconsistent naming or patterns
❌ Unclear error messages
❌ Unexplained magic numbers or strings
❌ Skipped tests or test TODOs

## AI Readiness Dimensions (Scoring)

This project is evaluated across 8 dimensions:

1. **Architecture** (20/100) - Code organization and modularity
2. **Testing** (15/100) - Test coverage and quality
3. **Dependencies** (12/100) - Dependency management
4. **Conventions** (8/100) - Consistent patterns
5. **Entry Points** (10/100) - Clear main/start locations
6. **Security** (10/100) - Input validation and error handling
7. **Build** (10/100) - Clear build/setup instructions
8. **Documentation** (8/100) - Code and project documentation

## Next Steps

Before making changes:
1. Read relevant source files to understand the existing code
2. Look at existing tests for similar functionality
3. Follow the patterns you see in the codebase
4. Write tests for your changes
5. Run `pytest` to verify nothing breaks
6. Run code quality checks: `ruff check . && mypy .`
7. Format your code: `ruff format .`

---

*Generated by Braxis - keeping AI agents in sync with your code*
