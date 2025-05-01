# app/db.py
import motor.motor_asyncio
from typing import Dict, Any, Optional, List
import os
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment or use default
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "tree_db")

# Create a new client and connect to the server
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Collections
nodes_collection = db.nodes
counters_collection = db.counters

# Helper class to convert MongoDB ObjectID to string
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

async def initialize_db():
    """Initialize the database with required collections and initial data."""
    # Check if counter exists, create if it doesn't
    counter = await counters_collection.find_one({"_id": "node_counter"})
    if not counter:
        await counters_collection.insert_one({"_id": "node_counter", "sequence_value": 0})
    
    # Check if root node exists, create if it doesn't
    root = await nodes_collection.find_one({"parentId": None})
    if not root:
        # Create a root node
        await create_node("root", None)

async def get_next_sequence_value() -> int:
    """Get the next ID for a new node."""
    result = await counters_collection.find_one_and_update(
        {"_id": "node_counter"},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    return result["sequence_value"]

async def create_node(label: str, parent_id: Optional[int] = None) -> Dict[str, Any]:
    """Create a new node in the database."""
    # Get next ID
    node_id = await get_next_sequence_value()
    
    # Create node document
    node = {
        "id": node_id,
        "label": label,
        "parentId": parent_id
    }
    
    # Insert into database
    result = await nodes_collection.insert_one(node)
    
    # Convert ObjectId to string before returning
    # This is important for JSON serialization
    node["_id"] = str(result.inserted_id)
    return node

async def get_all_nodes() -> List[Dict[str, Any]]:
    """Get all nodes from the database."""
    cursor = nodes_collection.find({})
    nodes = await cursor.to_list(length=None)
    
    # Convert ObjectId to string for each node
    for node in nodes:
        if "_id" in node:
            node["_id"] = str(node["_id"])
    
    return nodes

async def get_node_by_id(node_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific node by its ID."""
    node = await nodes_collection.find_one({"id": node_id})
    if node and "_id" in node:
        node["_id"] = str(node["_id"])
    return node