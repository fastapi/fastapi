import os

import typer
import uvicorn

from typing import Optional

from fastapi import __cliname__, __version__

app = typer.Typer()

@app.command()
def name():
    typer.echo(__cliname__)

@app.command()
def version():
    typer.echo(__version__)

@app.command("run", short_help="Run a development server.")
def run_command(
    app: Optional[str] = typer.Argument("main:app"),
    host: str = typer.Option("0.0.0.0", help="Put specific host"),
    port: int = typer.Option(8000, help="Put specific port"),
    level: str = typer.Option("info", help="Put specific level"),
    reload: bool = typer.Option(True, help="Reload option"),
    factory: bool = typer.Option(False, help="Factory Mode"),
):
    uvicorn.run(app, host=host, port=port, log_level=level, reload=reload)

@app.command("shell", short_help="Run a shell in the app context.")
def shell_command(
    app: str = typer.Option("main.py", help="Put specific app file"),
):
    os.system(f"python -i {app}")

@app.command()
def routes():
    typer.echo("Get all routes in main.py")

def main():
    app()

if __name__ == "__main__":
    main()
