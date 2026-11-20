# Contributing to FastAPI

First, thank you for considering contributing to FastAPI! 🎉

FastAPI is a community-driven project and we welcome contributions of all kinds:
- 📝 **Documentation** improvements (typos, clarifications, new guides)
- 🐛 **Bug reports** and **feature requests**
- 💻 **Code contributions** (bug fixes, new features)
- 🌐 **Translations** of the documentation
- 💬 **Helping others** in GitHub Discussions and Discord

---

## Quick Links

| Resource | Purpose |
|----------|---------|
| [GitHub Discussions](https://github.com/fastapi/fastapi/discussions) | Ask questions, propose ideas, get help |
| [Discord Chat](https://discord.com/invite/VQjSZaeJmf) | Community chat (not for technical questions) |
| [Issue Tracker](https://github.com/fastapi/fastapi/issues) | Bug reports and feature requests |
| [Documentation](https://fastapi.tiangolo.com) | Official docs (auto-generated from this repo) |
| [Contributing Guide (External)](https://tiangolo.com/open-source/contributing/) | Detailed development guide by the author |

---

## Ways to Contribute

### 📝 Documentation Contributions

Documentation improvements are **especially welcome** and are a great way to start contributing!

#### What you can do:
- Fix typos, grammar, or unclear explanations
- Add missing examples or clarify existing ones
- Write new tutorials or how-to guides
- Improve the [README](README.md) or this CONTRIBUTING guide
- Translate documentation to other languages

#### How to preview documentation changes locally:

```bash
# Install uv (if not already installed)
# https://docs.astral.sh/uv/getting-started/installation/

# Clone your fork and install dependencies
uv sync

# Start the live-reloading docs server
uv run ./scripts/docs.py live
```

This serves the documentation at **http://127.0.0.1:8008** with live reload - edit any `.md` file in `docs/en/docs/` and see changes instantly.

#### Documentation Structure:
```
docs/en/docs/
├── index.md              # Homepage
├── tutorial/             # Step-by-step tutorial (main learning path)
├── advanced/             # Advanced topics
├── how-to/               # Specific task guides
├── reference/            # API reference
├── deployment/           # Deployment guides
├── contributing.md       # This file (in-repo version)
├── help-fastapi.md       # Community help guide
└── ...other topic files
```

> **Note**: Many code examples in the docs are **injected from `docs_src/`** - they're actual runnable Python files tested by the test suite. See [tiangolo.com - Docs Structure](https://tiangolo.com/open-source/contributing/#docs-structure) for details.

---

### 🐛 Reporting Bugs

Before creating a bug report:
1. **Search existing issues** - your issue might already be reported
2. **Check the documentation** - it might be expected behavior
3. **Try the latest version** - the bug might be fixed

When creating a bug report, include:
- **FastAPI version** (`fastapi --version` or `pip show fastapi`)
- **Python version** (`python --version`)
- **Minimal reproducible code** - a complete, small example
- **Expected vs actual behavior**
- **Full error traceback** (if applicable)

---

### 💡 Feature Requests

Feature requests are welcome! Please:
1. **Start a GitHub Discussion** first (category: "Ideas")
2. Explain the **problem** you're trying to solve, not just the solution
3. Describe **use cases** and **benefits**
4. Consider if it fits FastAPI's design philosophy (simple, type-safe, standard Python)

---

### 💻 Code Contributions

#### Prerequisites
- Python 3.9+
- [uv](https://docs.astral.sh/uv/) for dependency management
- Git

#### Development Setup

```bash
# 1. Fork the repo on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/fastapi.git
cd fastapi

# 3. Install dependencies
uv sync

# 4. Install pre-commit hooks (runs formatting/linting before commits)
uv run prek install
```

#### Running Tests

```bash
# Run all tests
bash scripts/test.sh

# Or run pytest directly with options
uv run pytest -x -v                    # Stop on first failure, verbose
uv run pytest tests/test_tutorial.py   # Run specific test file
uv run pytest -k "test_name"           # Run tests matching pattern
```

#### Code Style & Quality

FastAPI uses automated tools (run via `prek` pre-commit hooks):
- **Ruff** - linting and formatting (replaces Black, isort, flake8)
- **mypy** - static type checking

Run manually:
```bash
uv run ruff check .      # Lint
uv run ruff format .     # Format
uv run mypy .            # Type check
```

#### Pull Request Process

1. **Start a Discussion** (for non-trivial changes) - explain what and why
2. **Create a branch** from `master` - use descriptive name: `fix/typo-readme`, `feat/new-dependency-injection`
3. **Make your changes** - keep commits focused and atomic
4. **Run tests and linting** - ensure everything passes locally
5. **Update documentation** if your change affects user-facing behavior
6. **Open a Pull Request** - fill out the PR template
7. **Wait for review** - maintainers will review and may request changes

> **Important**: PRs from non-team members **cannot modify** `pyproject.toml` or `uv.lock` (supply chain security). If you need a new dependency, open a Discussion first.

---

### 🌐 Translations

FastAPI documentation is translated by the community! 

See [Translations Guide](https://fastapi.tiangolo.com/translations/) for:
- How to start a new language
- How to contribute to existing translations
- Translation workflow and tools

Translation files are in `docs/{lang}/docs/` (e.g., `docs/es/docs/` for Spanish).

---

## Development Guidelines

### Design Principles

FastAPI follows these core principles:
1. **Standard Python types** - Use type hints, not custom decorators/schemas
2. **Automatic validation** - Declare once, get validation + docs + editor support
3. **High performance** - Built on Starlette and Pydantic
4. **Developer experience** - Great editor support, clear errors, minimal boilerplate
5. **Standards-based** - OpenAPI, JSON Schema, OAuth2, etc.

### Automated Code and AI Tools

You're encouraged to use AI/LLM tools to contribute efficiently. However:

> **Human effort in a PR must exceed the effort required to review it.**

- Don't submit PRs that are purely AI-generated without meaningful human review
- Don't copy-paste LLM output as PR descriptions or comments
- Automated PRs that waste maintainer time will be closed
- **Use tools wisely** - they're powerful, but you're responsible for the result

See [tiangolo.com - Automated Code and AI](https://tiangolo.com/open-source/contributing/#automated-code-and-ai) for full guidelines.

---

## Getting Help

| Question Type | Best Place |
|---------------|------------|
| "How do I...?" | [GitHub Discussions → Questions](https://github.com/fastapi/fastapi/discussions/new?category=questions) |
| "I found a bug" | [GitHub Issues](https://github.com/fastapi/fastapi/issues/new/choose) |
| "I have an idea" | [GitHub Discussions → Ideas](https://github.com/fastapi/fastapi/discussions/new?category=ideas) |
| "Can you review my PR?" | Ping `@fastapi/maintainers` in the PR |
| General chat | [Discord](https://discord.com/invite/VQjSZaeJmf) |

---

## Recognition

All contributors are recognized in:
- [FastAPI People](https://fastapi.tiangolo.com/fastapi-people/) page
- Release notes for significant contributions
- GitHub's contributor graphs

---

## License

By contributing to FastAPI, you agree that your contributions will be licensed under the **MIT License** (same as the project).

---

## Thank You! 🙏

Every contribution matters - whether it's fixing a typo, writing a tutorial, or implementing a major feature. FastAPI exists because of contributors like you!

**Questions?** Open a [GitHub Discussion](https://github.com/fastapi/fastapi/discussions/new?category=questions) or ask in [Discord](https://discord.com/invite/VQjSZaeJmf).