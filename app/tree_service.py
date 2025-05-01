# app/tree_service.py
from typing import List, Dict, Any, Optional
from .db import get_all_nodes, create_node, get_node_by_id
from .models import NodeTree

async def build_tree() -> List[NodeTree]:
    """Build a tree structure from all nodes in the database."""
    # Get all nodes from database
    nodes = await get_all_nodes()
    
    # Create a dictionary of nodes by ID for O(1) lookup
    nodes_dict = {node["id"]: node for node in nodes}
    
    # Initialize a dictionary to hold the tree structure
    tree_dict = {}
    
    # Initialize tree nodes (without children yet)
    for node in nodes:
        tree_dict[node["id"]] = {
            "id": node["id"],
            "label": node["label"],
            "children": []
        }
    
    # List to keep track of root nodes
    roots = []
    
    # Build the tree by assigning children to their parents
    for node in nodes:
        # If node has a parent
        if node["parentId"] is not None and node["parentId"] in tree_dict:
            # Add this node as a child of its parent
            parent = tree_dict[node["parentId"]]
            parent["children"].append(tree_dict[node["id"]])
        # If node is a root (no parent)
        elif node["parentId"] is None:
            roots.append(tree_dict[node["id"]])
    
    return roots

async def add_node(label: str, parent_id: Optional[int]) -> Dict[str, Any]:
    """Add a new node to the tree."""
    # If parent_id is provided, check if parent exists
    if parent_id is not None:
        parent = await get_node_by_id(parent_id)
        if not parent:
            raise ValueError(f"Parent node with ID {parent_id} not found")
    
    # Create the new node
    new_node = await create_node(label, parent_id)
    return new_node