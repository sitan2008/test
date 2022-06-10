from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import config

cfg = config.DatabaseConfig()

DB_URL = cfg.get_db_url()

engine = create_engine(DB_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(bind=engine)