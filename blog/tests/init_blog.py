import os
import sys
from blog.common.db import rw_session
from blog import app, root_dir
from blog.common.logger import logger


def caution():
    r = '\u001b[31m'
    b = '\u001b[34m'
    s = '\u001b[0m'
    text = f"""{r}
                       !! WARNING 警告 !!

    THIS SCRIPT WILL CLEAN ALL DATA IN THE FOLLOWING DATABASE
             本脚本将会清空以下数据库内的全部内容{s}

    {b}{app.config['MYSQL_RW']}{s}
    {b}{app.config['REDIS_RW']}{s}

PRESS Y TO CLEAN ALL DATA IN THE DATABASE, PRESS N TO EXIT RIGHT NOW
                 回答 Y 清除数据库，回答 N 立刻退出\n"""
    sys.stderr.write(text)


def init_db(need_confirm=True):
    if need_confirm:
        caution()
        confirm = input('Do you wanna procceed? (Y/N) ')
        if confirm.lower().strip() not in ('y', 'yes'):
            sys.stderr.write('Abort!!!\n')
            sys.exit(0)

    logger.info(f'start init database.')
    session = rw_session()
    with session.begin():
        old_tables = session.execute('show tables')
        for table in old_tables:
            session.execute(f'drop table {table[0]}')

        db_file = os.path.join(root_dir, 'blog/migrations/init_database.sql')
        with open(db_file) as f:
            sql = f.read()
            new_tables_sql = sql.split(';')
        for table_sql in new_tables_sql:
            if not table_sql.strip():
                continue
            session.execute(table_sql)
    logger.info(f'successfully init database.')
