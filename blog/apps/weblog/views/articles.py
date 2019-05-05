from blog.apps.weblog.controllers.articles import ArticlesController
from blog.apps.weblog.schemas.articles import res_article_list, req_category, \
    req_tag
from blog.common.base_view import BaseView
from blog.common.schema import schema


class Articles(BaseView):
    route = '/articles/<string:nickname>'

    @schema(reply=res_article_list)
    def get(self, **kwargs):
        data = ArticlesController.get_article_list(kwargs['nickname'])
        return dict(data=data)


class CategoryArticles(BaseView):
    route = '/articles/category/<string:nickname>'

    @schema(json=req_category, reply=res_article_list)
    def get(self, **kwargs):
        json = kwargs['json']
        data = ArticlesController.get_categoryarticle_list(kwargs['nickname'],
                                                           json['category'])
        return dict(data=data)

class TagArticles(BaseView):
    route = '/articles/tag/<string:nickname>'

    @schema(json=req_tag, reply=res_article_list)
    def get(self, **kwargs):
        json = kwargs['json']
        data = ArticlesController.get_tagarticle_list(kwargs['nickname'],
                                                           json['tag'])
        return dict(data=data)