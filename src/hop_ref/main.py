#!/usr/bin/env python
from pathlib import Path
import typer
from typing_extensions import Annotated
from hop_ref.crew import LinkedInContentStudio

app = typer.Typer(
    help="LinkedIn Content Studio - Transform ideas into high-engagement LinkedIn posts",
    add_completion=False
)

@app.command()
def run(
    topic: Annotated[
        str,
        typer.Option(prompt="What topic would you like to create content about?")
    ] = None,
    audience: Annotated[
        str,
        typer.Option(prompt="Who is your target audience?")
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show detailed agent reasoning")
    ] = False,
    output_dir: Annotated[
        str,
        typer.Option("--output-dir", "-o", help="Output directory (default: output/)")
    ] = "output"
):
    """Run the LinkedIn Content Studio crew"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    inputs = {'topic': topic, 'audience': audience}

    try:
        typer.echo(f"\n{'='*70}")
        typer.secho("  LinkedIn Content Studio", fg=typer.colors.BRIGHT_BLUE, bold=True)
        typer.echo(f"{'='*70}\n")
        typer.echo(f"Topic: {topic}")
        typer.echo(f"Audience: {audience}\n")

        if verbose:
            typer.echo("Workflow: Hook Crafter → Value Builder → Engagement Architect → Format Alchemist\n")

        typer.secho("Starting content creation...\n", fg=typer.colors.GREEN)

        LinkedInContentStudio().crew().kickoff(inputs=inputs)

        carousel_path = output_path / "carousel_outline.md"

        typer.echo(f"\n{'='*70}")
        typer.secho("✓ Complete!", fg=typer.colors.GREEN, bold=True)
        typer.echo(f"{'='*70}\n")

        if carousel_path.exists():
            typer.echo(f"Carousel outline: {carousel_path.absolute()}\n")

    except Exception as e:
        typer.secho(f"\n✗ Error: {e}", fg=typer.colors.RED, bold=True)
        typer.echo("\nTroubleshooting: Check .env file contains valid API keys\n")
        raise typer.Exit(code=1)

def main():
    app()
