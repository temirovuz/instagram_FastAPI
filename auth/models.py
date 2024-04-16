from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql.functions import now

from core.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(25), default=False)
    last_name = Column(String(25), default=False)
    username = Column(String(20), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
    signup_date = Column(DateTime(), server_default=now())
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return self.username
