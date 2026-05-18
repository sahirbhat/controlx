from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.sessions import get_db
from .schemas import LoginRequest, TokenResponse,AccessTokenResponse,RefreshRequest
from .service import login_service,refresh_token_service,logout_service

router = APIRouter(prefix="/auth", tags=["Auth"])


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return login_service(db, form_data.username, form_data.password)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(request: RefreshRequest):
    return refresh_token_service(request.refresh_token)


from .schemas import LogoutRequest

@router.post("/logout")
async def logout(request: LogoutRequest):
    return logout_service(request.refresh_token)



