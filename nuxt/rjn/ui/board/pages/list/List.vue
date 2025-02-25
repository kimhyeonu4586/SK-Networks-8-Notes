<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-card>
                    <v-card-title>
                        Board List
                        <v-btn
                            color="primary"
                            @click="goToCreateBoard"
                            class="ml-2"
                        >
                            게시글 작성하기
                        </v-btn>
                    </v-card-title>
                    <v-card-text>
                        <div v-if="boardList.length === 0">
                            <v-alert type="info">등록한 게시글이 없습니다.</v-alert>
                        </div>

                        <v-data-table
                            v-else
                            :items="boardList"
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
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useBoardStore } from '~/stores/boardStore'; // Assuming Pinia store

const router = useRouter();
const boardStore = useBoardStore();

const boardList = computed(() => {
    return boardStore.boardList.map(board => ({
        boardId: board.boardId,
        title: board.title,
        content: board.content,
        nickname: board.nickname,  // nickname만 그대로 사용
        createDate: board.createDate  // createDate를 그대로 사용
    }));
});

const totalPages = computed(() => boardStore.totalPages);
const currentPage = computed({
    get: () => boardStore.currentPage,
    set: (page) => {
        boardStore.currentPage = page;
    },
});

const pagination = ref({
    page: 1,
    itemsPerPage: 10
});

const headerTitle = [
    { title: 'No', align: 'start', sortable: true, key: 'boardId' },
    { title: '제목', align: 'end', key: 'title' },
    { title: '작성자', align: 'end', key: 'nickname' },
    { title: '작성일자', align: 'end', key: 'createDate' },
];

const pageSize = ref(10);

// Watch for changes in currentPage and call fetchBoardList whenever it changes
watch(currentPage, async (newPage) => {
    await fetchBoardList(newPage);
});

// Fetch board list based on the current page
const fetchBoardList = async (page = 1) => {
    await boardStore.requestBoardList({
        page,
        perPage: pageSize.value,
    });
};

// Redirect to board detail page
const goToDetail = (event, { item }) => {
    console.log("클릭한 아이템:", item);

    if (item && item.boardId) {
        router.push({ path: `/board/read/${item.boardId}` });
    } else {
        console.error("게시글 ID가 없습니다:", item);
    }
};

// Redirect to create board page
const goToCreateBoard = () => {
    router.push({ path: '/board/register' });
};

// Format date to 'yyyy-mm-dd' style
const formatDate = (dateString) => {
    const options = { year: "numeric", month: "2-digit", day: "2-digit" };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

onMounted(() => fetchBoardList(currentPage.value)); // Fetch on mount
</script>
