"""Backend management for quantum computing"""
import os
from typing import Optional, Dict, Any, List
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class BackendManager:
    """Manages quantum computing backends"""
    
    def __init__(self):
        self.backends = {}
        self._initialize_backends()
    
    def _initialize_backends(self):
        """Initialize available backends"""
        # Always available simulators
        self.backends["aer_simulator"] = AerSimulator()
        self.backends["statevector_simulator"] = AerSimulator(method="statevector")
        self.backends["qasm_simulator"] = AerSimulator(method="automatic")
        
        # Fake backends for testing
        self.backends["fake_backend"] = GenericBackendV2(num_qubits=27)
        
        # IBM Quantum backends (if token available)
        if os.getenv("IBM_QUANTUM_TOKEN"):
            try:
                self._initialize_ibm_backends()
            except Exception as e:
                logger.warning(f"Could not initialize IBM backends: {e}")
    
    def _initialize_ibm_backends(self):
        """Initialize IBM Quantum backends"""
        service = QiskitRuntimeService(
            channel="ibm_quantum",
            token=os.getenv("IBM_QUANTUM_TOKEN")
        )
        
        # Get available backends
        backends = service.backends()
        for backend in backends:
            self.backends[f"ibm_{backend.name}"] = backend
            logger.info(f"Added IBM backend: {backend.name}")
    
    def get_backend(self, name: str = "aer_simulator"):
        """Get a specific backend"""
        if name not in self.backends:
            raise ValueError(f"Backend {name} not available. Available: {list(self.backends.keys())}")
        return self.backends[name]
    
    def list_backends(self) -> List[str]:
        """List all available backends"""
        return list(self.backends.keys())
    
    def get_backend_info(self, name: str) -> Dict[str, Any]:
        """Get information about a specific backend"""
        backend = self.get_backend(name)
        
        info = {
            "name": name,
            "is_simulator": "sim" in name.lower() or "fake" in name.lower(),
        }
        
        if hasattr(backend, "configuration"):
            config = backend.configuration()
            info.update({
                "n_qubits": config.n_qubits,
                "basis_gates": config.basis_gates,
                "coupling_map": config.coupling_map,
            })
        
        return info
    
    def run_circuit(
        self,
        circuit: QuantumCircuit,
        backend_name: str = "aer_simulator",
        shots: int = 1024,
        optimization_level: int = 3,
        **kwargs
    ):
        """Run a circuit on a specified backend"""
        backend = self.get_backend(backend_name)
        
        logger.info(f"Running circuit on {backend_name} with {shots} shots")
        
        # For IBM Runtime backends
        if backend_name.startswith("ibm_"):
            with Session(service=self.service, backend=backend) as session:
                sampler = Sampler(session=session, options={"shots": shots})
                job = sampler.run(circuit)
                result = job.result()
        else:
            # For local simulators
            from qiskit import transpile
            transpiled = transpile(
                circuit,
                backend,
                optimization_level=optimization_level
            )
            job = backend.run(transpiled, shots=shots, **kwargs)
            result = job.result()
        
        return result
