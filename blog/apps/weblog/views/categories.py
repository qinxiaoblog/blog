from blog.apps.weblog.controllers.categories import CategoryController
from blog.apps.weblog.schemas.categories import res_category_list
from blog.common.base_view import BaseView
from blog.common.schema import schema


class CategoriesGetList(BaseView):
    route = '/categories/getList/<string:nickname>'

    @schema(reply=res_category_list)
    def get(self, **kwargs):

        data = CategoryController.get_category_list(kwargs['nickname'])
        return dict(data=data)

