"""Locate the user's backend without changing application code."""
import sys
from pathlib import Path
import pytest

for candidate in (Path.cwd(), Path.cwd() / 'backend', Path(__file__).resolve().parents[2] / 'backend'):
    if (candidate / 'app' / 'main.py').exists():
        sys.path.insert(0, str(candidate))
        break
else:
    raise RuntimeError('Run pytest from the project root or backend directory.')

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app, raise_server_exceptions=False) as connection:
        yield connection
