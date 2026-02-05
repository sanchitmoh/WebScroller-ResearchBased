"""
Pytest configuration and fixtures for ALCIS tests
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from unittest.mock import Mock, AsyncMock

# Import settings with fallback
try:
    from config.settings import ALCISSettings
except ImportError:
    # Create a mock settings class for testing
    class ALCISSettings:
        def __init__(self, **kwargs):
            self.environment = kwargs.get('environment', 'test')
            self.debug = kwargs.get('debug', True)
            
            # Create mock nested objects
            class MockDB:
                url = kwargs.get('database__url', 'sqlite:///test.db')
            
            class MockRedis:
                url = kwargs.get('redis__url', 'redis://localhost:6379/1')
            
            class MockSecurity:
                secret_key = kwargs.get('security__secret_key', 'test-secret')
                encryption_key = kwargs.get('security__encryption_key', 'test-key')
            
            self.database = MockDB()
            self.redis = MockRedis()
            self.security = MockSecurity()


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings() -> ALCISSettings:
    """Test configuration settings"""
    return ALCISSettings(
        environment="test",
        debug=True,
        database__url="sqlite:///test.db",
        redis__url="redis://localhost:6379/1",
        security__secret_key="test-secret-key",
        security__encryption_key="test-encryption-key"
    )


@pytest.fixture
def mock_browser():
    """Mock browser instance for testing"""
    browser = AsyncMock()
    browser.new_context = AsyncMock()
    browser.close = AsyncMock()
    return browser


@pytest.fixture
def mock_page():
    """Mock page instance for testing"""
    page = AsyncMock()
    page.goto = AsyncMock()
    page.wait_for_selector = AsyncMock()
    page.locator = AsyncMock()
    page.evaluate = AsyncMock()
    return page


@pytest.fixture
async def mock_database():
    """Mock database session for testing"""
    db = AsyncMock()
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    db.close = AsyncMock()
    return db


@pytest.fixture
def mock_redis():
    """Mock Redis client for testing"""
    redis = AsyncMock()
    redis.get = AsyncMock()
    redis.set = AsyncMock()
    redis.delete = AsyncMock()
    redis.exists = AsyncMock()
    return redis