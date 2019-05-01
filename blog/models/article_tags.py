from sqlalchemy import Column, String, BigInteger, Text
from blog.common.db import Base


class ArticleTag(Base):
    __tablename__ = 'article_tags'

    user_id = Column(BigInteger, unique=True)
    article_id = Column(BigInteger, unique=True)
    tag_id = Column(BigInteger, unique=True)
