from sqlalchemy import func

from blog import logger
from blog.models.article_tags import ArticleTag
from blog.models.blogs import Blog
from blog.common.db import use_orm
from blog.models.tags import Tag
from blog.models.users import User


class TagController:

    @classmethod
    @use_orm
    def get_tag_list(cls, nickname, *, session):
        with session.begin():
            user = session.query(User).filter_by(nickname=nickname).first()
            user_id = user.id

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
