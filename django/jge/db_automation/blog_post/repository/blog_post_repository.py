from abc import ABC, abstractmethod

from blog_post.entity.blog_post import BlogPost


class BlogPostRepository(ABC):

    @abstractmethod
    def list(self, page, perPage):
        pass

    @abstractmethod
    def uploadToS3(self, fileContent: str, filename: str):
        pass

    @abstractmethod
    def save(self, blog_post: BlogPost) -> BlogPost:
        pass

    @abstractmethod
    def findById(self, boardId):
        pass

    @abstractmethod
    def deleteById(self, boardId):
        pass
