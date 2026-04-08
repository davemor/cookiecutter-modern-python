from {{ cookiecutter.package_name }} import hello


def test_hello() -> None:
    assert hello() == "Hello, world!"
