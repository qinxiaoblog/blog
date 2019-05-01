from marshmallow import Schema, fields

from blog.apps.admin.schemas.articles import _Article


class ResponseArticleList(Schema):
    article_list = fields.Nested(_Article, dump_to='articleList', many=True)
    tag_list = fields.List(fields.String(), dump_to='tags', required=True)
    category_list = fields.List(fields.String(), dump_to='categories',
                                required=True)

res_article_list = ResponseArticleList(strict=True)

