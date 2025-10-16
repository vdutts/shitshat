import reflex as rx
from sqlmodel import create_engine, Session
from app.db import models
from contextlib import contextmanager
import os
import logging

config = rx.config.get_config()
connect_args = (
    {"check_same_thread": False} if config.db_url.startswith("sqlite") else {}
)
engine = create_engine(
    config.db_url,
    echo=False,
    connect_args=connect_args,
    pool_size=int(os.getenv("POOL_SIZE", "20")),
    max_overflow=int(os.getenv("MAX_OVERFLOW", "10")),
)


def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)


@contextmanager
def get_db_session():
    """Provide a transactional scope around a series of operations."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.exception(f"Error with database session: {e}")
        raise
    finally:
        session.close()