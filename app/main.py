import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .db import database
from .models import Users, Register, LogIn
from .security import hash_password, verify_password, create_jwt_token

from datetime import datetime, timezone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"], # параметр, в котором вы разрешаете конкретным доменам(фронтендам) обращаться к бэкенду
    allow_credentials=True, # параметр, в котором вы разрешаете передачу учетных данных(credentials) от фронтенда к бэкенду(Coockies, tokens, HTTP authentication)
    allow_methods=["GET", "POST", "PUT", "DELETE"], # параметр, определяющий какие HTTP методы могут испольвать фронтенд-приложения при обращении к вашему бэкенду
    allow_headers=["Content-type", "Authorization"], 
)

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

#РАБОТАЕТ АВТОМАТИЧЕСКИ
@app.on_event("startup")
async def startup():
    await database.connect()  # ← Инициализация пула при запуске

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()  # ← Корректное закрытие

@app.get("/users")
async def get_all_users():
    query = "SELECT id, name, email FROM users"
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query)
        users = [Users(id=record["id"], name=record["name"], email=record["email"]) for record in rows]
        return users
    
@app.post("/register")
async def register(user: Register):
    hashed_password = hash_password(user.password)
    created_at = datetime.now(timezone.utc)
    
    query = """
        INSERT INTO users (name, hashed_password, email, age, created_at) 
        VALUES ($1, $2, $3, $4, $5) 
    """
    async with database.pool.acquire() as connection:
        await connection.execute(
                query,
                user.name,
                hashed_password,  # ← хешированный пароль!
                user.email,
                user.age,
                created_at
            )
        
@app.post("/login")
async def login(user: LogIn):
    query = "SELECT id, email, hashed_password FROM users WHERE email = $1"
    
    async with database.pool.acquire() as connection:
        result = await connection.fetchrow(query, user.email)
        
        # result = await connection.execute(
        #     query,
        #     user.email
        # )
        
        if not result:
            raise HTTPException(status_code=401, detail="There is no such user")

        if not verify_password(user.password, result["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_jwt_token(
            data={"sub": result["email"], "user_id": result["id"] }
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": result["id"],
            "email": result["email"]
        }
    


app.mount("/static", StaticFiles(directory="static"), name="static")
    
    
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)