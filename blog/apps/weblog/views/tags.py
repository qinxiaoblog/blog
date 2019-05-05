from blog.apps.weblog.controllers.tags import TagController
from blog.apps.weblog.schemas.tags import res_tags_list
from blog.common.base_view import BaseView
from blog.common.schema import schema


class TagsGetList(BaseView):
    route = '/tags/getList/<string:nickname>'

    @schema(reply=res_tags_list)
    def get(self, **kwargs):

        data = TagController.get_tag_list(kwargs['nickname'])
        return dict(data=data)
