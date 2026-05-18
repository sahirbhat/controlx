from .schemas import UserCreate,UserResponse
from .models import User
from fastapi import status,HTTPException,APIRouter,Depends,Request
from sqlalchemy.orm import Session
from db.sessions import get_db
from .service import user_create_service,get_user_service
from core.rate_limit import limiter
from fastapi import Depends
from core.security import get_current_user
from fastapi_cache.decorator import cache
from core.cache import get_cache, set_cache



protected_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)



router = APIRouter(prefix="/users",tags=["Users"])


@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def user_create(request: Request,user:UserCreate,db:Session=Depends(get_db)):
    return user_create_service(db,user)




@protected_router.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cached = await get_cache("users:all")
    if cached:
        print("✅ FROM CACHE")
        return cached
    
    print("FROM DB")
    result = get_user_service(db)
    
    # convert to dict properly — exclude _sa_instance_state
    serialized = [UserResponse.from_orm(u).model_dump() for u in result]
    await set_cache("users:all", serialized, expire=60)
    
    return result
















