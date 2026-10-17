# tests/conftest.py
# Pytest configuration and shared fixtures

import sys
import os

# Add src to Python path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
