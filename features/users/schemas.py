




from pydantic import EmailStr, Field, BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=5, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default="developer")  # admin, devops, developer
    phone: Optional[str] = None 

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    phone: Optional[str] = None 

    class Config:
        from_attributes = True








