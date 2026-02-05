"""
Unit tests for ALCIS core configuration
"""
import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the modules we want to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.config import ConfigManager
from core.exceptions import ALCISException, ConfigurationError


class TestConfigManager:
    """Test configuration manager functionality"""
    
    def test_config_manager_initialization(self):
        """Test that ConfigManager initializes correctly"""
        config_manager = ConfigManager()
        assert config_manager is not None
        assert hasattr(config_manager, 'settings')
        assert hasattr(config_manager, '_platform_configs')
        assert hasattr(config_manager, '_policy_configs')
    
    def test_get_platform_config_empty(self):
        """Test getting platform config when none exist"""
        config_manager = ConfigManager()
        result = config_manager.get_platform_config('nonexistent')
        assert result is None
    
    def test_get_policy_config_empty(self):
        """Test getting policy config when none exist"""
        config_manager = ConfigManager()
        result = config_manager.get_policy_config('nonexistent')
        assert result is None
    
    def test_get_all_platforms_empty(self):
        """Test getting all platforms when none exist"""
        config_manager = ConfigManager()
        result = config_manager.get_all_platforms()
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_get_all_policies_empty(self):
        """Test getting all policies when none exist"""
        config_manager = ConfigManager()
        result = config_manager.get_all_policies()
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_reload_configs(self):
        """Test config reloading"""
        config_manager = ConfigManager()
        # Should not raise an exception
        config_manager.reload_configs()
        assert True  # If we get here, reload worked


class TestExceptions:
    """Test custom exception classes"""
    
    def test_alcis_exception_basic(self):
        """Test basic ALCIS exception"""
        message = "Test error"
        exc = ALCISException(message)
        assert str(exc) == message
        assert exc.message == message
        assert exc.error_code is None
        assert exc.details == {}
    
    def test_alcis_exception_with_details(self):
        """Test ALCIS exception with error code and details"""
        message = "Test error"
        error_code = "TEST_ERROR"
        details = {"key": "value"}
        
        exc = ALCISException(message, error_code, details)
        assert exc.message == message
        assert exc.error_code == error_code
        assert exc.details == details
    
    def test_configuration_error_inheritance(self):
        """Test that ConfigurationError inherits from ALCISException"""
        exc = ConfigurationError("Config error")
        assert isinstance(exc, ALCISException)
        assert exc.message == "Config error"


class TestBasicFunctionality:
    """Test basic system functionality"""
    
    def test_imports_work(self):
        """Test that all core imports work"""
        try:
            from core.config import ConfigManager
            from core.exceptions import ALCISException
            from core.logging import get_logger
            assert True
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
    
    def test_logger_creation(self):
        """Test that logger can be created"""
        from core.logging import get_logger
        logger = get_logger("test")
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')
    
    def test_project_structure(self):
        """Test that project structure exists"""
        project_root = Path(__file__).parent.parent.parent
        
        # Check main directories exist
        assert (project_root / "src").exists()
        assert (project_root / "config").exists()
        assert (project_root / "tests").exists()
        
        # Check core modules exist
        assert (project_root / "src" / "core").exists()
        assert (project_root / "src" / "auth").exists()
        assert (project_root / "src" / "crawler").exists()
        assert (project_root / "src" / "ai").exists()
        assert (project_root / "src" / "security").exists()


if __name__ == "__main__":
    pytest.main([__file__])