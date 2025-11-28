from pydantic import BaseModel, EmailStr

class Users(BaseModel):
    id: int
    name: str
    email: str
    
class Register(BaseModel):
    name: str
    password: str
    email: EmailStr
    age: int
    
class LogIn(BaseModel):
    email: str
    password: str
    