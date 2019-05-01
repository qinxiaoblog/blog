from blog import logger
from blog.apps.admin.controllers.tags import TagsController
from blog.apps.admin.schemas.tags import res_tags_data, req_insert_tag
from blog.common.base_view import BaseView

from blog.common.schema import schema
from blog.common.token import need_login


class UserTags(BaseView):
    route = '/tags'

    @schema(reply=res_tags_data)
    @need_login
    def get(self, **kwargs):
        data = TagsController.detail(kwargs['user_id'])
        return dict(data=data)

    @schema(json=req_insert_tag)
    @need_login
    def post(self, **kwargs):
        json = kwargs['json']
        TagsController.insert_tag(kwargs['user_id'], json['name'])

    @schema(json=req_insert_tag)
    @need_login
    def delete(self, **kwargs):
        json = kwargs['json']
        TagsController.delete_tag(kwargs['user_id'], json['name'])

