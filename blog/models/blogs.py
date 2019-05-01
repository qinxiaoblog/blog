from sqlalchemy import Column, String, BigInteger, Text
from blog.common.db import Base


class Blog(Base):

    __tablename__ = 'blogs'

    user_id = Column(BigInteger, unique=True)
    name = Column(String(64), unique=True)
    picture = Column(String(255), default='')
    description = Column(String(255), default='')

