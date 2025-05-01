import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncio
import os
from app.main import app
from app.db import initialize_db, nodes_collection, counters_collection

# Get API key from environment variable
API_KEY = os.getenv("API_KEY", "default_development_api_key_change_this_in_production")

@pytest.fixture
async def setup_test_db():
    # Clear collections before each test
    await nodes_collection.delete_many({})
    await counters_collection.delete_many({})
    
    # Initialize database with fresh data
    await initialize_db()
    yield
    
    # Clean up after tests
    await nodes_collection.delete_many({})
    await counters_collection.delete_many({})

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def auth_client():
    """Get a client with API key authentication."""
    async with AsyncClient(
        app=app, 
        base_url="http://test",
        headers={"X-API-Key": API_KEY}
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_get_trees_endpoint(setup_test_db, auth_client):
    # Set up test data
    # The initialize_db function already creates a root node
    
    # Make request to get trees
    response = await auth_client.get("/api/tree")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    
    # Should be an array with at least one item (root)
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Check structure of first tree
    root = data[0]
    assert "id" in root
    assert "label" in root
    assert "children" in root
    assert isinstance(root["children"], list)

@pytest.mark.asyncio
async def test_get_trees_unauthorized(setup_test_db, async_client):
    """Test that unauthorized requests are rejected."""
    response = await async_client.get("/api/tree")
    assert response.status_code == 403  # Forbidden

@pytest.mark.asyncio
async def test_create_node_endpoint(setup_test_db, auth_client):
    # First get the current trees to find a root node id
    response = await auth_client.get("/api/tree")
    trees = response.json()
    root_id = trees[0]["id"]
    
    # Test creating a child node
    node_data = {
        "label": "API Test Child",
        "parentId": root_id
    }
    
    response = await auth_client.post("/api/tree", json=node_data)
    
    # Check response
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "node" in data
    assert data["node"]["label"] == "API Test Child"
    assert data["node"]["parentId"] == root_id
    
    # Test creating a node with invalid parent
    invalid_node_data = {
        "label": "Invalid Parent",
        "parentId": 9999
    }
    
    response = await auth_client.post("/api/tree", json=invalid_node_data)
    assert response.status_code == 404
    
    # Test creating a new root node
    root_node_data = {
        "label": "New Root"
    }
    
    response = await auth_client.post("/api/tree", json=root_node_data)
    assert response.status_code == 201
    
    # Get trees again to verify our additions
    response = await auth_client.get("/api/tree")
    updated_trees = response.json()
    
    # Should have at least two root nodes now
    assert len(updated_trees) >= 2
    
@pytest.mark.asyncio
async def test_health_check(async_client):
    """Test the public health check endpoint."""
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}