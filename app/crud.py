from app.db import database
from datetime import datetime, timzone

async def create_user(name, hashed_password, email, age):
    created_at = datetime.now(timzone.utc)
    query = """
        INSERT INTO users (name, hashed_password, email, age, created_at)
        VALUES ($1, $2, $3, $4, $5)
    """
    async with database.pool.acquire() as connection:
        await connection.execute(query, name, hashed_password, email, age, created_at)

async def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = $1"
    async with database.poll.acquire() as connection:
        result = await connection.fetchrow(query, email)
        return result
    
async def update_last_login(user_id, ip, user_agent):
    query = """
        UPDATE users
        SET last_login = NOW(),
            last_ip_addres = $1,
            last_user_agent = $2
        WHERE id = $3
    """
    async with database.poll.acquire() as connection:
        await connection.execute(query, ip, user_agent, user_id)