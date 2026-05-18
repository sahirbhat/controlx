from .schemas import UserCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from  core.security import hash_password
from .models import User


def user_create_service(db: Session, user: UserCreate):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Email {user.email} already exists")
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
        is_active=True
    )
    db.add(new_user)
    db.flush()
    db.refresh(new_user)
    return new_user


def get_user_service(db: Session):
    result = db.query(User).all()  
    if not result:
        raise HTTPException(status_code=404, detail="No records found") 
    return result  



