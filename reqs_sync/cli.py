import click
from .r2toml import parse_requirements, update_pyproject_toml
from pathlib import Path


@click.group()
@click.version_option()
def cli():
    "Convert requirements.in to pyproject.toml dependencies"


@cli.command(name="reqs-to-toml")
@click.argument(
    "requirements_file",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-o",
    "--output",
    help="Output pyproject.toml file path",
    type=click.Path(path_type=Path),
    default="pyproject.toml",
)
@click.option(
    "--dev",
    is_flag=True,
    help="Sync to dev dependencies instead of project dependencies",
)
def reqs_to_toml(requirements_file, output, dev):
    "Convert requirements.in file to pyproject.toml dependencies"
    try:
        dependencies = parse_requirements(requirements_file)
        update_pyproject_toml(dependencies, output, dev=dev)
        target = "dev dependencies" if dev else "dependencies"
        click.echo(f"Successfully updated {output} with {len(dependencies)} {target}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()
