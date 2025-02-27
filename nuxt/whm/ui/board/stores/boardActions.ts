import * as axiosUtility from "../../utility/axiosInstance";

export const boardAction = {
  async requestBoardList(payload) {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

    const { page, perPage } = payload;

    try {
      const res = await djangoAxiosInstance.get(
        `/board/list?page=${page}&perPage=${perPage}`
      );

      console.log("Response Data:", res.data);

      // 서버 응답 데이터 구조 확인 후 필요한 값만 추출
      const { dataList, totalItems, totalPages } = res.data;
      console.log(
        `boardList: ${dataList}, totalItems: ${totalItems}, totalPages: ${totalPages}`
      );

      // 데이터 설정
      this.boardList = dataList || []; // boardList가 없으면 빈 배열
      this.totalPages = totalPages || 0; // totalPages가 없으면 0
      this.totalItems = totalItems || 0; // totalItems가 없으면 0
      this.currentPage = page; // 현재 페이지는 요청한 page로 설정
    } catch (error) {
      console.error("requestBoardList() 중 에러:", error);

      // 에러가 발생하면 상태를 초기화
      this.boardList = [];
      this.totalPages = 0;
      this.totalItems = 0;
      this.currentPage = 1; // 실패 시 페이지는 1로 초기화
    }
  },
  async requestCreateBoard(payload) {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

    const { title, content, userToken } = payload;

    try {
      const res = await djangoAxiosInstance.post(`/board/create`, {
        title,
        content,
        userToken,
      });

      console.log("Create Board Response Data:", res.data);

      if (res.data) {
        console.log("Board created successfully.");
        // 필요한 추가 동작 (예: 새로고침, 알림)
      } else {
        console.error(
          "Failed to create board:",
          res.data.message || "Unknown error"
        );
      }
    } catch (error) {
      console.error("requestCreateBoard() 중 에러:", error);
    }
  },
  async requestReadBoard(boardId) {
    try {
      const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
      const res = await djangoAxiosInstance.get(`/board/read/${boardId}`);
      console.log(`res: ${JSON.stringify(res)}`);
      this.board = res.data;
    } catch (error) {
      console.error("게시글 정보를 가져오는 데 실패했습니다:", error);
      this.board = null;
    }
  },
  async requestModifyBoard(boardId, boardDetails) {
    try {
      const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
      const response = await djangoAxiosInstance.put(
        `/board/modify/${boardId}`,
        {
          title: boardDetails.title,
          content: boardDetails.content,
          userToken: boardDetails.userToken, // userToken 포함
        }
      );

      console.log("게시글 수정 성공:", response.data);
      this.board = response.data; // 수정된 게시글을 스토어에 반영
    } catch (error) {
      console.error("게시글 수정 요청 중 에러 발생:", error);
      throw error; // 에러를 다시 던져서 상위 컴포넌트에서 처리하도록 함
    }
  },
  async requestDeleteBoard(boardId, userToken) {
    try {
      const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
      const response = await djangoAxiosInstance.delete(
        `/board/delete/${boardId}`,
        {
          data: { userToken },
        }
      );
      console.log("게시글 삭제 성공:", response.data);
    } catch (error) {
      console.error("게시글 삭제 요청 중 에러 발생:", error);
      throw error; // 에러를 다시 던져서 상위 컴포넌트에서 처리하도록 함
    }
  },
};
