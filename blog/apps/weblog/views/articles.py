from blog.apps.weblog.controllers.articles import ArticlesController
from blog.apps.weblog.schemas.articles import res_article_list
from blog.common.base_view import BaseView
from blog.common.schema import schema


class Articles(BaseView):
    route = '/articles/<string:user_name>'

    @schema(reply=res_article_list)
    def get(self, **kwargs):

        data = ArticlesController.get_article_list(kwargs['user_id'])
        return dict(data=data)
