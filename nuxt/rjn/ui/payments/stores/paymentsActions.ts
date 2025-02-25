import * as axiosUtility from "../../utility/axiosInstance"

export const paymentsAction = {
  async requestProcessPayments(requestForm) {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

    this.isProcessing = true;
    this.errorMessage = null; // 오류 메시지 초기화

    try {
      // 유저 토큰 확인
      const userToken = requestForm.userToken;
      if (!userToken) {
        throw new Error("User token is required to process the payment.");
      }

      const orderInfoId = requestForm.orderInfoId;
      if (!orderInfoId) {
        throw new Error("Order Info ID is required to process the payment.");
      }

      // 결제 요청
      const response = await djangoAxiosInstance.post("/payments/process", {
        paymentKey: requestForm.paymentKey,
        orderId: requestForm.orderId,
        amount: requestForm.amount,
        userToken, // 유저 토큰 전달
        orderInfoId, // 추가된 주문 정보 ID 전달
      });

      // 요청 성공 여부 확인
      if (response.data.success) {
        console.log("결제 성공:", response.data);
        this.paymentSuccess = true;
        this.paymentsId = response.data.paymentsId;
        return { success: true, data: response.data }; // 성공 데이터 반환
      } else {
        console.error("결제 실패:", response.data.message);
        this.errorMessage = response.data.message;
        return { success: false, message: response.data.message };
      }
    } catch (error) {
      console.error("결제 처리 중 오류 발생:", error);
      this.errorMessage = "서버 오류로 인해 결제 처리에 실패했습니다.";
      return { success: false, message: "서버 오류로 인해 결제 처리에 실패했습니다." };
    } finally {
      // 결제 요청 완료 후 isProcessing을 false로 설정
      this.isProcessing = false;
    }
  },
}