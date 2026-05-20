from fastapi import FastAPI
from db.sessions import engine
from db.base import Base
import features.users.models
from features.users.router import router as users_router, protected_router
from core.exceptions import register_exception_handlers
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.rate_limit import limiter
from features.auth.router import router as auth_router
from middlewares.logging_middleware import log_requests
from middlewares.cors_middleware import add_cors
from contextlib import asynccontextmanager
from core.cache import setup_cache
import uvicorn
from features.notifications.router import router as notifications_router

features.users.models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_cache()
    yield

app = FastAPI(title="ControlX", version="1.0.0", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
register_exception_handlers(app)
add_cors(app)
app.middleware("http")(log_requests)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(protected_router, prefix="/api/v1")

app.include_router(notifications_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)