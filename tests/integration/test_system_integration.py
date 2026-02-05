"""
Integration tests for ALCIS system components
"""
import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the modules we want to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestSystemIntegration:
    """Test integration between system components"""
    
    def test_core_modules_import_successfully(self):
        """Test that all core modules can be imported together"""
        try:
            from core.config import ConfigManager
            from core.logging import ALCISLogger, SecurityAuditLogger
            from core.exceptions import ALCISException
            
            # Test that they can be instantiated
            config_manager = ConfigManager()
            logger = ALCISLogger()
            audit_logger = SecurityAuditLogger()
            
            assert config_manager is not None
            assert logger is not None
            assert audit_logger is not None
            
        except ImportError as e:
            pytest.fail(f"Core module import failed: {e}")
        except Exception as e:
            pytest.fail(f"Core module instantiation failed: {e}")
    
    def test_configuration_and_logging_integration(self):
        """Test that configuration and logging work together"""
        try:
            from core.config import ConfigManager
            from core.logging import get_logger
            
            config_manager = ConfigManager()
            logger = get_logger("integration.test")
            
            # Test logging with configuration
            logger.info("Integration test message")
            
            # Should not raise an exception
            assert True
            
        except Exception as e:
            pytest.fail(f"Configuration and logging integration failed: {e}")
    
    def test_exception_handling_with_logging(self):
        """Test that exception handling works with logging"""
        try:
            from core.exceptions import ALCISException, handle_exception
            from core.logging import get_logger
            
            logger = get_logger("integration.exception.test")
            
            # Create and handle an exception
            original_exc = ValueError("Test integration error")
            handled_exc = handle_exception(original_exc, logger)
            
            assert isinstance(handled_exc, ALCISException)
            assert "Test integration error" in handled_exc.message
            
        except Exception as e:
            pytest.fail(f"Exception handling integration failed: {e}")
    
    @patch.dict(os.environ, {
        'SECRET_KEY': 'test-secret-key',
        'ENCRYPTION_KEY': 'test-encryption-key',
        'DATABASE_URL': 'sqlite:///test.db',
        'REDIS_URL': 'redis://localhost:6379/1'
    })
    def test_environment_configuration_loading(self):
        """Test that environment variables are loaded correctly"""
        try:
            from config.settings import ALCISSettings
            
            settings = ALCISSettings()
            
            # Check that environment variables are loaded
            assert settings.security.secret_key == 'test-secret-key'
            assert settings.security.encryption_key == 'test-encryption-key'
            assert settings.database.url == 'sqlite:///test.db'
            assert settings.redis.url == 'redis://localhost:6379/1'
            
        except Exception as e:
            pytest.fail(f"Environment configuration loading failed: {e}")
    
    def test_project_structure_integrity(self):
        """Test that the project structure is intact"""
        project_root = Path(__file__).parent.parent.parent
        
        # Test main directories
        required_dirs = [
            "src",
            "src/core",
            "src/auth",
            "src/crawler", 
            "src/ai",
            "src/security",
            "src/utils",
            "config",
            "tests",
            "tests/unit",
            "tests/integration"
        ]
        
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            assert full_path.exists(), f"Required directory missing: {dir_path}"
            assert full_path.is_dir(), f"Path is not a directory: {dir_path}"
        
        # Test main files
        required_files = [
            "src/core/__init__.py",
            "src/core/config.py",
            "src/core/logging.py",
            "src/core/exceptions.py",
            "config/settings.py",
            "requirements.txt",
            "pyproject.toml",
            "README.md"
        ]
        
        for file_path in required_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Required file missing: {file_path}"
            assert full_path.is_file(), f"Path is not a file: {file_path}"
    
    def test_docker_configuration_exists(self):
        """Test that Docker configuration files exist"""
        project_root = Path(__file__).parent.parent.parent
        
        docker_files = [
            "Dockerfile",
            "docker-compose.yml",
            ".dockerignore"
        ]
        
        for file_path in docker_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Docker file missing: {file_path}"
    
    def test_ci_cd_configuration_exists(self):
        """Test that CI/CD configuration files exist"""
        project_root = Path(__file__).parent.parent.parent
        
        cicd_files = [
            ".github/workflows/ci.yml",
            ".gitlab-ci.yml",
            "azure-pipelines.yml"
        ]
        
        for file_path in cicd_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"CI/CD file missing: {file_path}"


class TestModuleStructure:
    """Test module structure and organization"""
    
    def test_all_modules_have_init_files(self):
        """Test that all Python modules have __init__.py files"""
        project_root = Path(__file__).parent.parent.parent
        src_dir = project_root / "src"
        
        # Find all directories in src
        for item in src_dir.rglob("*"):
            if item.is_dir() and not item.name.startswith('.'):
                init_file = item / "__init__.py"
                assert init_file.exists(), f"Missing __init__.py in {item.relative_to(project_root)}"
    
    def test_test_modules_structure(self):
        """Test that test modules are properly structured"""
        project_root = Path(__file__).parent.parent.parent
        tests_dir = project_root / "tests"
        
        # Check test directories exist
        assert (tests_dir / "unit").exists()
        assert (tests_dir / "integration").exists()
        
        # Check conftest.py exists
        assert (tests_dir / "conftest.py").exists()
        
        # Check that test files follow naming convention
        for test_file in tests_dir.rglob("test_*.py"):
            assert test_file.name.startswith("test_"), f"Test file doesn't follow naming convention: {test_file.name}"


if __name__ == "__main__":
    pytest.main([__file__])