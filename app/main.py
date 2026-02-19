import logfire 
import uvicorn

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.db import database

from app.routers import auth_router
from app.routers import profile_router

logfire.configure()


app = FastAPI()

logfire.instrument_fastapi(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"], # параметр, в котором вы разрешаете конкретным доменам(фронтендам) обращаться к бэкенду
    allow_credentials=True, # параметр, в котором вы разрешаете передачу учетных данных(credentials) от фронтенда к бэкенду(Coockies, tokens, HTTP authentication)
    allow_methods=["GET", "POST", "PUT", "DELETE"], # параметр, определяющий какие HTTP методы могут испольвать фронтенд-приложения при обращении к вашему бэкенду
    allow_headers=["Content-type", "Authorization"], 
)

app.include_router(auth_router.router)
app.include_router(profile_router.router_profile)

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.on_event("startup")
async def startup():
    await database.connect()  # ← Инициализация пула при запуске

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()  # ← Корректное закрытие

app.mount("/static", StaticFiles(directory="static"), name="static")

    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)