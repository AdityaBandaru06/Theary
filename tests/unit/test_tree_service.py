# tests/unit/test_tree_service.py
import pytest
from app.tree_service import build_tree, add_node
from app.db import initialize_db, nodes_collection, counters_collection

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
async def test_build_tree(setup_test_db):
    # Create a unique root node
    root = await add_node("unique_root", None)
    
    # Add children to the root
    child1 = await add_node("unique_child1", root["id"])
    child2 = await add_node("unique_child2", root["id"])
    
    # Add a grandchild
    grandchild = await add_node("unique_grandchild", child1["id"])
    
    # Build the tree
    tree = await build_tree()
    
    # Find our specific test root node in the returned trees
    test_root = next((node for node in tree if node["label"] == "unique_root"), None)
    
    # Verify our test root exists and has the right structure
    assert test_root is not None, "Root node not found in the tree"
    assert test_root["id"] == root["id"], f"Root ID mismatch: expected {root['id']}, got {test_root['id']}"
    assert len(test_root["children"]) == 2, "Root should have 2 children"
    
    # Verify the correct number of children
    assert len(test_root["children"]) == 2
    child_labels = {child["label"] for child in test_root["children"]}
    assert "unique_child1" in child_labels
    assert "unique_child2" in child_labels
    
    # Find child1 which should have a grandchild
    child_with_grandchild = next(
        (child for child in test_root["children"] if child["label"] == "unique_child1"),
        None
    )
    
    assert child_with_grandchild is not None, "Child1 node not found"
    assert len(child_with_grandchild["children"]) == 1, "Child1 should have 1 grandchild"
    assert child_with_grandchild["children"][0]["id"] == grandchild["id"], "Grandchild ID mismatch"
    assert child_with_grandchild["children"][0]["label"] == "unique_grandchild", "Incorrect grandchild label"

@pytest.mark.asyncio
async def test_add_node(setup_test_db):
    # Add a root node
    root = await add_node("new_root", None)
    assert root["label"] == "new_root"
    assert root["parentId"] is None
    
    # Add a child to this root
    child = await add_node("child", root["id"])
    assert child["label"] == "child"
    assert child["parentId"] == root["id"]
    
    # Try adding with invalid parent ID
    with pytest.raises(ValueError):
        await add_node("orphan", 9999)