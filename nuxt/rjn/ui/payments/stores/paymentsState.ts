export const paymentsState = () => ({
  isProcessing: false, // 결제 진행 중인지 여부
  paymentSuccess: false, // 결제 성공 여부
  paymentsId: null, // 결제 ID
  errorMessage: null, // 결제 실패 시 오류 메시지
});
