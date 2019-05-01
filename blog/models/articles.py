from sqlalchemy import Column, String, BigInteger, Text
from blog.common.db import Base


class Article(Base):

    __tablename__ = 'articles'

    user_id = Column(BigInteger, unique=True)
    category_id = Column(BigInteger, unique=True)
    title = Column(String(64), unique=True)
    first_image = Column(String(255), default='')
    description = Column(String(255), default='')
    content = Column(Text, unique=True)
    scan_num = Column(BigInteger, default=0)
    thumbs_num = Column(BigInteger, default=0)
