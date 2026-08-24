# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Built with:

- [`uv`](https://docs.astral.sh/uv/) for Python, project, dependency, and build management
- [`ruff`](https://docs.astral.sh/ruff/) for linting and formatting
- [`basedpyright`](https://docs.basedpyright.com/) for type checking
- [`pytest`](https://docs.pytest.org/) and [`pytest-cov`](https://pytest-cov.readthedocs.io/) for tests and coverage
{% if cookiecutter.project_kind == "cli" %}- [`typer`](https://typer.tiangolo.com/) for the command-line interface
{% endif %}{% if cookiecutter.include_pre_commit == "yes" %}- A pre-commit compatible hook configuration run with [`prek`](https://github.com/j178/prek)
{% endif %}
## Prerequisite

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

## Quick start

Create the environment, install the project and development dependencies, and
create `uv.lock`:

```bash
uv sync
```

Commit `uv.lock` so local development and CI use the same dependency versions.
{% if cookiecutter.project_kind == "cli" %}
Run the command:

```bash
uv run {{ cookiecutter.project_slug }} --name world
```
{% else %}
Import the library:

```python
from {{ cookiecutter.package_name }} import hello

print(hello())
```
{% endif %}
## Quality checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
uv run pytest --cov
uv build
```

To apply safe lint fixes and formatting:

```bash
uv run ruff check --fix .
uv run ruff format .
```
{% if cookiecutter.include_pre_commit == "yes" %}
## Git hooks

Install the pre-commit and pre-push hooks:

```bash
uv run prek install --hook-type pre-commit --hook-type pre-push
```

Run every hook manually:

```bash
uv run prek run --all-files
```
{% endif %}
## Author

{{ cookiecutter.author_name }} — [{{ cookiecutter.author_email }}](mailto:{{ cookiecutter.author_email }})
{% if cookiecutter.license != "none" %}
## Licence

{{ cookiecutter.license }}. See `LICENSE`.
{% endif %}
