<template>
  <v-container class="mt-10">
    <!-- 로딩 중일 때 표시 -->
    <v-row v-if="isProcessing" justify="center" align="center">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary" size="64" />
        <div>결제 확인 중...</div>
      </v-col>
    </v-row>

    <!-- 결제 완료 후 데이터 표시 -->
    <v-card v-else class="mx-auto" max-width="600">
      <v-card-title>결제 완료</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="6"><b>결제금액:</b></v-col>
          <v-col cols="6" class="text-right">{{ jsonData.amountWithCurrency }}</v-col>
        </v-row>
        <v-row>
          <v-col cols="6"><b>결제 시간:</b></v-col>
          <v-col cols="6" class="text-right">{{ formattedApprovedAt }}</v-col>
        </v-row>
        <v-row>
          <v-col cols="6"><b>주문 항목:</b></v-col>
          <v-col cols="6" class="text-right">{{ jsonData.orderName }}</v-col>
        </v-row>
        <v-row>
          <v-col cols="6"><b>결제 방법:</b></v-col>
          <v-col cols="6" class="text-right">{{ jsonData.method }}</v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="redirectToDocs">연동 문서</v-btn>
        <v-btn color="secondary" @click="redirectToSupport">실시간 문의</v-btn>
        <!-- 홈으로 돌아가는 확인 버튼 추가 -->
        <v-btn color="success" @click="redirectToHome">확인</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { usePaymentStore } from "~/payments/stores/paymentsStore";
import { useOrderStore } from "~/order/stores/orderStore";

const route = useRoute();
const router = useRouter();
const paymentStore = usePaymentStore();
const orderStore = useOrderStore()

const confirmed = ref(false);
const jsonData = ref(null);
const isProcessing = ref(true); // 로딩 상태 초기화

// 날짜 포맷팅 함수
function formatDate(dateString) {
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false, // 24시간 형식
  };

  const date = new Date(dateString);
  return date.toLocaleString('ko-KR', options); // 한국어 형식으로 출력
}

const formattedApprovedAt = computed(() => {
  return jsonData.value ? formatDate(jsonData.value.approvedAt) : '';
});

async function confirmPayment() {
  try {
    const userToken = localStorage.getItem("userToken");
    if (!userToken) {
      console.error("User token not found");
      router.push("/login"); // 토큰이 없으면 로그인 페이지로 이동
      return;
    }

    // const orderInfoId = orderStore.getOrderInfoId();  // Pinia store에서 orderInfoId 가져오기
    const orderInfoId = localStorage.getItem("oid")
    if (!orderInfoId) {
      console.error("Order Info ID is missing");
      router.push("/payment/fail?message=Order Info ID is missing");
      return;
    }

    const requestForm = {
      paymentKey: route.query.paymentKey,
      orderId: route.query.orderId,
      amount: route.query.amount, // URL에서 전달된 amount 값 사용
      userToken,
      orderInfoId
    };

    console.log("Request Form:", requestForm);  // 여기서 데이터를 제대로 받고 있는지 로그로 확인

    const { success, data, message } = await paymentStore.requestProcessPayments(requestForm);

    if (success) {
      // 응답 받은 데이터(jsonData)에 URL 파라미터로 받은 값을 추가.
      confirmed.value = true;
      jsonData.value = { ...data, amount: route.query.amount }; // amount를 포함하여 jsonData에 추가

      localStorage.removeItem("oid");
    } else {
      console.error("Payment confirmation failed:", message);  // 오류 발생 시
      router.push(`/payment/fail?message=${message}`);
    }
  } catch (error) {
    console.error("Error confirming payment:", error);
    router.push("/payment/fail");
  } finally {
    isProcessing.value = false;  // 로딩 종료
  }
}

function redirectToDocs() {
  window.location.href = "https://docs.tosspayments.com/guides/payment/integration";
}

function redirectToSupport() {
  window.location.href = "https://discord.gg/A4fRFXQhRu";
}

// 홈으로 돌아가는 함수
function redirectToHome() {
  router.push('/'); // 홈 페이지로 리디렉션
}

onMounted(() => {
  confirmPayment();
});
</script>
