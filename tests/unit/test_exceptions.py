"""
Unit tests for ALCIS exception handling
"""
import pytest
from unittest.mock import MagicMock

# Import the modules we want to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.exceptions import (
    ALCISException,
    AuthenticationError,
    CredentialNotFoundError,
    CredentialExpiredError,
    UnauthorizedAccessError,
    TokenExpiredError,
    ConsentDeniedError,
    MFAError,
    SMSTimeoutError,
    EmailTimeoutError,
    TOTPSecretNotFoundError,
    InvalidMFACodeError,
    CrawlerError,
    BrowserLaunchError,
    PageLoadError,
    ElementNotFoundError,
    LoginFailedError,
    DetectionError,
    PolicyError,
    PolicyViolationError,
    PolicyNotFoundError,
    ActionNotAllowedError,
    AIError,
    ModelLoadError,
    InferenceError,
    ConfidenceThresholdError,
    ReasoningError,
    SecurityError,
    EncryptionError,
    IntegrityError,
    ThreatDetectedError,
    ConfigurationError,
    InvalidConfigurationError,
    MissingConfigurationError,
    DatabaseError,
    ConnectionError,
    QueryError,
    handle_exception
)


class TestALCISException:
    """Test base ALCIS exception"""
    
    def test_basic_exception(self):
        """Test basic exception creation"""
        message = "Test error message"
        exc = ALCISException(message)
        
        assert str(exc) == message
        assert exc.message == message
        assert exc.error_code is None
        assert exc.details == {}
    
    def test_exception_with_error_code(self):
        """Test exception with error code"""
        message = "Test error"
        error_code = "TEST_001"
        
        exc = ALCISException(message, error_code)
        assert exc.message == message
        assert exc.error_code == error_code
        assert exc.details == {}
    
    def test_exception_with_details(self):
        """Test exception with details"""
        message = "Test error"
        error_code = "TEST_001"
        details = {"key": "value", "number": 42}
        
        exc = ALCISException(message, error_code, details)
        assert exc.message == message
        assert exc.error_code == error_code
        assert exc.details == details


class TestAuthenticationExceptions:
    """Test authentication-related exceptions"""
    
    def test_authentication_error_inheritance(self):
        """Test AuthenticationError inherits from ALCISException"""
        exc = AuthenticationError("Auth failed")
        assert isinstance(exc, ALCISException)
        assert exc.message == "Auth failed"
    
    def test_credential_not_found_error(self):
        """Test CredentialNotFoundError"""
        exc = CredentialNotFoundError("Credential not found")
        assert isinstance(exc, AuthenticationError)
        assert isinstance(exc, ALCISException)
    
    def test_credential_expired_error(self):
        """Test CredentialExpiredError"""
        exc = CredentialExpiredError("Credential expired")
        assert isinstance(exc, AuthenticationError)
    
    def test_unauthorized_access_error(self):
        """Test UnauthorizedAccessError"""
        exc = UnauthorizedAccessError("Access denied")
        assert isinstance(exc, AuthenticationError)
    
    def test_token_expired_error(self):
        """Test TokenExpiredError"""
        exc = TokenExpiredError("Token expired")
        assert isinstance(exc, AuthenticationError)
    
    def test_consent_denied_error(self):
        """Test ConsentDeniedError"""
        exc = ConsentDeniedError("Consent denied")
        assert isinstance(exc, AuthenticationError)


class TestMFAExceptions:
    """Test MFA-related exceptions"""
    
    def test_mfa_error_inheritance(self):
        """Test MFAError inherits from AuthenticationError"""
        exc = MFAError("MFA failed")
        assert isinstance(exc, AuthenticationError)
        assert isinstance(exc, ALCISException)
    
    def test_sms_timeout_error(self):
        """Test SMSTimeoutError"""
        exc = SMSTimeoutError("SMS timeout")
        assert isinstance(exc, MFAError)
    
    def test_email_timeout_error(self):
        """Test EmailTimeoutError"""
        exc = EmailTimeoutError("Email timeout")
        assert isinstance(exc, MFAError)
    
    def test_totp_secret_not_found_error(self):
        """Test TOTPSecretNotFoundError"""
        exc = TOTPSecretNotFoundError("TOTP secret not found")
        assert isinstance(exc, MFAError)
    
    def test_invalid_mfa_code_error(self):
        """Test InvalidMFACodeError"""
        exc = InvalidMFACodeError("Invalid MFA code")
        assert isinstance(exc, MFAError)


class TestCrawlerExceptions:
    """Test crawler-related exceptions"""
    
    def test_crawler_error_inheritance(self):
        """Test CrawlerError inherits from ALCISException"""
        exc = CrawlerError("Crawler failed")
        assert isinstance(exc, ALCISException)
    
    def test_browser_launch_error(self):
        """Test BrowserLaunchError"""
        exc = BrowserLaunchError("Browser launch failed")
        assert isinstance(exc, CrawlerError)
    
    def test_page_load_error(self):
        """Test PageLoadError"""
        exc = PageLoadError("Page load failed")
        assert isinstance(exc, CrawlerError)
    
    def test_element_not_found_error(self):
        """Test ElementNotFoundError"""
        exc = ElementNotFoundError("Element not found")
        assert isinstance(exc, CrawlerError)
    
    def test_login_failed_error(self):
        """Test LoginFailedError"""
        exc = LoginFailedError("Login failed")
        assert isinstance(exc, CrawlerError)
    
    def test_detection_error(self):
        """Test DetectionError"""
        exc = DetectionError("Bot detected")
        assert isinstance(exc, CrawlerError)


class TestPolicyExceptions:
    """Test policy-related exceptions"""
    
    def test_policy_error_inheritance(self):
        """Test PolicyError inherits from ALCISException"""
        exc = PolicyError("Policy error")
        assert isinstance(exc, ALCISException)
    
    def test_policy_violation_error(self):
        """Test PolicyViolationError"""
        exc = PolicyViolationError("Policy violation")
        assert isinstance(exc, PolicyError)
    
    def test_policy_not_found_error(self):
        """Test PolicyNotFoundError"""
        exc = PolicyNotFoundError("Policy not found")
        assert isinstance(exc, PolicyError)
    
    def test_action_not_allowed_error(self):
        """Test ActionNotAllowedError"""
        exc = ActionNotAllowedError("Action not allowed")
        assert isinstance(exc, PolicyError)


class TestAIExceptions:
    """Test AI-related exceptions"""
    
    def test_ai_error_inheritance(self):
        """Test AIError inherits from ALCISException"""
        exc = AIError("AI error")
        assert isinstance(exc, ALCISException)
    
    def test_model_load_error(self):
        """Test ModelLoadError"""
        exc = ModelLoadError("Model load failed")
        assert isinstance(exc, AIError)
    
    def test_inference_error(self):
        """Test InferenceError"""
        exc = InferenceError("Inference failed")
        assert isinstance(exc, AIError)
    
    def test_confidence_threshold_error(self):
        """Test ConfidenceThresholdError"""
        exc = ConfidenceThresholdError("Confidence too low")
        assert isinstance(exc, AIError)
    
    def test_reasoning_error(self):
        """Test ReasoningError"""
        exc = ReasoningError("Reasoning failed")
        assert isinstance(exc, AIError)


class TestSecurityExceptions:
    """Test security-related exceptions"""
    
    def test_security_error_inheritance(self):
        """Test SecurityError inherits from ALCISException"""
        exc = SecurityError("Security error")
        assert isinstance(exc, ALCISException)
    
    def test_encryption_error(self):
        """Test EncryptionError"""
        exc = EncryptionError("Encryption failed")
        assert isinstance(exc, SecurityError)
    
    def test_integrity_error(self):
        """Test IntegrityError"""
        exc = IntegrityError("Integrity check failed")
        assert isinstance(exc, SecurityError)
    
    def test_threat_detected_error(self):
        """Test ThreatDetectedError"""
        exc = ThreatDetectedError("Threat detected")
        assert isinstance(exc, SecurityError)


class TestConfigurationExceptions:
    """Test configuration-related exceptions"""
    
    def test_configuration_error_inheritance(self):
        """Test ConfigurationError inherits from ALCISException"""
        exc = ConfigurationError("Config error")
        assert isinstance(exc, ALCISException)
    
    def test_invalid_configuration_error(self):
        """Test InvalidConfigurationError"""
        exc = InvalidConfigurationError("Invalid config")
        assert isinstance(exc, ConfigurationError)
    
    def test_missing_configuration_error(self):
        """Test MissingConfigurationError"""
        exc = MissingConfigurationError("Missing config")
        assert isinstance(exc, ConfigurationError)


class TestDatabaseExceptions:
    """Test database-related exceptions"""
    
    def test_database_error_inheritance(self):
        """Test DatabaseError inherits from ALCISException"""
        exc = DatabaseError("Database error")
        assert isinstance(exc, ALCISException)
    
    def test_connection_error(self):
        """Test ConnectionError"""
        exc = ConnectionError("Connection failed")
        assert isinstance(exc, DatabaseError)
    
    def test_query_error(self):
        """Test QueryError"""
        exc = QueryError("Query failed")
        assert isinstance(exc, DatabaseError)


class TestExceptionHandler:
    """Test exception handling utility"""
    
    def test_handle_alcis_exception(self):
        """Test handling ALCIS exceptions"""
        mock_logger = MagicMock()
        original_exc = ALCISException("Test error", "TEST_001", {"key": "value"})
        
        result = handle_exception(original_exc, mock_logger)
        
        assert result is original_exc
        mock_logger.error.assert_called_once()
    
    def test_handle_connection_refused_error(self):
        """Test handling ConnectionRefusedError"""
        mock_logger = MagicMock()
        original_exc = ConnectionRefusedError("Connection refused")
        
        result = handle_exception(original_exc, mock_logger)
        
        assert isinstance(result, ConnectionError)
        assert "Connection failed" in result.message
        assert result.error_code == "CONNECTION_FAILED"
        mock_logger.error.assert_called_once()
    
    def test_handle_permission_error(self):
        """Test handling PermissionError"""
        mock_logger = MagicMock()
        original_exc = PermissionError("Permission denied")
        
        result = handle_exception(original_exc, mock_logger)
        
        assert isinstance(result, UnauthorizedAccessError)
        assert "Permission denied" in result.message
        assert result.error_code == "PERMISSION_DENIED"
        mock_logger.error.assert_called_once()
    
    def test_handle_timeout_error(self):
        """Test handling TimeoutError"""
        mock_logger = MagicMock()
        original_exc = TimeoutError("Operation timed out")
        
        result = handle_exception(original_exc, mock_logger)
        
        assert isinstance(result, ALCISException)
        assert "Operation timed out" in result.message
        assert result.error_code == "TIMEOUT"
        mock_logger.error.assert_called_once()
    
    def test_handle_generic_exception(self):
        """Test handling generic exceptions"""
        mock_logger = MagicMock()
        original_exc = ValueError("Invalid value")
        
        result = handle_exception(original_exc, mock_logger)
        
        assert isinstance(result, ALCISException)
        assert "Unexpected error" in result.message
        assert result.error_code == "UNEXPECTED_ERROR"
        mock_logger.error.assert_called_once()
    
    def test_handle_exception_with_context(self):
        """Test handling exceptions with context"""
        mock_logger = MagicMock()
        original_exc = ValueError("Test error")
        context = {"user": "test_user", "action": "test_action"}
        
        result = handle_exception(original_exc, mock_logger, context)
        
        assert isinstance(result, ALCISException)
        assert context.items() <= result.details.items()  # Context should be in details


if __name__ == "__main__":
    pytest.main([__file__])