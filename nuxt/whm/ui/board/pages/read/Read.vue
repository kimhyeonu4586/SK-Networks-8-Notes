<template>
  <v-container class="pa-4">
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title>
            <span class="headline">게시글 상세</span>
            <v-spacer />
            <v-btn color="primary" @click="goToListPage" icon>
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
          </v-card-title>

          <v-card-subtitle>
            <v-row>
              <v-col cols="6">
                <strong>작성자:</strong> {{ boardDetails.writer.nickname }}
              </v-col>
              <v-col cols="6" class="text-right">
                <strong>작성일:</strong>
                {{ formatDate(boardDetails.createDate) }}
              </v-col>
            </v-row>
          </v-card-subtitle>

          <v-divider />

          <!-- 제목 -->
          <v-card-text>
            <div class="font-weight-bold">제목: {{ boardDetails.title }}</div>
          </v-card-text>

          <v-divider />
          <!-- 제목과 내용 사이의 구분선 -->

          <!-- 내용 -->
          <v-card-text>
            <div>{{ boardDetails.content }}</div>
          </v-card-text>

          <v-divider />

          <v-card-actions>
            <v-btn color="primary" @click="goToListPage">목록으로</v-btn>
            <v-btn color="orange" @click="goToEditPage">수정</v-btn>
            <v-btn color="red" @click="deleteBoard">삭제</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { useBoardStore } from "~/stores/boardStore";

const router = useRouter();
const boardStore = useBoardStore();

// boardId를 route에서 가져옴
const boardId = router.currentRoute.value.params.boardId;
const boardDetails = ref({
  title: "",
  writer: "",
  createDate: "",
  content: "",
});

// 게시글 정보를 요청하는 함수
const fetchBoardDetails = async () => {
  try {
    await boardStore.requestReadBoard(boardId);
    if (boardStore.board) {
      // 응답 데이터에서 필요한 필드를 boardDetails에 매핑
      boardDetails.value = {
        title: boardStore.board.title,
        writer: { nickname: boardStore.board.nickname },
        createDate: boardStore.board.createDate,
        content: boardStore.board.content,
      };
    } else {
      console.error("게시글 정보를 가져오는 데 실패했습니다.");
    }
  } catch (error) {
    console.error("게시글 요청 중 에러 발생:", error);
  }
};

// 날짜 형식 포맷 함수
const formatDate = (dateString) => {
  const options = { year: "numeric", month: "2-digit", day: "2-digit" };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// 목록 페이지로 이동하는 함수
const goToListPage = () => {
  router.push("/board/list");
};

// 수정 페이지로 이동하는 함수
const goToEditPage = () => {
  router.push(`/board/modify/${boardId}`);
};

// 게시글 삭제 함수
const deleteBoard = async () => {
  const confirmDelete = confirm("정말로 게시글을 삭제하시겠습니까?");
  if (confirmDelete) {
    try {
      const userToken = localStorage.getItem("userToken");
      await boardStore.requestDeleteBoard(boardId, userToken);
      router.push("/board/list"); // 삭제 후 목록 페이지로 리디렉션
    } catch (error) {
      console.error("게시글 삭제 중 에러 발생:", error);
    }
  }
};

// 컴포넌트가 마운트될 때 데이터 요청
onMounted(fetchBoardDetails);
</script>
