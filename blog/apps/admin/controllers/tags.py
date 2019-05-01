from blog import logger
from blog.common.db import use_orm
from blog.common.exceptions import ErrorCode, ClientError
from blog.models.tags import Tag


class TagsController:
    @classmethod
    @use_orm(name='ro')
    def detail(cls, user_id, *, session):
        tags = session.query(Tag).filter_by(user_id=user_id,is_drop=0).all()
        ret = [item.name for item in tags]
        return dict(tags=ret)

    @classmethod
    @use_orm(name='rw')
    def insert_tag(cls, user_id, name, *, session):
        tag = session.query(Tag).filter_by(name=name, user_id=user_id,is_drop=0).first()
        if tag:
            raise ClientError(code=400, err=ErrorCode.ARGS_ERROR,
                              msg='该标签已存在')
        with session.begin():
            tag = Tag(user_id=user_id, name=name)
            session.add(tag)


    @classmethod
    @use_orm(name='rw')
    def delete_tag(cls, user_id, name, *, session):
        tag = session.query(Tag).filter_by(name=name, user_id=user_id,is_drop=0).first()
        logger.info(tag)
        if not tag:
            raise ClientError(code=400, err=ErrorCode.ARGS_ERROR,
                              msg='该标签不存在')
        with session.begin():
            tag.is_drop = 1

