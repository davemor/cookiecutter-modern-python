from typing import Annotated

import typer

from {{ cookiecutter.package_name }} import hello

app = typer.Typer()


@app.command()
def main(name: Annotated[str, typer.Option(help="Name to greet.")] = "world") -> None:
    typer.echo(hello(name))


if __name__ == "__main__":
    app()
