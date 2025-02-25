<template>
    <v-container>
        <v-row>
            <v-col cols="12" md="8" offset-md="2">
                <v-card>
                    <v-card-title>Create New Board</v-card-title>
                    <v-card-text>
                        <v-form ref="form" v-model="isValid" lazy-validation>
                            <v-text-field
                                    v-model="board.title"
                                    label="Title"
                                    :rules="[rules.required]"
                                    required
                            />
                            <v-textarea
                                    v-model="board.content"
                                    label="Content"
                                    :rules="[rules.required]"
                                    required
                            />
                            <v-btn
                                    :disabled="!isValid"
                                    color="primary"
                                    @click="submitBoard"
                            >
                                Submit
                            </v-btn>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useBoardStore } from "~/board/stores/boardStore"; // Pinia store

const router = useRouter();
const boardStore = useBoardStore();

const board = ref({
    title: '',
    content: ''
});

const isValid = ref(false);

const rules = {
    required: value => !!value || 'This field is required',
};

// 게시글 등록
const submitBoard = async () => {
    const userToken = localStorage.getItem('userToken');

    try {
        const response = await boardStore.requestCreateBoard({
            ...board.value,
            userToken, // 사용자 토큰 추가
        });

        if (response !== null) {
            // 게시글이 성공적으로 등록되면 리스트 페이지로 돌아가기
            router.push('/board/list');
        } else {
            alert('Failed to create board.');
        }
    } catch (error) {
        console.error('Error creating board:', error);
        alert('An error occurred while creating the board.');
    }
};
</script>
