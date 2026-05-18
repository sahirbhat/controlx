from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

def register_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )