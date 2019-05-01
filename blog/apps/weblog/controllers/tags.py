from sqlalchemy import func

from blog import logger
from blog.models.article_tags import ArticleTag
from blog.models.blogs import Blog
from blog.common.db import use_orm
from blog.models.tags import Tag


class TagController:

    @classmethod
    @use_orm
    def detail(cls, nickname, *, session):
        with session.begin():
            blog = session.query(Blog).filter_by(name=nickname).first()
            user_id = blog.user_id

            tags = session.query(Tag).filter_by(user_id=user_id).all()
            tag_list = []
            for item in tags:
                name = item.name
                tag_id = item.id
                count = session.query(func.count(ArticleTag.id)).\
                    filter_by(user_id=user_id, tag_id=tag_id).scalar()
                print(count, 999999999999999)

                tag = dict(count=count,name=name)
                tag_list.append(tag)



        return dict(tag_list=tag_list)
