import * as axiosUtility from "../../utility/axiosInstance"
import { Cart } from "./cartType"

export const cartAction = {
    async requestCartList({ page = 1, perPage = 10, userToken }: { page: number, perPage: number, userToken: string }): Promise<any> {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
    
        console.log(`Fetching cart list with page: ${page}, perPage: ${perPage}, userToken: ${userToken}`);
    
        try {
            const res = await djangoAxiosInstance.post('/cart/list', {
                userToken,     // userToken을 본문에 포함
                page,          // 페이지 번호
                perPage        // 페이지 크기
            });
    
            console.log('Response Data:', res.data);
    
            // 응답 데이터를 사용하여 카트 목록 및 페이지 정보 업데이트
            this.cartList = res.data.cartList;
            this.totalPages = res.data.totalItems;
            this.currentPage = page;
    
            return res.data; // 반드시 데이터를 반환하도록 수정
        } catch (error) {
            console.log('requestCartList() 중 에러:', error);
            throw error; // 오류가 발생하면 throw로 다시 던지기
        }
    },    
    async requestCartSave(requestForm: { id: number, userToken: string, quantity: number }) {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances()

        const cart = {
            id: requestForm.id,
            quantity: requestForm.quantity,
        };

        try {
            const response = await djangoAxiosInstance.post("/cart/create", {
                cart: cart, userToken: requestForm.userToken
            });
            console.log("서버에 장바구니 저장 성공:", response.data.success);
            return response.data.success
        } catch (error) {
            console.error("서버에 장바구니 저장 실패:", error);
            this.cartList = this.cartList.filter(
                (item) => item.cartId !== cart.id
            );

            throw error;
        }
    },
    async requestRemoveCart(cartId) {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances()

        const userToken = localStorage.getItem('userToken');
        if (!userToken) {
          return { success: false, error: "로그인 상태가 아닙니다." };
        }
      
        try {
          const response = await djangoAxiosInstance.post('/cart/remove', {
            userToken,
            id: cartId,
          });
      
          if (response.data.success) {
            // 성공적으로 삭제된 경우
            return { success: true };
          } else {
            // 실패한 경우
            return { success: false, error: response.data.error || "카트 삭제 실패" };
          }
        } catch (error) {
          console.error("Error removing cart item:", error);
          return { success: false, error: "카트 삭제 중 오류가 발생했습니다." };
        }
      }
}