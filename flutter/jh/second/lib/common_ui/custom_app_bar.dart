import 'package:second/board/board_module.dart';
import 'package:second/path_finder/path_finder_module.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import '../blog_post/blog_post_module.dart';
import '../kakao_authentication/kakao_auth_module.dart';
import '../simple_chat/simple_chat_module.dart';
import 'app_bar_action.dart';

class CustomAppBar extends StatelessWidget {
  final String apiUrl = dotenv.env['API_URL'] ?? '';
  final String apiKey = dotenv.env['API_KEY'] ?? '';

  final Widget body;
  final String title;

  CustomAppBar({
    required this.body,
    this.title = 'Home'
  });

  @override
  Widget build(BuildContext context) {
    print("CustomAppBar apiUrl: ${apiUrl}");
    print("CustomAppBar apiKey: ${apiKey}");

    return Column(
      children: [
        AppBar(
          title: Text(title),
          backgroundColor: Colors.lightBlue,
          actions: [
            AppBarAction(
              icon: Icons.article,
              tooltip: 'Blog Posts',
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => BlogPostModule.provideBlogPostListPage(),
                  ),
                );
              },
            ),
            AppBarAction(
                icon: Icons.list_alt,
                tooltip: '게시물 리스트',
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => BoardModule.provideBoardListPage(),
                    ),
                  );
                }
            ),
            AppBarAction(
              icon: Icons.login,
              tooltip: 'Login',
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => KakaoAuthModule.provideKakaoLoginPage()
                  ),
                );
              },
            ),
            AppBarAction(
              icon: Icons.chat_bubble,
              tooltip: 'Simple Chat',
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => SimpleChatModule.provideSimpleChatPage(apiUrl, apiKey)
                  ),
                );
              },
            ),
            AppBarAction(
              icon: Icons.map,
              tooltip: 'Map',
              onPressed: () {
                // 지도 페이지로 이동하는 코드 작성
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => PathFinderModule.providePathFinderSearchMapPage(),  // 지도 페이지로 이동
                  ),
                );
              },
            ),
          ],
        ),
        Expanded(child: body)
      ],
    );
  }
}