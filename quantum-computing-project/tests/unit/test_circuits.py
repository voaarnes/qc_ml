"""Unit tests for circuit builders"""
import pytest
import numpy as np
from qiskit import QuantumCircuit

from src.circuits import QuantumCircuitBuilder, CircuitTemplates


def test_circuit_builder_initialization():
    """Test circuit builder initialization"""
    builder = QuantumCircuitBuilder(num_qubits=3)
    
    assert builder.num_qubits == 3
    assert builder.num_classical == 3
    assert isinstance(builder.circuit, QuantumCircuit)


def test_hadamard_gate():
    """Test Hadamard gate addition"""
    builder = QuantumCircuitBuilder(num_qubits=2)
    builder.add_hadamard(0)
    
    circuit = builder.build()
    ops = circuit.data
    
    assert len(ops) == 1
    assert ops[0].operation.name == 'h'


def test_cnot_gate():
    """Test CNOT gate addition"""
    builder = QuantumCircuitBuilder(num_qubits=2)
    builder.add_cnot(0, 1)
    
    circuit = builder.build()
    ops = circuit.data
    
    assert len(ops) == 1
    assert ops[0].operation.name == 'cx'


def test_bell_state_template():
    """Test Bell state template"""
    circuit = CircuitTemplates.bell_state(measure=False)
    
    assert circuit.num_qubits == 2
    ops = circuit.data
    
    # Should have H and CNOT
    assert len(ops) == 2
    assert ops[0].operation.name == 'h'
    assert ops[1].operation.name == 'cx'


def test_ghz_state_template():
    """Test GHZ state template"""
    n_qubits = 4
    circuit = CircuitTemplates.ghz_state(n_qubits, measure=False)
    
    assert circuit.num_qubits == n_qubits
    ops = circuit.data
    
    # Should have 1 H and (n-1) CNOTs
    assert len(ops) == n_qubits
    assert ops[0].operation.name == 'h'
    
    for i in range(1, n_qubits):
        assert ops[i].operation.name == 'cx'


def test_variational_ansatz():
    """Test variational ansatz creation"""
    circuit = CircuitTemplates.variational_ansatz(n_qubits=3, depth=2)
    
    assert circuit.num_qubits == 3
    assert len(circuit.parameters) > 0


def test_circuit_builder_chaining():
    """Test fluent interface chaining"""
    builder = QuantumCircuitBuilder(num_qubits=3)
    
    circuit = (builder
               .add_hadamard(0)
               .add_cnot(0, 1)
               .add_cnot(1, 2)
               .add_measurement()
               .build())
    
    assert circuit.num_qubits == 3
    # 3 gates + measurements
    assert len(circuit.data) > 3
