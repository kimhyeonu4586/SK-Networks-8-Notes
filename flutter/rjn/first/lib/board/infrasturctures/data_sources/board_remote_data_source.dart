import 'dart:convert';

import 'package:first/board/domain/entity/board.dart';
import 'package:first/board/domain/usecases/list/response/board_list_response.dart';
import 'package:http/http.dart' as http;

class BoardRemoteDataSource {
  final String baseUrl;

  BoardRemoteDataSource(this.baseUrl);
  
  Future<BoardListResponse> listBoard(int page, int perPage) async {
    final parsedUri =
      Uri.parse('$baseUrl/board/list?page=$page&perPage=$perPage');

    final boardListResponse = await http.get(parsedUri);

    if (boardListResponse.statusCode == 200) {
      final data = json.decode(boardListResponse.body);

      List<Board> boardList = (data['dataList'] as List)
        .map((data) => Board(
          id: data['boardId'] ?? 0,
          title: data['title'] ?? 'Untitled',
          content: '',
          nickname: data['nickname'] ?? '익명',
          createDate: data['createDate'] ?? 'Unknown'
        )
      )
      .toList();

      int totalItems = parseInt(data['totalItems']);
      int totalPages = parseInt(data['totalPages']);
      
      return BoardListResponse(
        boardList: boardList, 
        totalItems: totalItems, 
        totalPages: totalPages
      );
    } else {
      throw Exception('게시물 리스트 조회 실패');
    }
  }

  Future<Board> create(String title, String content, String userToken) async {
    final url = Uri.parse('$baseUrl/board/create');
    final response = await http.post(
      url,
      body: {
        'title': title,
        'content': content,
        'userToken': userToken,
      }
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);

      return Board(
        id: data['data']['boardId'] ?? 0,
        title: data['data']['title'] ?? 'Untitled',
        content: data['data']['content'] ?? '',
        nickname: data['data']['writerNickname'] ?? 'Anonymouse',
        createDate: data['data']['createDate'] ?? 'Unknown',
      );
    } else {
      throw Exception("게시물 생성 실패");
    }
  }

  Future<Board?> fetchBoard(int boardId) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/board/read/$boardId'));
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return Board.fromJson(data);
      }
    } catch (e) {
      return null;
    }
  }

  int parseInt(dynamic value) {
    if (value is String) {
      return int.tryParse(value) ?? 0;
    }

    return value ?? 0;
  }
}