"""Variational Quantum Eigensolver implementation"""
import numpy as np
from typing import Optional, Callable, Dict, Any
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE as QiskitVQE
from qiskit_algorithms.optimizers import COBYLA, SPSA, L_BFGS_B
from qiskit.primitives import Estimator
from loguru import logger


class VQE:
    """Variational Quantum Eigensolver for finding ground states"""
    
    def __init__(
        self,
        hamiltonian: SparsePauliOp,
        ansatz: QuantumCircuit,
        optimizer: Optional[str] = "COBYLA",
        initial_params: Optional[np.ndarray] = None
    ):
        self.hamiltonian = hamiltonian
        self.ansatz = ansatz
        self.initial_params = initial_params
        
        # Set up optimizer
        optimizers = {
            "COBYLA": COBYLA(maxiter=500),
            "SPSA": SPSA(maxiter=100),
            "L-BFGS-B": L_BFGS_B(maxiter=500)
        }
        self.optimizer = optimizers.get(optimizer, COBYLA())
        
        # Initialize estimator
        self.estimator = Estimator()
        
        # Results storage
        self.result = None
        self.energy_history = []
    
    def run(self) -> Dict[str, Any]:
        """Run VQE algorithm"""
        logger.info("Starting VQE optimization")
        
        # Create VQE instance
        vqe = QiskitVQE(
            estimator=self.estimator,
            ansatz=self.ansatz,
            optimizer=self.optimizer,
            initial_point=self.initial_params
        )
        
        # Set callback to track progress
        vqe.callback = self._callback
        
        # Compute minimum eigenvalue
        self.result = vqe.compute_minimum_eigenvalue(self.hamiltonian)
        
        logger.info(f"VQE completed. Ground state energy: {self.result.eigenvalue}")
        
        return {
            "energy": self.result.eigenvalue,
            "optimal_params": self.result.optimal_parameters,
            "optimal_circuit": self.result.optimal_circuit,
            "optimizer_evals": self.result.optimizer_evals,
            "energy_history": self.energy_history
        }
    
    def _callback(self, eval_count, params, value, metadata):
        """Callback function to track optimization progress"""
        self.energy_history.append(value)
        if eval_count % 10 == 0:
            logger.debug(f"Iteration {eval_count}: Energy = {value}")
    
    @staticmethod
    def create_h2_hamiltonian() -> SparsePauliOp:
        """Create H2 molecule Hamiltonian"""
        # Simplified H2 Hamiltonian in minimal basis
        coeffs = [
            -1.052373245772859,
            0.39793742484318045,
            -0.39793742484318045,
            -0.01128010425623538,
            0.18093119978423156
        ]
        
        operators = [
            "II",
            "IZ",
            "ZI",
            "ZZ",
            "XX"
        ]
        
        return SparsePauliOp(operators, coeffs)
