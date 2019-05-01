from marshmallow import Schema, fields


class RequestWriteArticle(Schema):
    title = fields.String(load_from='title', required=True)
    description = fields.String(load_from='summary', required=True)
    content = fields.String(load_from='markdownContent', required=True)
    tags = fields.List(fields.String(), load_from='tags', required=True)
    category = fields.String(load_from='category', required=True)


class _Article(Schema):
    id = fields.Integer(dump_to='_id', required=True)
    tags = fields.List(fields.String(), dump_to='tags', required=True)
    category = fields.String(dump_to='category', required=True)
    title = fields.String(dump_to='title', required=True)
    description = fields.String(dump_to='summary', required=True)
    content = fields.String(dump_to='markdownContent', required=True)
    scan_num = fields.Number(dump_to='viewTimes', required=True)
    create_at = fields.Time(dump_to='createTime', required=True)


class ResponseArticleList(Schema):
    article_list = fields.Nested(_Article, dump_to='articleList', many=True)
    tag_list = fields.List(fields.String(), dump_to='tags', required=True)
    category_list = fields.List(fields.String(), dump_to='categories',
                                required=True)


class RequestDeleteArticle(Schema):
    article_id = fields.Integer(load_from='id', required=True)


class RequestArticle(Schema):
    article_id = fields.Integer(load_from='_id', required=True)
    title = fields.String(load_from='title', required=True)
    description = fields.String(load_from='summary', required=True)
    content = fields.String(load_from='markdownContent', required=True)
    tags = fields.List(fields.String(), load_from='tags', required=True)
    category = fields.String(load_from='category', required=True)


req_write_article = RequestWriteArticle(strict=True)
res_article_list = ResponseArticleList(strict=True)
req_delete_article = RequestDeleteArticle(strict=True)

req_article = RequestArticle(strict=True)
