from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def get_db():
    from .config import settings

    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{settings.POSTGRES_USER}"
        f":{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}"
        f":{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
    )

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=True
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
