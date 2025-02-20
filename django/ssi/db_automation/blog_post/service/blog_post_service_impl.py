import uuid

from account.repository.account_repository_impl import AccountRepositoryImpl
from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl
from blog_post.entity.blog_post import BlogPost
from blog_post.repository.blog_post_repository_impl import BlogPostRepositoryImpl
from blog_post.service.blog_post_service import BlogPostService


class BlogPostServiceImpl(BlogPostService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__blogPostRepository = BlogPostRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__accountProfileRepository = AccountProfileRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestList(self, page, perPage):
        paginatedBlogPostList, totalItems = self.__blogPostRepository.list(page, perPage)

        totalPages = (totalItems + perPage - 1) // perPage

        paginatedFilteringBlogPostList = [
            {
                "id": blogPost.id,
                "title": blogPost.title,
                "nickname": blogPost.writer.nickname,  # writer 객체의 nickname 가져오기
                "createDate": blogPost.create_date.strftime("%Y-%m-%d %H:%M"),
            }
            for blogPost in paginatedBlogPostList
        ]

        print(f"paginatedFilteringBlogPostList: {paginatedFilteringBlogPostList}")

        return paginatedFilteringBlogPostList, totalItems, totalPages

    def requestUploadToS3(self, file, title):
        filename = f"{title}-{uuid.uuid4()}.html"

        print(f"filename: {filename}")

        return self.__blogPostRepository.uploadToS3(file, filename)

    def requestCreate(self, title, content, accountId):
        if not title or not content:
            raise ValueError("Title and content are required fields.")
        if not accountId:
            raise ValueError("Account ID is required.")

            # 2. Account 조회
        account = self.__accountRepository.findById(accountId)
        if not account:
            raise ValueError(f"Account with ID {accountId} does not exist.")

        # 3. AccountProfile 조회
        accountProfile = self.__accountProfileRepository.findByAccount(account)
        if not accountProfile:
            raise ValueError(f"AccountProfile for account ID {accountId} does not exist.")

        # 4. Board 객체 생성 및 저장
        blogPost = BlogPost(
            title=title,
            content=content,
            writer=accountProfile)  # ForeignKey로 연결된 account_profile)
        savedBlogPost = self.__blogPostRepository.save(blogPost)

        # 5. 응답 데이터 구조화
        return {
            "id": savedBlogPost.id,
            "title": savedBlogPost.title,
            "content": blogPost.content,
            "writerNickname": savedBlogPost.writer.nickname,
            "createDate": savedBlogPost.create_date.strftime("%Y-%m-%d %H:%M"),
        }

    def requestRead(self, id):
        blogPost = self.__blogPostRepository.findById(id)
        if blogPost:
            return {
                "id": blogPost.id,
                "title": blogPost.title,
                "content": blogPost.content,
                "createDate": blogPost.create_date.strftime("%Y-%m-%d %H:%M"),
                "nickname": blogPost.writer.nickname
            }

        return None

    def requestUpdate(self, id, title, accountId):
        try:
            account = self.__accountRepository.findById(accountId)
            accountProfile = self.__accountProfileRepository.findByAccount(account)

            blogPost = self.__blogPostRepository.findById(id)

            # 게시글 작성자와 요청한 사용자가 동일한지 확인
            if blogPost.writer.id != accountProfile.id:
                raise ValueError("You are not authorized to modify this post.")

            # 제목 업데이트
            blogPost.title = title

            # 게시글 저장 (수정)
            updatedBlogPost = self.__blogPostRepository.save(blogPost)

            # 수정된 게시글 반환
            return {
                "id": updatedBlogPost.id,
                "title": updatedBlogPost.title,
                "content": updatedBlogPost.content,
                "writerNickname": updatedBlogPost.writer.nickname,  # 작성자의 닉네임
                "createDate": updatedBlogPost.create_date.strftime("%Y-%m-%d %H:%M"),
            }

        except BlogPost.DoesNotExist:
            raise ValueError(f"BlogPost with ID {updatedBlogPost} does not exist.")
        except Exception as e:
            raise Exception(f"Error while modifying the post: {str(e)}")

    def requestDelete(self, id, accountId):
        try:
            account = self.__accountRepository.findById(accountId)
            accountProfile = self.__accountProfileRepository.findByAccount(account)

            blogPost = self.__blogPostRepository.findById(id)
            if not blogPost:
                raise ValueError(f"BlogPost with ID {id} does not exist.")

            if blogPost.writer.id != accountProfile.id:
                raise ValueError("You are not authorized to modify this post.")

            # 게시글 삭제 요청
            success = self.__blogPostRepository.deleteById(id)
            return success

        except Exception as e:
            raise Exception(f"게시글 삭제 중 오류 발생: {str(e)}")