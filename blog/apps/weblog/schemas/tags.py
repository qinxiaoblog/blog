from marshmallow import Schema, fields


class _Tag(Schema):
    name = fields.String(dump_to='name', required=True)
    count = fields.Integer(dump_to='count', required=True)


class ResponseTagsList(Schema):
    tag_list = fields.Nested(_Tag, dump_to='tagList', many=True)


res_tags_list = ResponseTagsList(strict=True)
