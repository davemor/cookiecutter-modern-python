from __future__ import annotations

import os
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

import pytest
from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter

TEMPLATE_ROOT = Path(__file__).parents[1]


def render(tmp_path: Path, **context: str) -> Path:
    output_dir = tmp_path / "output"
    replay_dir = tmp_path / "replay"
    cookiecutters_dir = tmp_path / "cookiecutters"
    config_file = tmp_path / "cookiecutter-config.yaml"

    output_dir.mkdir()
    config_file.write_text(
        f"cookiecutters_dir: {cookiecutters_dir}\nreplay_dir: {replay_dir}\n",
        encoding="utf-8",
    )

    rendered = cookiecutter(
        str(TEMPLATE_ROOT),
        no_input=True,
        output_dir=str(output_dir),
        extra_context=context,
        config_file=str(config_file),
    )
    return Path(rendered)


def read_pyproject(project: Path) -> dict[str, object]:
    with (project / "pyproject.toml").open("rb") as file:
        return tomllib.load(file)


def run(project: Path, *command: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("VIRTUAL_ENV", None)
    environment["XDG_CACHE_HOME"] = str(project / ".cache")
    result = subprocess.run(
        command,
        cwd=project,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Command failed: {' '.join(command)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    return result


@pytest.mark.parametrize("license_name", ["MIT", "Apache-2.0", "none"])
def test_license_variants(tmp_path: Path, license_name: str) -> None:
    project = render(
        tmp_path,
        project_name=f"{license_name} Project",
        license=license_name,
    )
    metadata = read_pyproject(project)["project"]

    if license_name == "none":
        assert "license" not in metadata
        assert "license-files" not in metadata
        assert not (project / "LICENSE").exists()
    else:
        assert metadata["license"] == license_name
        assert metadata["license-files"] == ["LICENSE"]
        assert (project / "LICENSE").is_file()
        assert license_name.split("-")[0] in (project / "LICENSE").read_text(encoding="utf-8")


def test_library_without_hooks(tmp_path: Path) -> None:
    project = render(
        tmp_path,
        project_name="Example Library",
        project_kind="library",
        include_pre_commit="no",
        repository_url="https://github.com/example/example-library",
    )
    metadata = read_pyproject(project)

    assert "scripts" not in metadata["project"]
    assert metadata["project"]["dependencies"] == []
    assert metadata["project"]["urls"]["Repository"].endswith("example-library")
    assert not (project / "src/example_library/__main__.py").exists()
    assert not (project / "tests/test_cli.py").exists()
    assert not (project / ".pre-commit-config.yaml").exists()
    assert all("prek" not in dependency for dependency in metadata["dependency-groups"]["dev"])


def test_invalid_import_name_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(FailedHookException):
        render(
            tmp_path,
            project_name="Invalid Package",
            package_name="123-not-python",
        )


@pytest.mark.parametrize(
    ("project_kind", "include_pre_commit"),
    [("cli", "yes"), ("library", "no")],
)
def test_generated_project(tmp_path: Path, project_kind: str, include_pre_commit: str) -> None:
    project_name = "Example CLI" if project_kind == "cli" else "Example Library"
    project = render(
        tmp_path,
        project_name=project_name,
        project_kind=project_kind,
        include_pre_commit=include_pre_commit,
    )

    run(project, "uv", "sync")
    assert (project / "uv.lock").is_file()
    run(project, "uv", "lock", "--check")
    run(project, "uv", "run", "ruff", "check", ".")
    run(project, "uv", "run", "ruff", "format", "--check", ".")
    run(project, "uv", "run", "basedpyright")
    run(project, "uv", "run", "pytest", "--cov", "--cov-report=term-missing")
    run(project, "uv", "build")

    wheel = next((project / "dist").glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        wheel_files = archive.namelist()
    expected_package = "example_cli" if project_kind == "cli" else "example_library"
    assert f"{expected_package}/py.typed" in wheel_files
    assert any(path.endswith("/licenses/LICENSE") for path in wheel_files)

    if project_kind == "cli":
        module_result = run(
            project,
            "uv",
            "run",
            "python",
            "-m",
            "example_cli",
            "--name",
            "Ada",
        )
        assert module_result.stdout == "Hello, Ada!\n"

        command_result = run(project, "uv", "run", "example-cli", "--name", "Ada")
        assert command_result.stdout == "Hello, Ada!\n"

        wheel_result = run(
            project,
            "uv",
            "run",
            "--isolated",
            "--no-project",
            "--with",
            str(wheel),
            "example-cli",
            "--name",
            "Wheel",
        )
        assert wheel_result.stdout == "Hello, Wheel!\n"

        run(project, "git", "init")
        run(project, "git", "add", ".")
        run(project, "uv", "run", "prek", "run", "--all-files")
    else:
        wheel_result = run(
            project,
            "uv",
            "run",
            "--isolated",
            "--no-project",
            "--with",
            str(wheel),
            "python",
            "-c",
            "from example_library import hello; assert hello() == 'Hello, world!'",
        )
        assert wheel_result.returncode == 0


@pytest.mark.parametrize("python_version", ["3.14", "3.13", "3.12"])
def test_supported_python_choices(tmp_path: Path, python_version: str) -> None:
    project = render(
        tmp_path,
        project_name=f"Python {python_version} Project",
        python_version=python_version,
    )
    metadata = read_pyproject(project)

    assert (project / ".python-version").read_text(encoding="utf-8").strip() == python_version
    assert metadata["project"]["requires-python"] == f">={python_version}"
    assert metadata["tool"]["ruff"]["target-version"] == f"py{python_version.replace('.', '')}"
    assert metadata["tool"]["basedpyright"]["pythonVersion"] == python_version
    assert sys.version_info >= (3, 12)
