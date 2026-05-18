from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.users.models import User
from core.security import verify_password, create_access_token, create_refresh_token,verify_token
from .schemas import LoginRequest






def login_service(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    data = {"sub": user.email, "role": user.role}
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_token_service(refresh_token: str):
    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    # generate new access token
    data = {"sub": payload["sub"], "role": payload["role"]}
    new_access_token = create_access_token(data)
    return {"access_token": new_access_token, "token_type": "bearer"}



def logout_service(refresh_token: str):
    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    # for now — just verify token is valid
    # later — blacklist in DB
    return {"message": "Logged out successfully"}