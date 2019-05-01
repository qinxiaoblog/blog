from blog.apps.admin.controllers.articles import ArticlesController
from blog.apps.admin.schemas.articles import req_write_article, \
    res_article_list, req_delete_article, req_article
from blog.common.base_view import BaseView

from blog.common.schema import schema
from blog.common.token import need_login


class Articles(BaseView):
    route = '/articles'

    @schema(json=req_write_article)
    @need_login
    def post(self, **kwargs):
        json = kwargs['json']
        ArticlesController.insert_article(kwargs['user_id'], json['title'],
                                          json['description'], json['content'],
                                          json['tags'], json['category'])

    @schema(reply=res_article_list)
    @need_login
    def get(self, **kwargs):

        data = ArticlesController.get_article_list(kwargs['user_id'])
        return dict(data=data)

    @schema(json=req_delete_article)
    @need_login
    def delete(self, **kwargs):
        json = kwargs['json']
        ArticlesController.delete_article(json['article_id'])


class UpdateArticle(BaseView):
    route = '/article'

    @schema(json=req_article)
    @need_login
    def post(self, **kwargs):
        json = kwargs['json']
        ArticlesController.update_article(kwargs['user_id'], json['article_id'],
                                          json['title'], json['description'],
                                          json['content'],
                                          json['tags'], json['category'])



