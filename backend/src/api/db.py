import os
import time

from psycopg import OperationalError as PsycopgOpError
from sqlalchemy.exc import OperationalError as SAOpError
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL needs to be set.")

# If someone still uses postgres:// fix it
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )


# engine with pre_ping so dead connections are recycled
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db(retries: int = 10, delay: float = 2.0):
    """
    Try to create all tables, retrying if the DB isn't ready yet.
    """
    for attempt in range(1, retries + 1):
        try:
            print("creating database tables...")
            SQLModel.metadata.create_all(engine)
            print("database tables ready")
            return
        except (PsycopgOpError, SAOpError) as e:
            if attempt == retries:
                raise
            print(f"DB not ready ({attempt}/{retries}): {e}")
            time.sleep(delay)

def get_session():
    with Session(engine) as session:
        yield session
