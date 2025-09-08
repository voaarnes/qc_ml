"""Abstract interface for quantum backends"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from qiskit import QuantumCircuit
from qiskit.result import Result


class QuantumBackend(ABC):
    """Abstract base class for quantum backends"""
    
    @abstractmethod
    def run(self, circuit: QuantumCircuit, shots: int = 1024, **kwargs) -> Result:
        """Execute a quantum circuit"""
        pass
    
    @abstractmethod
    def get_backend_info(self) -> Dict[str, Any]:
        """Get backend information and capabilities"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if backend is available"""
        pass
