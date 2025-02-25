<template>
  <v-container>
    <v-card>
      <v-card-title>이미지 등록</v-card-title>
      <v-card-text>
        <v-text-field v-model="title" label="갤러리 제목" outlined></v-text-field>

        <v-file-input 
          v-model="imageFile" 
          label="이미지 선택" 
          accept="image/*" 
          outlined 
          @change="previewImage"
        ></v-file-input>

        <v-img v-if="previewUrl" :src="previewUrl" class="mt-3" height="200px"></v-img>

        <v-btn color="primary" class="mt-3" @click="uploadImage">등록</v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
// npm update @aws-sdk/client-s3 @aws-sdk/lib-storage
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { S3Client } from '@aws-sdk/client-s3';
import { Upload } from '@aws-sdk/lib-storage';
import { useImageGalleryStore } from '~/stores/imageGalleryStore';
import { useRuntimeConfig } from 'nuxt/app';

import { createAwsS3Instance } from '~/utility/awsS3Instance';

const config = useRuntimeConfig();
const router = useRouter();
const imageGalleryStore = useImageGalleryStore();

const title = ref('');
const imageFile = ref(null);
const previewUrl = ref(null);

const previewImage = (event) => {
  const file = event.target.files[0];
  if (file) {
    console.log('📷 선택된 파일:', file);

    imageFile.value = file; // ✅ 파일을 imageFile에 저장
    previewUrl.value = URL.createObjectURL(file);
  }
};

const uploadImage = async () => {
  console.log('🚀 업로드 시작');

  if (!title.value || !imageFile.value) {
    alert("제목과 이미지를 모두 입력하세요.");
    console.log('❌ 제목 또는 이미지가 없음');
    return;
  }

  const file = imageFile.value;
  console.log('📁 업로드할 파일:', file);

  if (!file.name) {
    alert("올바른 이미지를 선택하세요.");
    console.log('❌ 파일명이 존재하지 않음');
    return;
  }

  const s3Client = createAwsS3Instance()

  const fileKey = `image_gallery/${file.name}`;
  console.log('📌 S3 업로드 경로:', fileKey);

  // ✅ Upload 사용 (파일 크기 자동 감지)
  const uploadParams = {
    Bucket: config.public.AWS_BUCKET_NAME,
    Key: fileKey,
    Body: file, // ✅ 수정된 부분 (file 자체 사용)
    ContentType: file.type,
  };

  console.log('📤 업로드 파라미터:', uploadParams);

  try {
    const upload = new Upload({
      client: s3Client,
      params: uploadParams,
    });

    upload.on("httpUploadProgress", (progress) => {
      console.log(`📊 업로드 진행률: ${progress.loaded} / ${progress.total}`);
    });

    await upload.done();
    console.log('✅ S3 Upload 성공');

    const imageUrl = `https://${config.public.AWS_BUCKET_NAME}.s3.${config.public.AWS_REGION}.amazonaws.com/${fileKey}`;

    await imageGalleryStore.requestRegisterImage({ title: title.value, imageUrl });

    alert("이미지가 성공적으로 등록되었습니다!");
    router.push('/image-gallery/list');
  } catch (error) {
    console.error('❌ S3 Upload Error:', error);
    alert("이미지 업로드 실패: " + error.message);
  }
};
</script>
