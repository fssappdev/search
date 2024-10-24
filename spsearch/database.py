from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from contextlib import contextmanager
import os


"""
This module sets up the database connection and session management for the MagazineDB.
It includes functions to initialize the database and provide a session for database operations.
"""

# Database URL
#URL_DB = "postgresql://postgres:password@localhost:55001/MagazineDB"
#URL_DB = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:55001/MagazineDB")
# Retrieve environment variables
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = "db"  # Assuming your PostgreSQL service in Docker Compose is named "db"
POSTGRES_PORT = "5432"  # Default PostgreSQL port

# Create the SQLAlchemy database URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()

def init_db():
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")


def get_db():
    """Provide a session to the request."""
    db = SessionLocal()
    try:
        yield db  # Provide the session to the caller
    finally:
        db.close()  # Ensure the session is closed after use
        