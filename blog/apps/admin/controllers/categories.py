from blog.common.db import use_orm
from blog.common.exceptions import ClientError, ErrorCode
from blog.models.blogs import Blog
from blog.models.categories import Category


class CategoriesController:
    @classmethod
    @use_orm(name='ro')
    def detail(cls, user_id, *, session):
        categories = session.query(Category).filter_by(user_id=user_id,is_drop = 0).all()
        ret = [item.name for item in categories]
        return dict(categories=ret)

    @classmethod
    @use_orm(name='rw')
    def insert_category(cls,user_id, name, *, session):
        category = session.query(Category).filter_by(name=name,
                                           user_id=user_id,is_drop=0).first()
        if category:
            raise ClientError(code=400, err=ErrorCode.ARGS_ERROR,
                              msg='该分类已存在')
        with session.begin():
            blog = session.query(Blog).filter_by( user_id=user_id).first()
            blog_id = blog.id
            category = Category(user_id=user_id, name=name,blog_id=blog_id)
            session.add(category)

    @classmethod
    @use_orm(name='rw')
    def delete_category(cls, user_id, name, *, session):
        category = session.query(Category).filter_by(name=name,
                                                  user_id=user_id,is_drop=0).first()
        if not category:
            raise ClientError(code=400, err=ErrorCode.ARGS_ERROR,
                                  msg='该分类不存在')
        with session.begin():
            category.is_drop = 1





