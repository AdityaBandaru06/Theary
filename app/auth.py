# In auth.py
import os
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable with no fallback default
API_KEY = os.getenv("API_KEY")

# Check if API_KEY is set on startup
if not API_KEY:
    raise ValueError(
        "API_KEY environment variable must be set. Please set a strong API key in your environment variables."
    )

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key_header)):
    """Verify that the API key is valid."""
    
    if api_key_header is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, 
            detail="API key missing"
        )
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, 
            detail="Invalid API key"
        )
    return api_key_header