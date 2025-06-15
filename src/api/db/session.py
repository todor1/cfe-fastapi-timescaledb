import sqlmodel
from sqlmodel import SQLModel, Session
from .config import DATABASE_URL

if not DATABASE_URL:
    raise NotImplementedError("DATABASE_URL needs to be set.")

engine = sqlmodel.create_engine(url=DATABASE_URL)


def init_db():
    print("creating database")
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Will be used inside of our routes that need a database session.
    """
    with Session(engine) as session:
        yield session
