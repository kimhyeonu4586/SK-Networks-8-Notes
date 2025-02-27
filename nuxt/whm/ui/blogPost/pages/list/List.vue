<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            블로그 포스트
            <v-btn color="primary" @click="goToCreatePost" class="ml-2">
              글 작성하기
            </v-btn>
          </v-card-title>
          <v-card-text>
            <div v-if="postList.length === 0">
              <v-alert type="info">등록된 포스트가 없습니다.</v-alert>
            </div>

            <v-data-table
              v-else
              :items="postList"
              :headers="headerTitle"
              :items-per-page="pageSize"
              :page.sync="currentPage"
              v-model:pagination="pagination"
              class="elevation-1"
              @click:row="goToDetail"
              item-value="boardId"
              dense
            >
              <template #item.createDate="{ item }">
                {{ formatDate(item.createDate) }}
              </template>
            </v-data-table>

            <v-pagination
              v-model="currentPage"
              :length="totalPages"
              class="mt-3"
            ></v-pagination>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useBlogPostStore } from "~/stores/blogPostStore"; // Pinia store

const router = useRouter();
const blogPostStore = useBlogPostStore();

const postList = computed(() => {
  return blogPostStore.blogPostList.map((post) => ({
    boardId: post.id, // BlogPost의 id를 boardId로 사용
    title: post.title,
    nickname: post.nickname, // nickname만 그대로 사용
    createDate: post.createDate, // createDate를 그대로 사용
  }));
});

const totalPages = computed(() => blogPostStore.totalPages);
const currentPage = computed({
  get: () => blogPostStore.currentPage,
  set: (page) => {
    blogPostStore.currentPage = page;
  },
});

const pagination = ref({
  page: 1,
  itemsPerPage: 10,
});

const headerTitle = [
  { title: "No", align: "start", sortable: true, key: "boardId" },
  { title: "제목", align: "start", key: "title" },
  { title: "작성자", align: "start", key: "nickname" },
  { title: "작성일자", align: "start", key: "createDate" },
];

const pageSize = ref(10);

// Watch for changes in currentPage and call fetchPostList whenever it changes
watch(currentPage, async (newPage) => {
  await fetchPostList(newPage);
});

// Fetch post list based on the current page
const fetchPostList = async (page = 1) => {
  await blogPostStore.requestPostList({
    page,
    perPage: pageSize.value,
  });
};

// Redirect to post detail page
const goToDetail = (event, { item }) => {
  console.log("클릭한 아이템:", item);

  if (item && item.boardId) {
    router.push({ path: `/blog-post/read/${item.boardId}` });
  } else {
    console.error("게시글 ID가 없습니다:", item);
  }
};

// Redirect to create post page
const goToCreatePost = () => {
  router.push({ path: "/blog-post/register" });
};

// Format date to 'yyyy-mm-dd' style
const formatDate = (dateString) => {
  const options = { year: "numeric", month: "2-digit", day: "2-digit" };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

onMounted(() => fetchPostList(currentPage.value)); // Fetch on mount
</script>
