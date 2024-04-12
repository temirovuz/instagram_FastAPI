from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import now

engine = create_engine('sqlite:///instagram.db')

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
