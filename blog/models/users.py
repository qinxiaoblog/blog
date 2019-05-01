from sqlalchemy import Column, String, Text
from blog.common.db import Base


class User(Base):

    __tablename__ = 'users'

    nickname = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    description = Column(String(255), default='')
    about_me = Column(Text, default='')
