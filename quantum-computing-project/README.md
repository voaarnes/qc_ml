# Quantum Computing Project

A comprehensive, modular, and future-proof quantum computing project built with Qiskit and supporting multiple quantum computing paradigms.

## Features

- **Modular Architecture**: Easily extensible design supporting multiple quantum algorithms and applications
- **Hardware Agnostic**: Simulator-first development with seamless hardware integration
- **Multiple Paradigms**: Support for VQE, QAOA, QML, Grover's, Shor's, and custom algorithms
- **Backend Flexibility**: Easy switching between simulators and real quantum hardware
- **REST API**: FastAPI-based service for quantum computations
- **Visualization**: Rich visualization tools for circuits and results
- **Testing**: Comprehensive test suite with unit and integration tests

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/quantum-computing-project.git
cd quantum-computing-project

# Install dependencies
make install

# For development
make install-dev
```

## Quick Start

```python
from src.backends import BackendManager
from src.circuits import QuantumCircuitBuilder
from src.algorithms import VQE, QAOA, GroverSearch

# Initialize backend manager
backend_manager = BackendManager()
backend = backend_manager.get_backend("aer_simulator")

# Create a simple quantum circuit
builder = QuantumCircuitBuilder(num_qubits=2)
circuit = builder.add_hadamard(0).add_cnot(0, 1).build()

# Run the circuit
result = backend.run(circuit, shots=1000)
print(result.get_counts())
```

## Project Structure

```
quantum-computing-project/
├── src/
│   ├── algorithms/      # Quantum algorithms (VQE, QAOA, Grover, etc.)
│   ├── circuits/        # Circuit builders and templates
│   ├── backends/        # Backend management and abstraction
│   ├── utils/           # Utility functions and helpers
│   └── applications/    # Application-specific modules
│       ├── qml/         # Quantum Machine Learning
│       ├── optimization/# Quantum Optimization
│       ├── cryptography/# Quantum Cryptography
│       └── simulation/  # Quantum Simulation
├── tests/               # Test suite
├── notebooks/           # Jupyter notebooks for experiments
├── configs/             # Configuration files
└── docs/               # Documentation
```

## Usage Examples

### Running VQE for H2 Molecule

```python
from src.applications.simulation import MolecularSimulation

sim = MolecularSimulation()
energy = sim.compute_ground_state_energy("H2", method="VQE")
print(f"Ground state energy: {energy}")
```

### Quantum Machine Learning

```python
from src.applications.qml import QuantumClassifier

qc = QuantumClassifier(n_qubits=4)
qc.fit(X_train, y_train)
predictions = qc.predict(X_test)
```

### API Usage

```bash
# Start the API server
make run-api

# Send a request
curl -X POST "http://localhost:8000/api/v1/circuits/run" \
  -H "Content-Type: application/json" \
  -d '{"circuit": "qasm_string", "backend": "aer_simulator", "shots": 1000}'
```

## Testing

```bash
# Run all tests
make test

# Run specific test
pytest tests/unit/test_circuits.py -v
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
