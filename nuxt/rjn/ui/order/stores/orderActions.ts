import * as axiosUtility from "../../utility/axiosInstance"

export const orderAction = {
  async requestCreateOrder(orderData) {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

    const { items, total, userToken } = orderData
    console.log(`requestCreateOrder(): ${items}, ${total}, ${userToken}`)

    try {
      // 주문 생성 요청
      console.log(`requestCreateOrder(): ${JSON.stringify(orderData)}`)
      const response = await djangoAxiosInstance.post("/orders/create", { items, total, userToken });

      // 요청 성공 여부 확인
      if (response.data.success) {
        console.log(`requestCreateOrder(): ${response}`)
        this.setOrderInfoId(response.data.orderId);
        return {
          success: true,
          orderId: response.data.orderId, // 서버에서 반환한 주문 ID
        };
      } else {
        return {
          success: false,
          error: response.data.message || "주문 생성에 실패했습니다.",
        };
      }
    } catch (error) {
      console.error("Error in requestCreateOrder:", error);
      return {
        success: false,
        error: "서버와 통신 중 오류가 발생했습니다.",
      };
    }
  },
  setOrderInfoId(orderId: string) {
    this.orderInfoId = orderId
  },

  // 주문 ID 클리어
  clearOrderInfoId() {
    this.orderInfoId = null
  },

  getOrderInfoId() {
    return this.orderInfoId;
  },
}