from sqlalchemy import Column, String, BigInteger
from blog.common.db import Base


class LocalAuth(Base):

    __tablename__ = 'local_auth'

    user_id = Column(BigInteger, unique=True)
    password = Column(String(127))
