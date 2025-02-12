<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            이미지 갤러리
            <v-btn color="primary" class="ml-3" @click="goToRegister">추가</v-btn>
          </v-card-title>
          <v-card-text>
            <!-- No images available message -->
            <div v-if="imageList.length === 0">
              <v-alert type="info">등록된 사진이 없습니다.</v-alert>
            </div>

            <!-- Display gallery if there are images -->
            <v-row v-else>
              <v-col
                v-for="(image, index) in imageList"
                :key="index"
                cols="12" sm="6" md="4"
              >
                <v-card>
                  <v-img :src="image.imageUrl" alt="Gallery Image" height="200px" />
                  <v-card-title>{{ image.title }}</v-card-title>
                </v-card>
              </v-col>
            </v-row>
            
            <!-- Pagination -->
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
// npm install @aws-sdk/client-s3 --save-dev
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useImageGalleryStore } from '~/stores/imageGalleryStore'; // Pinia store

const imageGalleryStore = useImageGalleryStore();
const router = useRouter();

const imageList = computed(() => imageGalleryStore.imageGalleryList);
const currentPage = computed({
  get: () => imageGalleryStore.currentPage,
  set: (page) => imageGalleryStore.requestImageList({ page, perPage: 10 }),
});
const totalPages = computed(() => imageGalleryStore.totalPages);

const goToRegister = () => {
  router.push('/image-gallery/register'); // 등록 페이지로 이동
};

onMounted(async () => {
  await imageGalleryStore.requestImageList({ page: currentPage.value, perPage: 10 });
});
</script>
