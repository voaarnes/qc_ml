"""Unit tests for backend management"""
import pytest
from src.backends import BackendManager


def test_backend_manager_initialization():
    """Test backend manager initialization"""
    manager = BackendManager()
    
    assert len(manager.backends) > 0
    assert "aer_simulator" in manager.backends


def test_list_backends():
    """Test listing available backends"""
    manager = BackendManager()
    backends = manager.list_backends()
    
    assert isinstance(backends, list)
    assert len(backends) > 0
    assert "aer_simulator" in backends


def test_get_backend():
    """Test getting a specific backend"""
    manager = BackendManager()
    backend = manager.get_backend("aer_simulator")
    
    assert backend is not None


def test_get_invalid_backend():
    """Test getting an invalid backend"""
    manager = BackendManager()
    
    with pytest.raises(ValueError):
        manager.get_backend("invalid_backend")


def test_backend_info():
    """Test getting backend information"""
    manager = BackendManager()
    info = manager.get_backend_info("aer_simulator")
    
    assert isinstance(info, dict)
    assert "name" in info
    assert "is_simulator" in info
    assert info["is_simulator"] is True
