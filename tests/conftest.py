# tests/conftest.py
import pytest
import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load test environment variables
load_dotenv()

# Override database name for testing
os.environ["DATABASE_NAME"] = "test_tree_db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()