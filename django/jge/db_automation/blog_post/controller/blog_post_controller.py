import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.status import HTTP_200_OK

from blog_post.service.blog_post_service_impl import BlogPostServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class BlogPostController(viewsets.ViewSet):
    blogPostService = BlogPostServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestBlogPostList(self, request):
        getRequest = request.GET
        page = int(getRequest.get("page", 1))
        perPage = int(getRequest.get("perPage", 8))
        paginatedBlogPostList, totalItems, totalPages = self.blogPostService.requestList(page, perPage)

        # JSON 응답 생성
        return JsonResponse({
            "dataList": paginatedBlogPostList,  # 게시글 정보 목록
            "totalItems": totalItems,  # 전체 게시글 수
            "totalPages": totalPages  # 전체 페이지 수
        }, status=status.HTTP_200_OK)

    def requestCreateBlogPost(self, request):
        postRequest = request.data
        print("📥 받은 데이터:", postRequest)

        title = postRequest.get("title")
        content = postRequest.get("content")
        userToken = postRequest.get("userToken")

        if not userToken:  # userToken이 없거나 빈 문자열이면 400 반환
            return JsonResponse(
                {"error": "User token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        accountId = self.redisCacheService.getValueByKey(userToken)
        print(f'requestCreateBlogPost() accountId: ${accountId}')

        if not accountId:  # userToken이 유효하지 않은 경우도 거부
            return JsonResponse(
                {"error": "Invalid user token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        savedBlogPost = self.blogPostService.requestCreate(title, content, accountId)

        return JsonResponse({"data": savedBlogPost}, status=status.HTTP_200_OK)

    def requestReadBlogPost(self, request, pk=None):
        try:
            if not pk:
                return JsonResponse({"error": "ID를 제공해야 합니다."}, status=400)

            print(f"requestGameSoftwareRead() -> pk: {pk}")
            readBlogPost = self.blogPostService.requestRead(pk)

            return JsonResponse(readBlogPost, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def requestUpdateBlogPost(self, request, pk=None):
        try:
            postRequest = request.data
            print(f"postRequest: {postRequest}")

            title = postRequest.get("title")

            # 필수 항목 체크
            if not title:
                return JsonResponse({"error": "Title are required."}, status=status.HTTP_400_BAD_REQUEST)

            userToken = postRequest.get("userToken")
            accountId = self.redisCacheService.getValueByKey(userToken)

            # 게시글 수정 요청 처리
            updatedBoard = self.blogPostService.requestUpdate(pk, title, accountId)

            return JsonResponse(updatedBoard, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
