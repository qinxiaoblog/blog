from blog.common.db import use_orm
from blog.models.blogs import Blog
from blog.models.categories import Category
from sqlalchemy import asc


class BlogController:
    @classmethod
    @use_orm(name='ro')
    def info(cls, blog_id, *, session):
        blog = session.query(Blog).filter_by(id=blog_id).first()
        categories = session.query(Category).filter_by(
            blog_id=blog.id).order_by(asc(Category.position)).all()

        blog.categories = categories
        return blog
