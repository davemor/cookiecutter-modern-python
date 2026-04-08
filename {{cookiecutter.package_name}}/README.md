# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Built with:

- [`uv`](https://docs.astral.sh/uv/) for Python/project/dependency management
- [`ruff`](https://docs.astral.sh/ruff/) for linting, formatting, and import sorting
- [`basedpyright`](https://docs.basedpyright.com/) for type checking
- [`pytest`](https://docs.pytest.org/) for tests
- [`pytest-cov`](https://pytest-cov.readthedocs.io/) for coverage

## Prerequisites

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) first.

## Quick start

Create the virtual environment and install dependencies:

```bash
uv sync
```

Run the sample code:

```bash
uv run python -m {{ cookiecutter.package_name }}
```

Run tests:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov
```

Lint and auto-fix:

```bash
uv run ruff check --fix .
```

Format code:

```bash
uv run ruff format .
```

Type-check:

```bash
uv run basedpyright
```

## Author

{{ cookiecutter.author_name }} — {{ cookiecutter.author_email }}
{% if cookiecutter.license != "none" %}
## License

{{ cookiecutter.license }}
{% endif %}
