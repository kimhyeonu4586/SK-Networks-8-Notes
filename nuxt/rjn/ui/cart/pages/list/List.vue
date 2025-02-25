<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Shopping Cart</v-card-title>
          <v-card-text>
            <v-table>
              <thead>
                <tr>
                  <th>Select</th>
                  <th>Title</th>
                  <th>Price</th>
                  <th>Quantity</th>
                  <th>Total</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in cartItems" :key="item.id">
                  <td>
                    <v-checkbox v-model="selectedItems" :value="item"></v-checkbox>
                  </td>
                  <td>{{ item.title }}</td>
                  <td>{{ item.price }}</td>
                  <td>
                    <v-text-field
                      v-model="item.quantity"
                      type="number"
                      min="1"
                      @change="updateQuantity(item)"
                    ></v-text-field>
                  </td>
                  <td>{{ item.price * item.quantity }}</td>
                  <td>
                    <v-btn color="red" @click="removeItem(item)">Remove</v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <v-divider></v-divider>
            <v-row justify="space-between" align="center">
              <v-col cols="6">
                <v-btn color="blue" @click="confirmCheckout">Checkout</v-btn>
              </v-col>
              <v-col cols="6" class="text-right">
                <strong>Total: {{ selectedItemsTotal }}</strong>
              </v-col>
            </v-row>
            <v-pagination
              v-model="currentPage"
              :length="totalPages"
              @input="fetchCartList"
            ></v-pagination>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Confirmation Dialog -->
    <v-dialog v-model="isCheckoutDialogVisible" max-width="500">
      <v-card>
        <v-card-title>Confirm Checkout</v-card-title>
        <v-card-text>
          Are you sure you want to order the selected items?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="isCheckoutDialogVisible = false"
          >Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="proceedToOrder">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useCartStore } from "~/cart/stores/cartStore"; // cartStore를 import
import { useOrderStore } from "~/order/stores/orderStore";

const selectedItems = ref([]);
const isCheckoutDialogVisible = ref(false);
const cartItems = ref([]);
const totalItems = ref(0);
const currentPage = ref(1);
const pageSize = ref(10); // 페이지 크기
const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value));

const router = useRouter();

const cartStore = useCartStore();  // cartStore 인스턴스
const orderStore = useOrderStore();

// 계산 속성
const selectedItemsTotal = computed(() =>
  selectedItems.value.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  )
);

// 메서드
const updateQuantity = (item) => {
  // 수량 업데이트 로직
  console.log(`Updating quantity for item ID: ${item.id}, New Quantity: ${item.quantity}`);
};

const removeItem = async (item) => {
  const result = await cartStore.requestRemoveCart(item.id);

  if (result.success) {
    // 요청이 성공하면 로컬 상태에서 해당 항목을 제거
    cartItems.value = cartItems.value.filter((cartItem) => cartItem.id !== item.id);
    selectedItems.value = selectedItems.value.filter((selectedItem) => selectedItem.id !== item.id);
  } else {
    // 실패한 경우에 대한 처리 (예: 알림 메시지 등)
    alert(result.error || "카트 삭제에 실패했습니다.");
  }
};

const confirmCheckout = () => {
  isCheckoutDialogVisible.value = true;
};

const proceedToOrder = async () => {
  isCheckoutDialogVisible.value = false;

  const selectedCartItems = selectedItems.value.map((item) => ({
    id: item.id,
    title: item.title,
    price: item.price,
    quantity: item.quantity,
  }));

  const userToken = localStorage.getItem("userToken");

  if (!userToken) {
    alert("로그인이 필요합니다. 다시 로그인해주세요.");
    return;
  }

  // router.push({
  //   path: '/payments/confirm',
  //   query: { items: encodeURIComponent(JSON.stringify(selectedCartItems)) },
  // });

  try {
    const response = await orderStore.requestCreateOrder({
      items: selectedCartItems,
      total: selectedItemsTotal.value,
      userToken: userToken,
    });

    if (response.success) {
      // 주문 생성 성공: 결제 페이지로 이동
      // router.push({
      //   path: "/payments/confirm",
      //   query: { orderId: response.orderId },
      // });
      router.push({
        path: '/payments/confirm',
        query: {
            orderId: response.orderId,
            items: encodeURIComponent(JSON.stringify(selectedCartItems))
        },
      });
    } else {
      // 주문 생성 실패: 사용자에게 알림
      alert(response.error || "주문 생성에 실패했습니다.");
    }
  } catch (error) {
    console.error("Error creating order:", error);
    alert("주문 처리 중 오류가 발생했습니다.");
  }
};

const fetchCartList = async () => {
  try {
    const userToken = localStorage.getItem("userToken");

    if (!userToken) {
      console.log("User token is missing.");
      return;
    }

    // currentPage와 pageSize가 숫자여야 하므로 객체가 아니라 숫자 값이 전달되어야 함
    const page = currentPage.value;  // 숫자 값이 전달
    const pageSizeValue = pageSize.value;  // 숫자 값이 전달

    console.log(`Fetching cart list with page: ${page}, perPage: ${pageSizeValue}, userToken: ${userToken}`);

    // cartStore.requestCartList 호출 시 매개변수가 객체가 아닌 숫자 값이 전달되도록 확인
    const response = await cartStore.requestCartList({
      page: page, 
      perPage: pageSizeValue,  // pageSize값을 명확히 전달
      userToken: userToken 
    });

    if (response.success) {
      cartItems.value = response.cartList;
      totalItems.value = response.totalItems;
      console.log("Cart items loaded:", cartItems.value);
    } else {
      alert(response.error || "카트 목록을 불러오는 데 실패했습니다.");
    }
  } catch (error) {
    console.error("Error fetching cart list:", error);
  }
};

watch(currentPage, (newPage) => {
  fetchCartList();  // 페이지 변경 시 fetchCartList 호출
});

onMounted(() => {
  // onMounted에서 비동기 호출이 완료되기 전에 호출되는 문제를 방지
  fetchCartList();
});
</script>

<style scoped>
/* 스타일은 필요에 따라 추가 */
</style>
