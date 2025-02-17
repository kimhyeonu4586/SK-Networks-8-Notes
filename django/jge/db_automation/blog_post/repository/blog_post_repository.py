from abc import ABC, abstractmethod

from blog_post.entity.blog_post import BlogPost


class BlogPostRepository(ABC):

    @abstractmethod
    def list(self, page, perPage):
        pass

    @abstractmethod
    def save(self, blog_post: BlogPost) -> BlogPost:
        pass

    @abstractmethod
    def findById(self, boardId):
        pass
