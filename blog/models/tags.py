from blog.common.db import Base
from sqlalchemy import Column, BigInteger, String


class Tag(Base):
    __tablename__ = 'tags'

    user_id = Column(BigInteger, unique=True)
    name = Column(String(64), unique=True)
    description = Column(String(255), default='')
