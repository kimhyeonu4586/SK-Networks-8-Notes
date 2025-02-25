import * as axiosUtility from "../../utility/axiosInstance";
import { AxiosResponse } from "axios"
import { useAccountStore } from "./accountStore"

export const accountAction = {

	async requestEmail(userToken: string): Promise<any> {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
        try {
          // userToken을 body로 보내기
          const res: AxiosResponse = await djangoAxiosInstance.post(
            "/account/email",
            { userToken } // userToken을 요청 바디로 전달
          );
          
          // 응답에서 이메일 추출
          return res.data.email;
        } catch (error) {
          console.error("requestEmail() axios 오류!", error);
          throw new Error("Failed to fetch email");
        }
      },
};