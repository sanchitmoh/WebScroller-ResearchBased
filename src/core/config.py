"""
ALCIS Core Configuration Manager
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

# Import settings directly to avoid circular imports
try:
    from config.settings import ALCISSettings
    settings = ALCISSettings()
except ImportError:
    # Fallback for testing
    from dataclasses import dataclass
    
    @dataclass
    class MockSettings:
        project_root: Path = Path(__file__).parent.parent.parent
        data_dir: Path = Path(__file__).parent.parent.parent / "data"
        logs_dir: Path = Path(__file__).parent.parent.parent / "logs"
        debug: bool = True
    
    settings = MockSettings()


@dataclass
class ConfigManager:
    """
    Central configuration management for ALCIS system
    """
    settings: Any = field(default_factory=lambda: settings)
    _platform_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    _policy_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize configuration manager"""
        self._ensure_directories()
        self._load_platform_configs()
        self._load_policy_configs()
    
    def _ensure_directories(self) -> None:
        """Ensure required directories exist"""
        directories = [
            self.settings.data_dir,
            self.settings.logs_dir,
            self.settings.project_root / "sessions",
            self.settings.project_root / "cache",
            self.settings.project_root / "temp"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_platform_configs(self) -> None:
        """Load platform-specific configurations"""
        platform_dir = self.settings.project_root / "config" / "platforms"
        
        if not platform_dir.exists():
            return
        
        for config_file in platform_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    platform_name = config_file.stem
                    self._platform_configs[platform_name] = config
            except Exception as e:
                print(f"Warning: Failed to load platform config {config_file}: {e}")
    
    def _load_policy_configs(self) -> None:
        """Load policy configurations"""
        policy_dir = self.settings.project_root / "config" / "policies"
        
        if not policy_dir.exists():
            return
        
        for config_file in policy_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    policy_name = config_file.stem
                    self._policy_configs[policy_name] = config
            except Exception as e:
                print(f"Warning: Failed to load policy config {config_file}: {e}")
    
    def get_platform_config(self, platform_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific platform"""
        return self._platform_configs.get(platform_name)
    
    def get_policy_config(self, policy_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific policy"""
        return self._policy_configs.get(policy_name)
    
    def get_all_platforms(self) -> Dict[str, Dict[str, Any]]:
        """Get all platform configurations"""
        return self._platform_configs.copy()
    
    def get_all_policies(self) -> Dict[str, Dict[str, Any]]:
        """Get all policy configurations"""
        return self._policy_configs.copy()
    
    def reload_configs(self) -> None:
        """Reload all configurations"""
        self._platform_configs.clear()
        self._policy_configs.clear()
        self._load_platform_configs()
        self._load_policy_configs()
    
    def validate_config(self) -> bool:
        """Validate current configuration"""
        try:
            # Check required settings
            required_settings = [
                self.settings.security.secret_key,
                self.settings.security.encryption_key
            ]
            
            if not all(required_settings):
                return False
            
            # Check directory permissions
            test_dirs = [
                self.settings.data_dir,
                self.settings.logs_dir
            ]
            
            for directory in test_dirs:
                if not directory.exists() or not os.access(directory, os.W_OK):
                    return False
            
            return True
            
        except Exception:
            return False


# Global configuration manager instance
config_manager = ConfigManager()