from blog.apps.weblog.controllers.articles import ArticlesController
from blog.apps.weblog.schemas.articles import res_article_list, req_category, \
    req_tag, req_article, res_article_detail, article_data_list
from blog.common.base_view import BaseView
from blog.common.schema import schema


class Articles(BaseView):
    route = '/articles/<string:nickname>'

    @schema(reply=res_article_list)
    def get(self, **kwargs):
        data = ArticlesController.get_article_list(kwargs['nickname'])
        return dict(data=data)


class CategoryArticles(BaseView):
    route = '/articles/category/<string:nickname>/<string:category>'

    @schema(reply=res_article_list)
    def get(self, **kwargs):
        from flask import request
        print(request.full_path, 123)
        print(request.data, 123)
        print(request.args, 123)


        print(kwargs, 99999)
        data = ArticlesController.get_categoryarticle_list(kwargs['nickname'],
                                                           kwargs['category'])
        return dict(data=data)


class TagArticles(BaseView):
    route = '/articles/tag/<string:nickname>/<string:tag>'

    @schema(reply=res_article_list)
    def get(self, **kwargs):
        # json = kwargs['json']
        data = ArticlesController.get_tagarticle_list(
            kwargs['nickname'], kwargs['tag'])
        return dict(data=data)


class Article(BaseView):
    route = '/article/<int:id>'

    @schema(reply=res_article_detail)
    def get(self, **kwargs):
        #json = kwargs['json']
        data = ArticlesController.get_article_detail(kwargs['id'])
        return dict(data=data)


class ArticleArchiving(BaseView):
    route = '/articles/archiving/<string:nickname>'

    @schema(reply=article_data_list)
    def get(self, **kwargs):
        data = ArticlesController.get_article_bytime_list(
            kwargs['nickname'])
        return dict(data=data)
