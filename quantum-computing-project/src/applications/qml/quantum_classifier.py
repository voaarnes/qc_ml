"""Quantum Machine Learning Classifier"""
import numpy as np
from typing import Optional, Tuple
from sklearn.preprocessing import StandardScaler
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit_machine_learning.algorithms import VQC
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler


class QuantumClassifier:
    """Variational Quantum Classifier for binary classification"""
    
    def __init__(
        self,
        n_qubits: int = 4,
        feature_map_reps: int = 2,
        ansatz_reps: int = 2,
        optimizer: str = "COBYLA"
    ):
        self.n_qubits = n_qubits
        self.feature_map_reps = feature_map_reps
        self.ansatz_reps = ansatz_reps
        
        self.feature_map = self._create_feature_map()
        self.ansatz = self._create_ansatz()
        
        optimizers = {
            "COBYLA": COBYLA(maxiter=100),
            "SPSA": SPSA(maxiter=100)
        }
        self.optimizer = optimizers.get(optimizer, COBYLA())
        
        self.scaler = StandardScaler()
        self.vqc = None
    
    def _create_feature_map(self) -> QuantumCircuit:
        """Create a feature map for encoding classical data"""
        from qiskit.circuit.library import ZZFeatureMap
        
        return ZZFeatureMap(
            feature_dimension=self.n_qubits,
            reps=self.feature_map_reps,
            entanglement='linear'
        )
    
    def _create_ansatz(self) -> QuantumCircuit:
        """Create a variational ansatz"""
        from qiskit.circuit.library import RealAmplitudes
        
        return RealAmplitudes(
            num_qubits=self.n_qubits,
            reps=self.ansatz_reps,
            entanglement='full'
        )
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train the quantum classifier"""
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Ensure correct dimensions
        if X_scaled.shape[1] > self.n_qubits:
            X_scaled = X_scaled[:, :self.n_qubits]
        elif X_scaled.shape[1] < self.n_qubits:
            padding = np.zeros((X_scaled.shape[0], self.n_qubits - X_scaled.shape[1]))
            X_scaled = np.hstack([X_scaled, padding])
        
        # Create VQC
        self.vqc = VQC(
            feature_map=self.feature_map,
            ansatz=self.ansatz,
            optimizer=self.optimizer,
            sampler=Sampler()
        )
        
        # Fit the model
        self.vqc.fit(X_scaled, y)
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if self.vqc is None:
            raise ValueError("Model must be fitted before prediction")
        
        X_scaled = self.scaler.transform(X)
        
        # Ensure correct dimensions
        if X_scaled.shape[1] > self.n_qubits:
            X_scaled = X_scaled[:, :self.n_qubits]
        elif X_scaled.shape[1] < self.n_qubits:
            padding = np.zeros((X_scaled.shape[0], self.n_qubits - X_scaled.shape[1]))
            X_scaled = np.hstack([X_scaled, padding])
        
        return self.vqc.predict(X_scaled)
