<template>
    <client-only>
        <v-container>
            <v-card>
                <v-card-title>블로그 포스트 수정</v-card-title>
                <v-card-text>
                    <v-text-field v-model="title" label="제목" outlined></v-text-field>

                    <div class="editor-container" v-if="QuillEditor">
                        <QuillEditor
                            v-model="content"
                            :options="editorOptions"
                            toolbar="full"
                            ref="quillEditorRef"
                        />
                    </div>

                    <v-card-actions class="justify-end">
                        <v-btn color="primary" class="mt-3" @click="submitPost">저장</v-btn>
                        <v-btn color="secondary" class="mt-3" @click="goBack">취소</v-btn>
                    </v-card-actions>
                </v-card-text>
            </v-card>
        </v-container>
    </client-only>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBlogPostStore } from "~/stores/blogPostStore";
import { createAwsS3Instance, getSignedUrlFromS3 } from '~/utility/awsS3Instance';
import { compressHTML } from '~/utility/compression';
import { useRuntimeConfig } from "nuxt/app";
import { PutObjectCommand } from "@aws-sdk/client-s3"; // ✅ 누락된 import 추가
import "@vueup/vue-quill/dist/vue-quill.snow.css";

const title = ref("");
const content = ref("");
const router = useRouter();
const route = useRoute();
const blogPostStore = useBlogPostStore();
const editorOptions = ref({
    theme: "snow",
    placeholder: "Write here...",
});

const QuillEditor = ref(null);
const quillEditorRef = ref(null);

const config = useRuntimeConfig();
let originalFilename = ""; // ✅ 기존 S3 파일명을 저장할 변수 추가

onMounted(async () => {
    console.log("Mounted: Dynamically loading QuillEditor...");
    const { QuillEditor: LoadedQuillEditor } = await import("@vueup/vue-quill");
    QuillEditor.value = LoadedQuillEditor;
    console.log("Mounted: QuillEditor loaded successfully.");

    const postId = route.params.id;
    const statePost = history.state.post;

    if (statePost) {
        console.log("Already has post data");
        title.value = statePost.title;
        originalFilename = statePost.content; // ✅ 기존 S3 파일명 저장
        const url = await getSignedUrlFromS3(`blog-post/${originalFilename}`);
        const response = await fetch(url);
        content.value = await response.text();
        nextTick(() => {
            const quillInstance = quillEditorRef.value?.getQuill();
            if (quillInstance) {
                quillInstance.root.innerHTML = content.value;
            }
        });
    } else if (postId) {
        console.log("Need to acquire post data");
        const data = await blogPostStore.requestReadPost(postId);
        if (data) {
            title.value = data.title;
            originalFilename = data.content; // ✅ 기존 S3 파일명 저장
            const url = await getSignedUrlFromS3(`blog-post/${originalFilename}`);
            const response = await fetch(url);
            content.value = await response.text();
            nextTick(() => {
                const quillInstance = quillEditorRef.value?.getQuill();
                if (quillInstance) {
                    quillInstance.root.innerHTML = content.value;
                }
            });
        }
    }
});

const uploadToS3 = async (content: string, filename: string) => {
    const s3Client = createAwsS3Instance();
    const params = {
        Bucket: config.public.AWS_BUCKET_NAME,
        Key: `blog-post/${filename}`,
        Body: content,
        ContentType: "text/html",
    };

    console.log("📝 S3 Upload Params:", params);

    try {
        const command = new PutObjectCommand(params);
        const data = await s3Client.send(command);
        console.log("✅ Content uploaded to S3:", data);
    } catch (err) {
        console.error("❌ Error uploading content to S3", err);
        throw new Error("S3 업로드 실패");
    }
};

const submitPost = async () => {
    console.log("🚀 Submit post started...");

    if (!title.value || !content.value) {
        alert("제목과 내용을 입력하세요.");
        return;
    }

    await nextTick(async () => {
        const quillInstance = quillEditorRef.value?.getQuill();
        if (!quillInstance) {
            console.error("❌ Quill instance is not available.");
            return;
        }

        const updatedContent = quillInstance.root.innerHTML;
        console.log("📄 HTML content to upload:", updatedContent);

        if (!updatedContent) {
            console.error("❌ Failed to extract content from QuillEditor.");
            return;
        }

        const compressedHTML = await compressHTML(updatedContent);
        console.log("📄 압축된 HTML:", compressedHTML);

        try {
            const postId = route.params.id;
            const postData = await blogPostStore.requestReadPost(postId); // 기존 데이터 가져오기
            const originalTitle = postData.title;
            const filename = postData.content; // ✅ 기존 S3 파일명 그대로 사용

            console.log("📝 S3 Upload Params:", filename);

            // ✅ S3에 HTML 업데이트 (항상 실행)
            await uploadToS3(compressedHTML, filename);

            // ✅ 제목이 변경된 경우만 Django에 업데이트 요청
            if (originalTitle !== title.value) {
                console.log("🔄 Title changed, updating Django...");
                await blogPostStore.requestUpdatePost({
                    id: postId,
                    title: title.value
                });
            }

            alert("블로그 포스트가 수정되었습니다!");
            router.push(`/blog-post/read/${postId}`);
        } catch (error) {
            console.error("❌ 블로그 포스트 수정 실패:", error);
            alert("포스트 수정 중 오류가 발생했습니다.");
        }
    });
};

const goBack = () => {
    router.push(`/blog-post/read/${route.params.id}`);
};
</script>
