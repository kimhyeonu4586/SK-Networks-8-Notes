

import 'package:first/board/domain/usecases/read/read_board_usecase.dart';

import '../../../infrasturctures/repository/board_repository.dart';
import '../../entity/board.dart';

class ReadBoardUseCaseImpl implements ReadBoardUseCase {
  final BoardRepository boardRepository;

  ReadBoardUseCaseImpl(
      this.boardRepository
      );

  @override
  Future<Board?> execute(int boardId) async {
    try {
      final board = await boardRepository.readBoard(boardId);
      return board;
    } catch (e) {
      return null;
    }
  }
}