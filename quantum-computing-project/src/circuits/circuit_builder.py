"""Quantum circuit builder with fluent interface"""
from typing import List, Optional, Union
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter


class QuantumCircuitBuilder:
    """Fluent interface for building quantum circuits"""
    
    def __init__(self, num_qubits: int, num_classical: Optional[int] = None):
        self.num_qubits = num_qubits
        self.num_classical = num_classical or num_qubits
        
        self.qreg = QuantumRegister(num_qubits, 'q')
        self.creg = ClassicalRegister(self.num_classical, 'c')
        self.circuit = QuantumCircuit(self.qreg, self.creg)
        
        self.parameters = []
    
    def add_hadamard(self, qubit: int):
        """Add Hadamard gate"""
        self.circuit.h(qubit)
        return self
    
    def add_pauli_x(self, qubit: int):
        """Add Pauli-X gate"""
        self.circuit.x(qubit)
        return self
    
    def add_pauli_y(self, qubit: int):
        """Add Pauli-Y gate"""
        self.circuit.y(qubit)
        return self
    
    def add_pauli_z(self, qubit: int):
        """Add Pauli-Z gate"""
        self.circuit.z(qubit)
        return self
    
    def add_cnot(self, control: int, target: int):
        """Add CNOT gate"""
        self.circuit.cx(control, target)
        return self
    
    def add_rotation_x(self, qubit: int, angle: Union[float, Parameter]):
        """Add X rotation gate"""
        if isinstance(angle, str):
            angle = Parameter(angle)
            self.parameters.append(angle)
        self.circuit.rx(angle, qubit)
        return self
    
    def add_rotation_y(self, qubit: int, angle: Union[float, Parameter]):
        """Add Y rotation gate"""
        if isinstance(angle, str):
            angle = Parameter(angle)
            self.parameters.append(angle)
        self.circuit.ry(angle, qubit)
        return self
    
    def add_rotation_z(self, qubit: int, angle: Union[float, Parameter]):
        """Add Z rotation gate"""
        if isinstance(angle, str):
            angle = Parameter(angle)
            self.parameters.append(angle)
        self.circuit.rz(angle, qubit)
        return self
    
    def add_toffoli(self, control1: int, control2: int, target: int):
        """Add Toffoli gate"""
        self.circuit.ccx(control1, control2, target)
        return self
    
    def add_swap(self, qubit1: int, qubit2: int):
        """Add SWAP gate"""
        self.circuit.swap(qubit1, qubit2)
        return self
    
    def add_barrier(self, qubits: Optional[List[int]] = None):
        """Add barrier"""
        if qubits is None:
            self.circuit.barrier()
        else:
            self.circuit.barrier(qubits)
        return self
    
    def add_measurement(self, qubit: Optional[int] = None, classical: Optional[int] = None):
        """Add measurement"""
        if qubit is None:
            self.circuit.measure_all()
        else:
            classical = classical or qubit
            self.circuit.measure(qubit, classical)
        return self
    
    def add_custom_gate(self, gate, qubits: List[int], params: Optional[List] = None):
        """Add custom gate"""
        if params:
            self.circuit.append(gate(*params), qubits)
        else:
            self.circuit.append(gate, qubits)
        return self
    
    def create_entangled_pair(self, qubit1: int, qubit2: int):
        """Create Bell state"""
        self.add_hadamard(qubit1)
        self.add_cnot(qubit1, qubit2)
        return self
    
    def create_ghz_state(self):
        """Create GHZ state for all qubits"""
        self.add_hadamard(0)
        for i in range(1, self.num_qubits):
            self.add_cnot(0, i)
        return self
    
    def build(self) -> QuantumCircuit:
        """Build and return the circuit"""
        return self.circuit
    
    def draw(self, output: str = 'mpl', **kwargs):
        """Draw the circuit"""
        return self.circuit.draw(output=output, **kwargs)
