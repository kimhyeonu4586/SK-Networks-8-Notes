import 'package:flutter/cupertino.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../domain/entity/board.dart';
import '../../domain/usecases/read/read_board_usecase.dart';

class BoardReadProvider with ChangeNotifier {
  final ReadBoardUseCase readBoardUseCase;
  final FlutterSecureStorage secureStorage = FlutterSecureStorage();
  final int boardId;

  Board? _board;
  String? _error;
  bool _isLoading = false;

  int totalItems = 0;
  int totalPages = 0;
  int currentPage = 1;

  BoardReadProvider({
    required this.readBoardUseCase,
    required this.boardId,
  });

  Board? get board => _board;
  String? get error => _error;
  bool get isLoading => _isLoading;

  Future<void> fetchBoard() async {
    if (_isLoading) return;

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _board = await readBoardUseCase.execute(boardId);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}