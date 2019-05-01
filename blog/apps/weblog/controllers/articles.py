from blog.common.db import use_orm
from blog.models.article_tags import ArticleTag
from blog.models.articles import Article
from blog.models.categories import Category
from blog.models.tags import Tag


class ArticlesController:

    @classmethod
    @use_orm(name='rw')
    def get_article_list(cls, user_id, *, session):
        with session.begin():
            articles = session.query(Article).filter_by(user_id=user_id,
                                                        is_drop=0).all()
            article_list = []
            for article in articles:
                title = article.title
                description = article.description
                content = article.content
                scan_num = article.scan_num
                create_at = article.create_at

                category_id = article.category_id
                category = session.query(Category).filter_by(
                    id=category_id, is_drop=0).first()

                article_id = article.id
                article_tag_list = session.query(ArticleTag).filter_by(
                    article_id=article_id, is_drop=0).all()
                tags = []
                for article_tag in article_tag_list:

                    tag_id = article_tag.tag_id
                    tag = session.query(Tag).filter_by(id=tag_id,is_drop=0).first()
                    tags.append(tag.name)

                article = {'id':article.id, 'tags': tags, 'category': category.name,
                          'title': title, 'description': description,
                          'content': content, 'scan_num': scan_num,
                          'create_at': create_at}

                article_list.append(article)

            tagss = session.query(Tag).filter_by(user_id=user_id,is_drop=0).all()
            tag_list = [item.name for item in tagss]
            categoriess = session.query(Category).filter_by(
                user_id=user_id,is_drop=0).all()
            category_list = [item.name for item in categoriess]

        return dict(article_list=article_list, tag_list=tag_list,
                    category_list=category_list)


