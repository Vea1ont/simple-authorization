from fastapi import APIRouter

from app.db import database
from app.models import Users

router_user = APIRouter(prefix="/users", tags=["Users"])

@router_user.get("/")
async def get_all_users():
    query = "SELECT id, name, email FROM users"
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query)
        users = [Users(id=record["id"], name=record["name"], email=record["email"]) for record in rows]
        return users
    
@router_user.get("/me")
async def get_current_user():
    pass

@router_user.delete("/me")
async def delete_account():
    pass
    
