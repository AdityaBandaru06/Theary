# app/models.py
from typing import List, Optional
from pydantic import BaseModel, Field

class NodeCreate(BaseModel):
    """Model for creating a new node."""
    label: str
    parentId: Optional[int] = None

class Node(BaseModel):
    """Model for a node without children."""
    id: int
    label: str
    parentId: Optional[int] = None

class NodeTree(BaseModel):
    """Model for a node with its children (recursive structure)."""
    id: int
    label: str
    children: List["NodeTree"] = []

# Required for recursive models in Pydantic
NodeTree.model_rebuild()