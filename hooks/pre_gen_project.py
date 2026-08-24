import json
import keyword
import re
import sys

# fmt: off
PROJECT_SLUG: str = json.loads(r'''{{ cookiecutter.project_slug | jsonify }}''')
DISTRIBUTION_NAME: str = json.loads(r'''{{ cookiecutter.distribution_name | jsonify }}''')
PACKAGE_NAME: str = json.loads(r'''{{ cookiecutter.package_name | jsonify }}''')
# fmt: on

NORMALIZED_NAME = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


if not NORMALIZED_NAME.fullmatch(PROJECT_SLUG):
    fail(
        "project_slug must contain only ASCII letters, digits, dots, underscores, and hyphens, "
        "and must start and end with a letter or digit"
    )

if not NORMALIZED_NAME.fullmatch(DISTRIBUTION_NAME):
    fail(
        "distribution_name must contain only ASCII letters, digits, dots, underscores, and "
        "hyphens, and must start and end with a letter or digit"
    )

if not PACKAGE_NAME.isidentifier() or keyword.iskeyword(PACKAGE_NAME):
    fail(f"package_name {PACKAGE_NAME!r} is not a valid Python import identifier")
