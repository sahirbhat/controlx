# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app
from db.sessions import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base

TEST_DATABASE_URL = "postgresql://admin:admin123@localhost:5432/controlx_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)