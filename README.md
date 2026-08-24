# Modern Python Cookiecutter

An opinionated, minimal Cookiecutter template for modern Python CLI applications
and libraries.

Generated projects use:

- [`uv`](https://docs.astral.sh/uv/) for Python, dependency, build, and project
  management
- [`uv_build`](https://docs.astral.sh/uv/concepts/build-backend/) as the build
  backend
- [`ruff`](https://docs.astral.sh/ruff/) for linting and formatting
- [`basedpyright`](https://docs.basedpyright.com/) for type checking
- [`pytest`](https://docs.pytest.org/) and
  [`pytest-cov`](https://pytest-cov.readthedocs.io/) for testing and coverage
- GitHub Actions for continuous integration
- Optional [pre-commit](https://pre-commit.com/) compatible hooks, run with
  [`prek`](https://github.com/j178/prek)

## Create a project

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/), then run:

```bash
uvx cookiecutter gh:davemor/cookiecutter-modern-python
```

The generated project includes a `src/` layout, an explicit build backend,
Python version pin, dependency lock workflow, quality configuration, tests, and
CI. Choose between a Typer CLI application and an importable library during
generation.

## Develop the template

```bash
uv sync
uv run pytest
```

The test suite renders the supported template variants and exercises the
generated projects as installed packages.
