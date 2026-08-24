from typer.testing import CliRunner

from {{ cookiecutter.package_name }}.__main__ import app

runner = CliRunner()


def test_cli() -> None:
    result = runner.invoke(app, ["--name", "Ada"])

    assert result.exit_code == 0
    assert result.stdout == "Hello, Ada!\n"
