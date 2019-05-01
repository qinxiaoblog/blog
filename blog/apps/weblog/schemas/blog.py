from marshmallow import fields, Schema


class _Category(Schema):
    id = fields.Integer(dump_to='categoryId')
    name = fields.String(dump_to='name')
    description = fields.String(dump_to='description')
    position = fields.Integer(dump_to='position')


class ResponseBlogInfo(Schema):
    id = fields.Integer(dump_to='blogId')
    user_id = fields.Integer(dump_only='userId')
    name = fields.String(dump_to='blogName')
    picture = fields.String(dump_to='picture')
    description = fields.String(dump_to='description')
    categories = fields.Nested(_Category, many=True)


res_blog_info = ResponseBlogInfo(strict=True)
