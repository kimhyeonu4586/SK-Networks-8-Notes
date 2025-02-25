<template>
  <!-- Game Software 상세 정보 표시 페이지 -->
  <v-container>
    <h2>상품 세부 사항 보기</h2>

    <!-- 로딩 중일 때 스피너 표시 -->
    <v-row v-if="isLoading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="grey lighten-5" />
      </v-col>
    </v-row>

    <!-- 게임 소프트웨어 상세 정보 표시 -->
    <v-row v-else>
      <v-col cols="12">
        <!-- 이미지 표시 -->
        <v-img :src="getGameSoftwareImageUrl(gameSoftware.image)" aspect-ratio="1" class="grey lighten-2">
          <template v-slot:placeholder>
            <v-row class="fill-height ma-0" align="center" justify="center">
              <v-progress-circular indeterminate color="grey lighten-5"/>
            </v-row>
          </template>
        </v-img>
      </v-col>

      <v-col cols="12">
        <v-card>
          <v-card-title>상품 정보</v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="gameSoftware.title" readonly label="상품명" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="gameSoftware.description" readonly label="상품 설명" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="gameSoftware.price" readonly label="가격" type="number" />
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>

        <v-btn color="primary" @click="onPurchase" class="action-button" style="float: right;">
          <v-icon>mdi-cart</v-icon>
          <span class="button-text">구매하기</span>
        </v-btn>
        <v-btn color="success" @click="onAddToCart" class="action-button" style="float: right;">
          <v-icon>mdi-cart-plus</v-icon>
          <span class="button-text">장바구니에 추가</span>
        </v-btn>
        <!-- 목록으로 돌아가기 -->
        <NuxtLink to="/game-software/list" class="router-link no-underline">
          <v-btn color="secondary" class="action-button" style="float: right;">
            <v-icon>mdi-arrow-left</v-icon>
            <span class="button-text">목록으로 돌아가기</span>
          </v-btn>
        </NuxtLink>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCartStore } from '~/cart/stores/cartStore';
import { useGameSoftwareStore } from '../../stores/gameSoftwareStore';

interface ImageModule {
  default: string;
}

const gameSoftwareStore = useGameSoftwareStore();
const cartStore = useCartStore()

const route = useRoute();
const gameSoftwareId = route.params.id
console.log(`현재 읽은 id: ${gameSoftwareId}`)

const isLoading = ref(true);
const gameSoftware = ref({
  id: '',
  title: '',
  price: '',
  description: '',
  image: '',
});

const images = import.meta.glob('@/assets/images/uploadImages/*', { eager: true }) as Record<string, ImageModule>;

const getGameSoftwareImageUrl = (imageName: string) => {
  const imagePathKey = `/assets/images/uploadImages/${imageName}`;
  const imagePath = images[imagePathKey];
  return imagePath ? imagePath.default : '/assets/images/default-image.jpg';
};

const router = useRouter()

const onAddToCart = async () => {
  if (gameSoftware.value) {
    const userToken = localStorage.getItem("userToken") || "";

    const requestForm = {
      id: Number(gameSoftware.value.id),
      userToken: userToken,
      quantity: 1,
    };

    try {
      const response = await cartStore.requestCartSave(requestForm);
      console.log('장바구니에 아이템을 성공적으로 추가했습니다.', response.data);

      router.push('/cart/list');
    } catch (error) {
      console.error('장바구니 추가에 실패했습니다:', error);
    }
  }
}

onMounted(async () => {
  const { id } = route.params;

  const software = await gameSoftwareStore.requestGameSoftwareById(id as string);
  if (software) {
    gameSoftware.value = software;
  }
  isLoading.value = false;
});
</script>

<style scoped>
</style>
