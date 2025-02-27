<template>
  <v-container>
    <v-card>
      <v-card-title>{{ post?.title || "제목 없음" }}</v-card-title>
      <v-card-subtitle
        >{{ post?.nickname }} |
        {{ formatDate(post?.createDate) }}</v-card-subtitle
      >
      <v-card-text>
        <!-- 🔥 HTML 그대로 삽입 -->
        <div class="post-content" v-html="postContent"></div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <!-- This spacer pushes the buttons to the right -->

        <!-- 목록으로 돌아가기 버튼 -->
        <v-btn color="primary" @click="goBack">목록으로</v-btn>

        <!-- 수정 버튼 -->
        <!-- <v-btn color="secondary" @click="goEdit" v-if="canEdit">수정</v-btn> -->
        <v-btn color="secondary" @click="goUpdate">수정</v-btn>

        <!-- 삭제 버튼 -->
        <!-- <v-btn color="red" @click="deletePost" v-if="canDelete">삭제</v-btn> -->
        <v-btn color="red" @click="deletePost">삭제</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBlogPostStore } from "~/stores/blogPostStore";
import { getSignedUrlFromS3, deleteFileFromS3 } from "~/utility/awsS3Instance";

const route = useRoute();
const router = useRouter();
const blogPostStore = useBlogPostStore();
const post = ref(null);
const postContent = ref("");

const fetchPostDetail = async () => {
  const postId = route.params.id;
  if (!postId) return;

  try {
    const data = await blogPostStore.requestReadPost(postId);
    if (data) {
      post.value = data;

      // S3에서 HTML 파일 다운로드
      if (data.content) {
        const url = await getSignedUrlFromS3(`blog-post/${data.content}`);
        const response = await fetch(url);
        postContent.value = await response.text();

        blogPostStore.blogPostContent = postContent.value;
      }
    }
  } catch (error) {
    console.error("게시글을 불러오는 데 실패했습니다.", error);
  }
};

const goBack = () => {
  router.push("/blog-post/list");
};

const goUpdate = () => {
  const postId = route.params.id;
  if (postId) {
    router.push({
      path: `/blog-post/update/${postId}`,
      state: { post: post.value }, // ✅ 현재 포스트 데이터 전달
    });
  }
};

const deletePost = async () => {
  const postId = route.params.id;
  if (!postId) return;

  if (!confirm("정말 삭제하시겠습니까?")) return;

  try {
    await blogPostStore.requestDeletePost(postId);

    if (post.value?.content) {
      await deleteFileFromS3(`blog-post/${post.value.content}`);
    }

    alert("게시글이 삭제되었습니다.");
    router.push("/blog-post/list");
  } catch (error) {
    console.error("게시글 삭제에 실패했습니다.", error);
    alert("게시글 삭제에 실패했습니다.");
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString("ko-KR");
};

onMounted(fetchPostDetail);
</script>

<style scoped>
.post-content {
  max-width: 100%;
  overflow-wrap: break-word; /* 긴 텍스트 줄바꿈 */
}

/* 🔥 이미지 스타일 추가 */
.post-content img {
  max-width: 100%; /* 이미지가 카드 너비를 벗어나지 않도록 */
  height: auto;
  display: block;
  margin: 10px auto;
}
</style>
