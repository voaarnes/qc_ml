"""Pre-built circuit templates for common quantum algorithms"""
import numpy as np
from typing import List, Optional
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT, HGate, ZGate, CXGate


class CircuitTemplates:
    """Collection of quantum circuit templates"""
    
    @staticmethod
    def bell_state(measure: bool = True) -> QuantumCircuit:
        """Create a Bell state circuit"""
        qr = QuantumRegister(2, 'q')
        cr = ClassicalRegister(2, 'c')
        circuit = QuantumCircuit(qr, cr)
        
        circuit.h(qr[0])
        circuit.cx(qr[0], qr[1])
        
        if measure:
            circuit.measure(qr, cr)
        
        return circuit
    
    @staticmethod
    def ghz_state(n_qubits: int, measure: bool = True) -> QuantumCircuit:
        """Create a GHZ state circuit"""
        qr = QuantumRegister(n_qubits, 'q')
        cr = ClassicalRegister(n_qubits, 'c')
        circuit = QuantumCircuit(qr, cr)
        
        circuit.h(qr[0])
        for i in range(1, n_qubits):
            circuit.cx(qr[0], qr[i])
        
        if measure:
            circuit.measure(qr, cr)
        
        return circuit
    
    @staticmethod
    def quantum_fourier_transform(n_qubits: int) -> QuantumCircuit:
        """Create a QFT circuit"""
        circuit = QuantumCircuit(n_qubits)
        circuit.append(QFT(n_qubits), range(n_qubits))
        return circuit
    
    @staticmethod
    def grover_oracle(marked_states: List[str]) -> QuantumCircuit:
        """Create a Grover oracle for marked states"""
        n_qubits = len(marked_states[0])
        oracle = QuantumCircuit(n_qubits)
        
        for state in marked_states:
            # Add X gates for 0s in the state
            for i, bit in enumerate(state):
                if bit == '0':
                    oracle.x(i)
            
            # Multi-controlled Z gate
            oracle.h(n_qubits - 1)
            oracle.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            oracle.h(n_qubits - 1)
            
            # Undo X gates
            for i, bit in enumerate(state):
                if bit == '0':
                    oracle.x(i)
        
        return oracle
    
    @staticmethod
    def variational_ansatz(n_qubits: int, depth: int = 1) -> QuantumCircuit:
        """Create a variational ansatz circuit"""
        from qiskit.circuit import Parameter
        
        circuit = QuantumCircuit(n_qubits)
        params = []
        
        for d in range(depth):
            # Rotation layer
            for i in range(n_qubits):
                theta = Parameter(f'θ_{d}_{i}')
                params.append(theta)
                circuit.ry(theta, i)
            
            # Entanglement layer
            for i in range(n_qubits - 1):
                circuitcx(i, i + 1)
            if n_qubits > 2:
                circuit.cx(n_qubits - 1, 0)
        
        return circuit
    
    @staticmethod
    def quantum_phase_estimation(n_precision: int) -> QuantumCircuit:
        """Create a quantum phase estimation circuit template"""
        # Precision qubits + 1 eigenstate qubit
        n_qubits = n_precision + 1
        
        qr_precision = QuantumRegister(n_precision, 'precision')
        qr_eigenstate = QuantumRegister(1, 'eigenstate')
        cr = ClassicalRegister(n_precision, 'measurement')
        
        circuit = QuantumCircuit(qr_precision, qr_eigenstate, cr)
        
        # Initialize precision qubits in superposition
        for qubit in qr_precision:
            circuit.h(qubit)
        
        # Controlled unitary operations
        repetitions = 1
        for counting_qubit in range(n_precision):
            for _ in range(repetitions):
                # This is a template - replace with actual controlled unitary
                circuit.cp(np.pi/4, qr_precision[counting_qubit], qr_eigenstate[0])
            repetitions *= 2
        
        # Inverse QFT on precision qubits
        circuit.append(QFT(n_precision).inverse(), qr_precision)
        
        # Measure precision qubits
        circuit.measure(qr_precision, cr)
        
        return circuit
