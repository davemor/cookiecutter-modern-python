import typer

from {{ cookiecutter.package_name }} import hello

app = typer.Typer()


@app.command()
def main(name: str = typer.Option("world", help="Name to greet.")) -> None:
    typer.echo(hello(name))


if __name__ == "__main__":
    app()
