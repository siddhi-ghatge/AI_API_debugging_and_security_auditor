
import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database connection URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost/ai_api_analyzer"
)

# Project root folder (where main.py is located)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Aiven CA certificate path
CA_FILE = Path(
    os.getenv("DB_SSL_CA", str(PROJECT_ROOT / "ca.pem"))
)

# Configure SSL for Aiven MySQL
connect_args = {}

if "aivencloud.com" in DATABASE_URL:
    if not CA_FILE.is_file():
        raise FileNotFoundError(
            f"Aiven CA certificate not found: {CA_FILE}. "
            "Download the CA certificate from Aiven and save it as ca.pem."
        )

    connect_args["ssl"] = {
        "ca": str(CA_FILE)
    }

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=1800,
    future=True
)

# Database session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
