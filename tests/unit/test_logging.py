"""
Unit tests for ALCIS logging system
"""
import pytest
import logging
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the modules we want to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.logging import ALCISLogger, SecurityAuditLogger, get_logger, get_structured_logger


class TestALCISLogger:
    """Test ALCIS logging functionality"""
    
    def test_alcis_logger_initialization(self):
        """Test that ALCISLogger initializes correctly"""
        logger = ALCISLogger()
        assert logger is not None
        assert hasattr(logger, '_loggers')
        assert isinstance(logger._loggers, dict)
    
    def test_get_logger_creates_logger(self):
        """Test that get_logger creates a logger"""
        logger_instance = ALCISLogger()
        test_logger = logger_instance.get_logger("test.logger")
        
        assert test_logger is not None
        assert isinstance(test_logger, logging.Logger)
        assert test_logger.name == "test.logger"
    
    def test_get_logger_caches_loggers(self):
        """Test that loggers are cached"""
        logger_instance = ALCISLogger()
        logger1 = logger_instance.get_logger("test.cache")
        logger2 = logger_instance.get_logger("test.cache")
        
        assert logger1 is logger2  # Should be the same instance
    
    def test_get_structured_logger(self):
        """Test structured logger creation"""
        logger_instance = ALCISLogger()
        struct_logger = logger_instance.get_structured_logger("test.struct")
        
        assert struct_logger is not None
        # Should have structured logging methods
        assert hasattr(struct_logger, 'info')
        assert hasattr(struct_logger, 'error')
        assert hasattr(struct_logger, 'warning')


class TestSecurityAuditLogger:
    """Test security audit logging"""
    
    def test_security_audit_logger_initialization(self):
        """Test SecurityAuditLogger initializes correctly"""
        audit_logger = SecurityAuditLogger()
        assert audit_logger is not None
        assert hasattr(audit_logger, 'logger')
        assert hasattr(audit_logger, 'struct_logger')
    
    def test_log_authentication_attempt(self):
        """Test logging authentication attempts"""
        audit_logger = SecurityAuditLogger()
        
        # Should not raise an exception
        try:
            audit_logger.log_authentication_attempt(
                platform="test_platform",
                username="test_user",
                success=True,
                ip_address="127.0.0.1"
            )
            assert True
        except Exception as e:
            pytest.fail(f"Authentication logging failed: {e}")
    
    def test_log_policy_decision(self):
        """Test logging policy decisions"""
        audit_logger = SecurityAuditLogger()
        
        try:
            audit_logger.log_policy_decision(
                action="test_action",
                decision="allow",
                confidence=0.95,
                reasoning={"rule": "test_rule", "result": "pass"}
            )
            assert True
        except Exception as e:
            pytest.fail(f"Policy decision logging failed: {e}")
    
    def test_log_security_event(self):
        """Test logging security events"""
        audit_logger = SecurityAuditLogger()
        
        try:
            audit_logger.log_security_event(
                event_type="test_event",
                severity="info",
                description="Test security event"
            )
            assert True
        except Exception as e:
            pytest.fail(f"Security event logging failed: {e}")
    
    def test_log_data_access(self):
        """Test logging data access events"""
        audit_logger = SecurityAuditLogger()
        
        try:
            audit_logger.log_data_access(
                resource="test_resource",
                action="read",
                user="test_user",
                success=True
            )
            assert True
        except Exception as e:
            pytest.fail(f"Data access logging failed: {e}")


class TestGlobalLoggerFunctions:
    """Test global logger convenience functions"""
    
    def test_get_logger_function(self):
        """Test global get_logger function"""
        logger = get_logger("test.global")
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_get_structured_logger_function(self):
        """Test global get_structured_logger function"""
        struct_logger = get_structured_logger("test.global.struct")
        assert struct_logger is not None
        assert hasattr(struct_logger, 'info')


class TestLoggingIntegration:
    """Test logging system integration"""
    
    def test_logger_hierarchy(self):
        """Test that logger hierarchy works correctly"""
        parent_logger = get_logger("parent")
        child_logger = get_logger("parent.child")
        
        assert parent_logger is not None
        assert child_logger is not None
        assert child_logger.name.startswith(parent_logger.name)
    
    def test_multiple_loggers_different_names(self):
        """Test creating multiple loggers with different names"""
        logger1 = get_logger("test.one")
        logger2 = get_logger("test.two")
        
        assert logger1 is not logger2
        assert logger1.name != logger2.name
    
    @patch('core.logging.settings')
    def test_debug_mode_handling(self, mock_settings):
        """Test that debug mode is handled correctly"""
        mock_settings.debug = True
        mock_settings.logs_dir = Path(tempfile.gettempdir())
        
        # Should not raise an exception
        try:
            logger_instance = ALCISLogger()
            test_logger = logger_instance.get_logger("test.debug")
            assert test_logger is not None
        except Exception as e:
            pytest.fail(f"Debug mode handling failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])