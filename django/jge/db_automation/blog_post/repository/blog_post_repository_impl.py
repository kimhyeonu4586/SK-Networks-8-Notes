from blog_post.entity.blog_post import BlogPost
from blog_post.repository.blog_post_repository import BlogPostRepository


class BlogPostRepositoryImpl(BlogPostRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def list(self, page, perPage):
        offset = (page - 1) * perPage
        blogPostList = BlogPost.objects.all().order_by('-create_date')[offset:offset + perPage]
        totalItems = BlogPost.objects.count()

        return blogPostList, totalItems

    def save(self, blog_post: BlogPost) -> BlogPost:
        blog_post.save()
        return blog_post

    def findById(self, boardId):
        try:
            return BlogPost.objects.get(id=boardId)
        except BlogPost.DoesNotExist:
            return None
