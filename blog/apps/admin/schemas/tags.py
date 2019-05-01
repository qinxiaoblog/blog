from marshmallow import Schema, fields


class ResponseTagsData(Schema):
    tags = fields.List(fields.String(), dump_to='tags')


class RequestInsertTag(Schema):
    name = fields.String(load_from='name', required=True)


res_tags_data = ResponseTagsData(strict=True)

req_insert_tag = RequestInsertTag(strict=True)
