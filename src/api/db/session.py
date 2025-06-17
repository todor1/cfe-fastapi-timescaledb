from sqlmodel import SQLModel, Session
import timescaledb
from .config import DATABASE_URL, DB_TIMEZONE

if not DATABASE_URL:
    raise NotImplementedError("DATABASE_URL needs to be set.")

# engine = sqlmodel.create_engine(url=DATABASE_URL)
engine = timescaledb.create_engine(url=DATABASE_URL, timezone=DB_TIMEZONE)


def init_db():
    print("creating database")
    SQLModel.metadata.create_all(engine)
    print("creating hypertables")
    # the function below will look through all timescale model classes and create hypertables for them
    timescaledb.metadata.create_all(engine)


def get_session():
    """
    Will be used inside of our routes that need a database session.
    """
    with Session(engine) as session:
        yield session
