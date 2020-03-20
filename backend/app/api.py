"""Setup an API."""

from typing import List
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import requests
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="WirVsVirus", description="WirVsVirus!"
)

class User(BaseModel):
    """Define user model."""

    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False


@app.get("/users")
async def read_users_me() -> List[User]:
    """Return the current user information."""
    return []
