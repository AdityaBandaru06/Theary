from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from .models import NodeTree, NodeCreate
from .tree_service import build_tree, add_node
from .auth import verify_api_key

router = APIRouter()

@router.get("/tree", response_model=List[NodeTree])
async def get_trees(api_key: str = Depends(verify_api_key)):
    """
    Get all trees in the database.
    
    Returns a list of all root nodes with their nested children.
    """
    try:
        trees = await build_tree()
        return trees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve trees: {str(e)}")

@router.post("/tree", status_code=201)
async def create_node(
    node: NodeCreate, 
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Create a new node and attach it to the specified parent.
    
    If parentId is not provided, the node will be created as a root node.
    """
    try:
        new_node = await add_node(node.label, node.parentId)
        return {
            "message": "Node created successfully", 
            "node": {
                "id": new_node["id"],
                "label": new_node["label"],
                "parentId": new_node["parentId"]
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create node: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Public health check endpoint that doesn't require authentication.
    """
    return {"status": "ok"}