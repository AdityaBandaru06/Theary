# tests/unit/test_db.py
import pytest
import asyncio
from bson import ObjectId
from app.db import (
    initialize_db, 
    get_next_sequence_value, 
    create_node, 
    get_all_nodes,
    get_node_by_id,
    nodes_collection,
    counters_collection
)

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

@pytest.mark.asyncio
async def test_initialize_db(setup_test_db):
    # Check if counter exists
    counter = await counters_collection.find_one({"_id": "node_counter"})
    assert counter is not None
    assert "sequence_value" in counter
    
    # Check if root node exists
    root = await nodes_collection.find_one({"parentId": None})
    assert root is not None
    assert root["label"] == "root"

@pytest.mark.asyncio
async def test_get_next_sequence_value(setup_test_db):
    # Get initial value
    value1 = await get_next_sequence_value()
    # Get next value
    value2 = await get_next_sequence_value()
    
    # Second value should be one more than first
    assert value2 == value1 + 1

@pytest.mark.asyncio
async def test_create_node(setup_test_db):
    # Create a test node
    node = await create_node("test_node", None)
    
    # Check if node was created properly
    assert node is not None
    assert "id" in node
    assert node["label"] == "test_node"
    assert node["parentId"] is None
    
    # Create a child node
    child_node = await create_node("child_node", node["id"])
    assert child_node["parentId"] == node["id"]

@pytest.mark.asyncio
async def test_get_all_nodes(setup_test_db):
    # Create a few nodes
    await create_node("node1", None)
    await create_node("node2", None)
    
    # Get all nodes
    nodes = await get_all_nodes()
    
    # Should have at least 3 nodes (root + 2 new ones)
    assert len(nodes) >= 3
    
    # Check that ObjectIds are converted to strings
    for node in nodes:
        assert isinstance(node["_id"], str)

@pytest.mark.asyncio
async def test_get_node_by_id(setup_test_db):
    # Create a node
    new_node = await create_node("findable_node", None)
    
    # Find the node by id
    found_node = await get_node_by_id(new_node["id"])
    
    # Check that we found the right node
    assert found_node is not None
    assert found_node["id"] == new_node["id"]
    assert found_node["label"] == "findable_node"
    
    # Check for non-existent node
    non_existent = await get_node_by_id(9999)
    assert non_existent is None