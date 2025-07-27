from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import Settings


engine = create_engine(Settings.get_db_url(), pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
