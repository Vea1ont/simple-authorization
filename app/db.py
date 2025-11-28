import asyncpg
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

class Postgres:
    def __init__(self, database_url):
        self.database_url = database_url
        self.pool = None  # ← Инициализируем как None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)  # ← Создаём пул
    
    async def disconnect(self):
        if self.pool:  # ← Проверяем существование
            await self.pool.close()
    def zxc(self):
        pass
database = Postgres(DATABASE_URL)