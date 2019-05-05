from sqlalchemy import func

from blog.common.db import use_orm
from blog.models.articles import Article
from blog.models.categories import Category
from blog.models.users import User


class CategoryController:

    @classmethod
    @use_orm
    def get_category_list(cls, nickname, *, session):
        with session.begin():
            user = session.query(User).filter_by(nickname=nickname).first()
            user_id = user.id

            categories = session.query(Category).filter_by(user_id=user_id).all()
            category_list = []
            for item in categories:
                name = item.name
                category_id = item.id
                count = session.query(func.count(Article.id)).\
                    filter_by(user_id=user_id, category_id=category_id).scalar()


                category = dict(count=count,name=name)
                print(category, 999999999999999)
                category_list.append(category)


        return dict(category_list=category_list)




