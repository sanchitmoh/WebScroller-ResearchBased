#!/usr/bin/env python3
"""
ALCIS Test Runner Script
"""
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🧪 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def main():
    """Run all tests"""
    print("🚀 ALCIS Test Suite Runner")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    print(f"Project root: {project_root}")
    
    # Test commands
    tests = [
        ("python -m pytest tests/unit/ -v", "Unit Tests"),
        ("python -m pytest tests/integration/ -v", "Integration Tests"),
        ('python -c "import src.main; print(\\"Main module imports successfully\\")"', "Main Module Import Test"),
        ('python -c "from src.core.config import ConfigManager; print(\\"Config module works\\")"', "Configuration Test"),
        ('python -c "from src.core.logging import get_logger; print(\\"Logging module works\\")"', "Logging Test"),
    ]
    
    # Run tests
    passed = 0
    total = len(tests)
    
    for command, description in tests:
        if run_command(command, description):
            passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())