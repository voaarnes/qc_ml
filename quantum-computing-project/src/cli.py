#!/usr/bin/env python3
"""Command-line interface for quantum computing project"""
import click
import json
from rich.console import Console
from rich.table import Table
from src.backends import BackendManager
from src.circuits import CircuitTemplates

console = Console()


@click.group()
def cli():
    """Quantum Computing Project CLI"""
    pass


@cli.command()
def list_backends():
    """List available quantum backends"""
    manager = BackendManager()
    
    table = Table(title="Available Quantum Backends")
    table.add_column("Backend", style="cyan")
    table.add_column("Type", style="magenta")
    
    for backend_name in manager.list_backends():
        backend_type = "Simulator" if "sim" in backend_name.lower() else "Hardware"
        table.add_row(backend_name, backend_type)
    
    console.print(table)


@cli.command()
@click.option('--circuit', type=click.Choice(['bell', 'ghz', 'qft']), default='bell')
@click.option('--backend', default='aer_simulator')
@click.option('--shots', default=1024)
def run(circuit, backend, shots):
    """Run a quantum circuit"""
    manager = BackendManager()
    
    # Create circuit
    if circuit == 'bell':
        qc = CircuitTemplates.bell_state()
    elif circuit == 'ghz':
        qc = CircuitTemplates.ghz_state(3)
    elif circuit == 'qft':
        qc = CircuitTemplates.quantum_fourier_transform(3)
    
    console.print(f"[bold green]Running {circuit} circuit on {backend}...[/bold green]")
    
    # Run circuit
    result = manager.run_circuit(qc, backend_name=backend, shots=shots)
    counts = result.get_counts()
    
    # Display results
    table = Table(title=f"Results ({shots} shots)")
    table.add_column("State", style="cyan")
    table.add_column("Count", style="magenta")
    table.add_column("Probability", style="yellow")
    
    for state, count in sorted(counts.items()):
        prob = count / shots
        table.add_row(state, str(count), f"{prob:.3f}")
    
    console.print(table)


if __name__ == "__main__":
    cli()
