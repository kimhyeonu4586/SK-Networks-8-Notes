import { Board } from "./boardType";

export const boardState = () => ({
    boardList: [] as Board[],
    board: null as Board | null,

    currentPage: 1,
    totalPages: 0,
    totalItems: 0,
})