from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from .models.base import Base, metadata
from .models.users import User

db_url = settings.DATABASE_URL
if db_url is None:
    raise RuntimeError("DATABASE_URL environment variable not set")

engine = create_engine(db_url, pool_pre_ping=True, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()