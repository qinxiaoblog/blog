from blog.apps.admin.controllers.categories import CategoriesController
from blog.apps.admin.schemas.categories import res_categories_data, \
    req_insert_category, req_delete_category
from blog.common.base_view import BaseView
from blog.common.schema import schema
from blog.common.token import need_login


class UserCategories(BaseView):
    route = '/categories'

    @schema(reply=res_categories_data)
    @need_login
    def get(self, **kwargs):
        data = CategoriesController.detail(kwargs['user_id'])
        return dict(data=data)

    @schema(json=req_insert_category)
    @need_login
    def post(self, **kwargs):
        json = kwargs['json']
        CategoriesController.insert_category(kwargs['user_id'], json['name'])

    @schema(json=req_delete_category)
    @need_login
    def delete(self, **kwargs):
        json = kwargs['json']
        CategoriesController.delete_category(kwargs['user_id'], json['name'])
