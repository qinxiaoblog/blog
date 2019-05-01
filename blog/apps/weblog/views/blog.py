from blog.apps.weblog.controllers.blog import BlogController
from blog.common.base_view import BaseView
from blog.common.schema import schema
from blog.apps.weblog.schemas.blog import res_blog_info


class BlogInfo(BaseView):
    route = '/blog/<int:blog_id>'

    @schema(reply=res_blog_info)
    def get(self, **kwargs):
        data = BlogController.info(kwargs['blog_id'])
        return dict(data=data)
