from blog.common.db import Base
from sqlalchemy import Column, BigInteger, String


class Category(Base):
    __tablename__ = 'categories'

    user_id = Column(BigInteger, unique=True)
    blog_id = Column(BigInteger, unique=True)
    name = Column(String(64), unique=True)
    description = Column(String(255), default='')
    position = Column(BigInteger, default=999)
