<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Order Confirmation</v-card-title>
          <v-card-text>
            <!-- 상품 목록 -->
            <v-table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Price</th>
                  <th>Quantity</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in items" :key="item.id">
                  <td>{{ item.title }}</td>
                  <td>{{ item.price }}</td>
                  <td>{{ item.quantity }}</td>
                  <td>{{ item.price * item.quantity }}</td>
                </tr>
              </tbody>
            </v-table>

            <v-divider class="my-4"></v-divider>

            <!-- 결제 UI -->
            <div id="payment-method"></div>
            <!-- 이용약관 UI -->
            <div id="agreement"></div>

            <!-- 결제 로딩 상태 -->
            <v-progress-circular
              v-if="isProcessing"
              indeterminate
              color="primary"
              size="64"
              width="6"
              class="d-flex justify-center my-4"
            ></v-progress-circular>

            <!-- 결제 실패 메시지 -->
            <v-alert v-if="errorMessage" type="error">
              {{ errorMessage }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 결제하기 버튼을 오른쪽 하단에 배치 -->
    <v-row justify="end">
      <v-col cols="auto">
        <v-btn :disabled="isProcessing" @click="requestPayment" class="button" style="margin-top: 30px">
          결제하기
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { loadPaymentWidget, ANONYMOUS } from "@tosspayments/payment-widget-sdk";
import { useRuntimeConfig } from "nuxt/app";
import { nanoid } from "nanoid";
import { useRoute, useRouter } from "vue-router";
import { useAccountStore } from "~/account/stores/accountStore";
import { usePaymentStore } from "~/payments/stores/paymentsStore"

// 변수 선언
const config = useRuntimeConfig();
const paymentWidget = ref(null);
const paymentMethodWidget = ref(null);
const clientKey = ref(config.public.TOSS_CLIENT_KEY);
const inputEnabled = ref(false);
const amount = ref(0);
const discountCouponAmount = ref(5);
const items = ref([]);

// 라우터 및 쿼리
const route = useRoute();
const router = useRouter();

const totalAmount = ref(0);
const userToken = ref("");

const accountStore = useAccountStore();

// 로딩 상태 및 오류 메시지 관리
const isProcessing = ref(false);
const errorMessage = ref(null);

// 결제 UI 준비
onMounted(async () => {
  userToken.value = localStorage.getItem("userToken");

  // 쿼리 파라미터로 전달된 선택된 상품들
  if (route.query.items) {
    try {
      items.value = JSON.parse(decodeURIComponent(route.query.items));
      totalAmount.value = items.value.reduce(
        (total, item) => total + item.price * item.quantity,
        0
      );
      amount.value = totalAmount.value;
    } catch (error) {
      console.error("Error parsing query items:", error);
      router.push("/cart/list"); // 데이터가 잘못되었을 경우 카트로 이동
    }
  } else {
    router.push("/cart/list"); // 데이터가 없으면 카트로 이동
  }

  // 결제 위젯 초기화
  paymentWidget.value = await loadPaymentWidget(clientKey.value, ANONYMOUS);
  paymentMethodWidget.value = paymentWidget.value.renderPaymentMethods("#payment-method", { value: amount.value }, { variantKey: "DEFAULT" });
  paymentWidget.value.renderAgreement("#agreement", { variantKey: "AGREEMENT" });
  paymentMethodWidget.value.on("ready", () => {
    inputEnabled.value = true;
  });
});

// 결제 요청
const requestPayment = async () => {
  isProcessing.value = true; // 결제 진행 상태로 변경
  errorMessage.value = null; // 오류 메시지 초기화

  try {
    const customerEmail = await accountStore.requestEmail(userToken.value); // 고객 이메일

    const orderInfoId = route.query.orderId
    localStorage.setItem("oid", orderInfoId)

    if (paymentWidget.value) {
      await paymentWidget.value.requestPayment({
        orderId: nanoid(),
        orderName: generateOrderName(items.value), // 주문명
        customerName: "test", // 고객 이름 (필요시 수정)
        customerEmail: customerEmail, // 고객 이메일
        customerMobilePhone: "01012341234", // 고객 전화번호
        successUrl: `${window.location.origin}/payments/success`, // 성공 URL
        failUrl: `${window.location.origin}/payments/fail`, // 실패 URL
      });
    }
  } catch (error) {
    console.error("Payment failed:", error);
    errorMessage.value = "결제 실패! 다시 시도해 주세요.";
  } finally {
    isProcessing.value = false; // 결제 진행 상태 종료
  }
};

// 주문 이름 생성 함수
const generateOrderName = (items) => {
  const orderNames = items.map(item => `${item.title} ${item.quantity}개`);
  let orderName = orderNames.join(', ');

  // orderName 길이가 일정 이상일 경우 '...'으로 자르기
  const maxLength = 50; // 예를 들어 50자로 제한
  if (orderName.length > maxLength) {
    orderName = orderName.substring(0, maxLength) + '...';
  }

  return orderName;
};
</script>

<style scoped>
/* 필요한 스타일 추가 */
</style>
