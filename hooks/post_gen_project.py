import json
from pathlib import Path

# fmt: off
PROJECT_KIND: str = json.loads(r'''{{ cookiecutter.project_kind | jsonify }}''')
LICENSE: str = json.loads(r'''{{ cookiecutter.license | jsonify }}''')
INCLUDE_PRE_COMMIT: str = json.loads(r'''{{ cookiecutter.include_pre_commit | jsonify }}''')
# fmt: on


def remove(path: str) -> None:
    target = Path(path)
    if target.exists():
        target.unlink()


if PROJECT_KIND != "cli":
    remove("src/{{ cookiecutter.package_name }}/__main__.py")
    remove("tests/test_cli.py")

if LICENSE == "none":
    remove("LICENSE")

if INCLUDE_PRE_COMMIT != "yes":
    remove(".pre-commit-config.yaml")
