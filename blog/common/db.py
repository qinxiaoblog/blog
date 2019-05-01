from sqlalchemy import (
    Column, String, create_engine, BigInteger, Integer, DateTime)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from datetime import datetime
import functools

from blog import app


rw_engine = create_engine(app.config['MYSQL_RW'])
rw_session = sessionmaker(bind=rw_engine, autocommit=True)
ro_engine = create_engine(app.config['MYSQL_RO'])
ro_session = sessionmaker(bind=ro_engine, autocommit=True)


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(BigInteger, primary_key=True)
    remark = Column(String(255), default='')
    is_drop = Column(Integer, default=0)
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())


def use_orm(func=None, name='rw'):
    if func is None:
        return functools.partial(use_orm, name=name)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if name not in ('rw', 'ro'):
            raise Exception(f'MySQL connection name not found: {name}')
        session = rw_session() if name == 'rw' else ro_session()
        kwargs.update(session=session)
        ret_val = func(*args, **kwargs)
        return ret_val

    return wrapper
