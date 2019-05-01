from marshmallow import Schema, fields


class ResponseCategoriesData(Schema):
    categories = fields.List(fields.String(), dump_to='categories')


class RequestInsertCategory(Schema):
    name = fields.String(load_from='name', required=True)


class RequestDeleteCategory(Schema):
    name = fields.String(load_from='name', required=True)

res_categories_data = ResponseCategoriesData(strict=True)
req_insert_category = RequestInsertCategory(strict=True)
req_delete_category = RequestDeleteCategory(strict=True)