import click
import os
from blog.tests.init_blog import init_db as initial_database


@click.group()
def cli():
    pass


@cli.command(help='init database，this will drop all data！')
def init_db():
    initial_database()


@cli.command(help='run blog backend server using gunicorn!')
def run():
    os.system('gunicorn blog:app')


if __name__ == '__main__':
    cli()
