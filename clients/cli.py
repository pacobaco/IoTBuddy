import time
from pathlib import Path
import typer
import yaml
from iotbuddy.core import IoTBuddy

app = typer.Typer(help="IoT Buddy command-line interface")


@app.command()
def simulate(
    config: Path = typer.Option(Path("config/default.yaml"), help="Config file"),
    minutes: int = typer.Option(5, help="Duration in minutes"),
    seat: str = typer.Option("default", help="Seat ID"),
):
    """Run simulated EEG neurofeedback + IoT control."""
    with open(config) as f:
        cfg = yaml.safe_load(f)
    buddy = IoTBuddy(cfg)
    buddy.run_simulated(duration_min=minutes, seat_id=seat)


@app.command()
def serve(
    config: Path = typer.Option(Path("config/default.yaml"), help="Config file"),
):
    """Start the companion and keep it running."""
    with open(config) as f:
        cfg = yaml.safe_load(f)
    buddy = IoTBuddy(cfg)
    buddy.start()
    typer.echo("Buddy running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        buddy.running = False
        typer.echo("\nStopped.")


if __name__ == "__main__":
    app()
