from django.db import IntegrityError

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

    def findById(self, id):
        try:
            return BlogPost.objects.get(id=id)
        except BlogPost.DoesNotExist:
            return None

    def deleteById(self, id):
        try:
            # 게시글을 ID로 조회
            board = BlogPost.objects.get(id=id)
            board.delete()  # 게시글 삭제
            return True  # 삭제 성공

        except BlogPost.DoesNotExist:
            # 게시글이 존재하지 않으면 None을 반환
            print(f"게시글 ID {id}가 존재하지 않습니다.")
            return False  # 삭제 실패

        except IntegrityError as e:
            # 삭제 중에 발생한 예외 처리
            print(f"Error deleting board: {e}")
            return False  # 삭제 실패
