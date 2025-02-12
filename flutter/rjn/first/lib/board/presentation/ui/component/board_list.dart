import 'package:first/board/board_module.dart';
import 'package:first/board/presentation/providers/board_list_provider.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'card_item.dart';

class BoardList extends StatelessWidget {
  final List<dynamic> boardList;

  BoardList({
    required this.boardList
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: List.generate(boardList.length, (index) {
        final board = boardList[index];
        if (board == null) {
          return SizedBox(height: 20);
        }

        return CardItem(
          title: board.title,
          content: board.content,
          nickname: board.nickname,
          createDate: board.createDate,
          onTap: () async {
            final result = await Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => BoardModule.provideBoardReadPage(board.id)
              ),
            );

            if (result != null) {
              final boardListProvider = Provider.of<BoardListProvider>(context, listen: false);
            }
          }
        );
      })
    );
  }
}