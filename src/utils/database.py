from sqlmodel import create_engine, Session

from src.config import config


engine = create_engine(config.DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
