"""
ALCIS Logging Framework
"""
import logging
import logging.handlers
import structlog
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Import settings with fallback for testing
try:
    from config.settings import settings
except ImportError:
    # Fallback for testing
    from dataclasses import dataclass
    
    @dataclass
    class MockSettings:
        logs_dir: Path = Path(__file__).parent.parent.parent / "logs"
        debug: bool = True
    
    settings = MockSettings()


class ALCISLogger:
    """
    Advanced logging system for ALCIS with structured logging support
    """
    
    def __init__(self):
        self._loggers: Dict[str, logging.Logger] = {}
        self._setup_structlog()
        self._setup_file_handlers()
    
    def _setup_structlog(self) -> None:
        """Configure structured logging"""
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    
    def _setup_file_handlers(self) -> None:
        """Setup file handlers for different log types"""
        log_dir = settings.logs_dir
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Main application log
        self._setup_file_handler(
            "alcis.main",
            log_dir / "alcis.log",
            level=logging.INFO
        )
        
        # Security audit log
        self._setup_file_handler(
            "alcis.security",
            log_dir / "security.log",
            level=logging.WARNING
        )
        
        # Authentication log
        self._setup_file_handler(
            "alcis.auth",
            log_dir / "auth.log",
            level=logging.INFO
        )
        
        # AI decision log
        self._setup_file_handler(
            "alcis.ai",
            log_dir / "ai_decisions.log",
            level=logging.INFO
        )
        
        # Error log
        self._setup_file_handler(
            "alcis.error",
            log_dir / "errors.log",
            level=logging.ERROR
        )
    
    def _setup_file_handler(
        self, 
        logger_name: str, 
        file_path: Path, 
        level: int = logging.INFO,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ) -> None:
        """Setup rotating file handler for a specific logger"""
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
        # Add console handler for development
        if settings.debug:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        self._loggers[logger_name] = logger
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get logger by name"""
        if name not in self._loggers:
            # Create default logger if not exists
            self._setup_file_handler(
                name,
                settings.logs_dir / f"{name.replace('.', '_')}.log"
            )
        return self._loggers[name]
    
    def get_structured_logger(self, name: str) -> structlog.BoundLogger:
        """Get structured logger by name"""
        return structlog.get_logger(name)


class SecurityAuditLogger:
    """
    Specialized logger for security events and audit trails
    """
    
    def __init__(self):
        self.logger = logging.getLogger("alcis.security")
        self.struct_logger = structlog.get_logger("alcis.security")
    
    def log_authentication_attempt(
        self,
        platform: str,
        username: str,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        **kwargs
    ) -> None:
        """Log authentication attempt"""
        self.struct_logger.info(
            "authentication_attempt",
            platform=platform,
            username=username,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs
        )
    
    def log_policy_decision(
        self,
        action: str,
        decision: str,
        confidence: float,
        reasoning: Dict[str, Any],
        **kwargs
    ) -> None:
        """Log policy decision"""
        self.struct_logger.info(
            "policy_decision",
            action=action,
            decision=decision,
            confidence=confidence,
            reasoning=reasoning,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs
        )
    
    def log_security_event(
        self,
        event_type: str,
        severity: str,
        description: str,
        **kwargs
    ) -> None:
        """Log security event"""
        log_method = getattr(self.struct_logger, severity.lower(), self.struct_logger.info)
        log_method(
            "security_event",
            event_type=event_type,
            severity=severity,
            description=description,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs
        )
    
    def log_data_access(
        self,
        resource: str,
        action: str,
        user: str,
        success: bool,
        **kwargs
    ) -> None:
        """Log data access event"""
        self.struct_logger.info(
            "data_access",
            resource=resource,
            action=action,
            user=user,
            success=success,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs
        )


# Global logger instances
alcis_logger = ALCISLogger()
security_logger = SecurityAuditLogger()

# Convenience functions
def get_logger(name: str) -> logging.Logger:
    """Get standard logger"""
    return alcis_logger.get_logger(name)

def get_structured_logger(name: str) -> structlog.BoundLogger:
    """Get structured logger"""
    return alcis_logger.get_structured_logger(name)