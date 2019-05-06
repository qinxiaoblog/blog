from marshmallow import Schema, fields

from blog.apps.admin.schemas.articles import _Article


class ResponseArticleList(Schema):
    article_list = fields.Nested(_Article, dump_to='articleList', many=True)
    # tag_list = fields.List(fields.String(), dump_to='tags', required=True)
    # category_list = fields.List(fields.String(), dump_to='categories',
    #                             required=True)


class _Articles(Schema):
    id = fields.Integer(dump_to='_id', required=True)
    title = fields.String(dump_to='title', required=True)
    create_at = fields.Time(dump_to='createTime', required=True)
    tags = fields.List(fields.String(), dump_to='tags', required=True)


class ResponseArticleDataList(Schema):
    article_data_list = fields.List(
        fields.List(fields.Nested(_Articles)),
        dump_to='archivingList')


class RequestCategory(Schema):
    category = fields.String(load_from='category', required=True)


class RequestTag(Schema):
    tag = fields.String(load_from='tag', required=True)


class RequestArticle(Schema):
    id = fields.String(load_from='_id', required=True)


class ResponseArticle(Schema):
    id = fields.Integer(dump_to='_id', required=True)
    tags = fields.List(fields.String(), dump_to='tags', required=True)
    category = fields.String(dump_to='category', required=True)
    title = fields.String(dump_to='title', required=True)
    description = fields.String(dump_to='summary', required=True)
    content = fields.String(dump_to='markdownContent', required=True)
    scan_num = fields.Number(dump_to='viewTimes', required=True)
    create_at = fields.Time(dump_to='createTime', required=True)


res_article_list = ResponseArticleList(strict=True)
req_category = RequestCategory(strict=True)#
req_tag = RequestTag(strict=True)#
req_article = RequestArticle(strict=True) #
res_article_detail = ResponseArticle(strict=True)
article_data_list = ResponseArticleDataList(strict=True)
