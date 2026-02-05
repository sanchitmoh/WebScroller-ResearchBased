"""
ALCIS Custom Exceptions
"""
from typing import Optional, Dict, Any


class ALCISException(Exception):
    """Base exception for all ALCIS errors"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


# Authentication Exceptions
class AuthenticationError(ALCISException):
    """Base authentication error"""
    pass


class CredentialNotFoundError(AuthenticationError):
    """Credential not found in vault"""
    pass


class CredentialExpiredError(AuthenticationError):
    """Credential has expired"""
    pass


class UnauthorizedAccessError(AuthenticationError):
    """Access denied due to insufficient permissions"""
    pass


class TokenExpiredError(AuthenticationError):
    """JWT token has expired"""
    pass


class ConsentDeniedError(AuthenticationError):
    """User consent was denied"""
    pass


# MFA Exceptions
class MFAError(AuthenticationError):
    """Base MFA error"""
    pass


class SMSTimeoutError(MFAError):
    """SMS verification code timeout"""
    pass


class EmailTimeoutError(MFAError):
    """Email verification timeout"""
    pass


class TOTPSecretNotFoundError(MFAError):
    """TOTP secret not found"""
    pass


class InvalidMFACodeError(MFAError):
    """Invalid MFA code provided"""
    pass


# Crawler Exceptions
class CrawlerError(ALCISException):
    """Base crawler error"""
    pass


class BrowserLaunchError(CrawlerError):
    """Failed to launch browser"""
    pass


class PageLoadError(CrawlerError):
    """Failed to load page"""
    pass


class ElementNotFoundError(CrawlerError):
    """Required element not found on page"""
    pass


class LoginFailedError(CrawlerError):
    """Login attempt failed"""
    pass


class DetectionError(CrawlerError):
    """Bot detection triggered"""
    pass


# Policy Exceptions
class PolicyError(ALCISException):
    """Base policy error"""
    pass


class PolicyViolationError(PolicyError):
    """Action violates policy"""
    pass


class PolicyNotFoundError(PolicyError):
    """Policy configuration not found"""
    pass


class ActionNotAllowedError(PolicyError):
    """Action not allowed by current scope"""
    pass


# AI Exceptions
class AIError(ALCISException):
    """Base AI error"""
    pass


class ModelLoadError(AIError):
    """Failed to load AI model"""
    pass


class InferenceError(AIError):
    """AI inference failed"""
    pass


class ConfidenceThresholdError(AIError):
    """Confidence below threshold"""
    pass


class ReasoningError(AIError):
    """Reasoning chain generation failed"""
    pass


# Security Exceptions
class SecurityError(ALCISException):
    """Base security error"""
    pass


class EncryptionError(SecurityError):
    """Encryption/decryption failed"""
    pass


class IntegrityError(SecurityError):
    """Data integrity check failed"""
    pass


class ThreatDetectedError(SecurityError):
    """Security threat detected"""
    pass


# Configuration Exceptions
class ConfigurationError(ALCISException):
    """Configuration error"""
    pass


class InvalidConfigurationError(ConfigurationError):
    """Invalid configuration provided"""
    pass


class MissingConfigurationError(ConfigurationError):
    """Required configuration missing"""
    pass


# Database Exceptions
class DatabaseError(ALCISException):
    """Database operation error"""
    pass


class ConnectionError(DatabaseError):
    """Database connection failed"""
    pass


class QueryError(DatabaseError):
    """Database query failed"""
    pass


# Utility Functions
def handle_exception(
    exception: Exception,
    logger,
    context: Optional[Dict[str, Any]] = None
) -> ALCISException:
    """
    Convert generic exceptions to ALCIS exceptions with proper logging
    """
    context = context or {}
    
    if isinstance(exception, ALCISException):
        logger.error(
            f"ALCIS Exception: {exception.message}",
            extra={
                "error_code": exception.error_code,
                "details": exception.details,
                **context
            }
        )
        return exception
    
    # Convert common exceptions
    if isinstance(exception, PermissionError):
        alcis_exception = UnauthorizedAccessError(
            f"Permission denied: {str(exception)}",
            error_code="PERMISSION_DENIED",
            details={"original_exception": str(exception), **context}
        )
    elif isinstance(exception, TimeoutError):
        alcis_exception = ALCISException(
            f"Operation timed out: {str(exception)}",
            error_code="TIMEOUT",
            details={"original_exception": str(exception), **context}
        )
    elif isinstance(exception, (ConnectionRefusedError, OSError)):
        alcis_exception = ConnectionError(
            f"Connection failed: {str(exception)}",
            error_code="CONNECTION_FAILED",
            details={"original_exception": str(exception), **context}
        )
    else:
        alcis_exception = ALCISException(
            f"Unexpected error: {str(exception)}",
            error_code="UNEXPECTED_ERROR",
            details={"original_exception": str(exception), **context}
        )
    
    logger.error(
        f"Exception converted: {alcis_exception.message}",
        extra={
            "error_code": alcis_exception.error_code,
            "details": alcis_exception.details
        }
    )
    
    return alcis_exception