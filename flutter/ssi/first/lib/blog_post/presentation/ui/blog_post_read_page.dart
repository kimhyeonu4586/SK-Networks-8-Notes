import 'package:flutter/material.dart';
import 'package:html/parser.dart';
import 'package:provider/provider.dart';

import '../../blog_post_module.dart';
import '../../domain/entity/blog_post.dart';
import '../providers/blog_post_read_provider.dart';


class BlogPostReadPage extends StatefulWidget {
  @override
  _BlogPostReadPageState createState() => _BlogPostReadPageState();
}

class _BlogPostReadPageState extends State<BlogPostReadPage> {
  @override
  void initState() {
    super.initState();
    // 게시글 데이터를 가져옵니다.
    final blogPostReadProvider = Provider.of<BlogPostReadProvider>(context, listen: false);

    if (blogPostReadProvider.blogPost == null) {
      blogPostReadProvider.fetchBlogPost();
    }
  }

  Future<bool> _onWillPop() async {
    // 뒤로가기 버튼 이벤트 처리
    final blogPostReadProvider =
    Provider.of<BlogPostReadProvider>(context, listen: false);
    final updatedBlogPost = blogPostReadProvider.blogPost;

    // 현재 수정된 게시글 데이터를 반환하며 뒤로가기
    Navigator.pop(context, updatedBlogPost);
    return Future.value(false); // 기본 뒤로가기 동작 방지
  }

  @override
  Widget build(BuildContext context) {
    final blogPostReadProvider = Provider.of<BlogPostReadProvider>(context);

    return WillPopScope(
      onWillPop: _onWillPop, // 뒤로가기 이벤트 처리
      child: Scaffold(
        appBar: AppBar(
          title: Text('게시글 상세보기'),
          actions: [
            IconButton(
              icon: Icon(Icons.edit),
              onPressed: () {
                final selectedBlogPost = blogPostReadProvider.blogPost;
                if (selectedBlogPost != null) {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => BlogPostModule.provideBlogPostModifyPage(
                        selectedBlogPost.id,
                        selectedBlogPost.title,
                        selectedBlogPost.content,
                      ),
                    ),
                  ).then((updatedData) {
                    if (updatedData != null &&
                        updatedData is Map<String, dynamic>) {
                      final updatedTitle =
                          updatedData['title'] ?? selectedBlogPost.title;
                      final updatedContent =
                          updatedData['content'] ?? selectedBlogPost.content;

                      // 생성된 Board 객체
                      final updatedBlogPost = BlogPost(
                        id: selectedBlogPost.id,
                        title: updatedTitle,
                        content: updatedContent,
                        nickname: selectedBlogPost.nickname,
                        createDate: selectedBlogPost.createDate,
                      );

                      // 상세 페이지 갱신
                      blogPostReadProvider.updateBlogPost(updatedBlogPost);
                    }
                  });
                }
              },
            ),
            IconButton(
              icon: Icon(Icons.delete),
              onPressed: () => _showDeleteDialog(context, blogPostReadProvider),
            ),
          ],
        ),
        body: _buildBody(blogPostReadProvider),
      ),
    );
  }

  Widget _buildBody(BlogPostReadProvider blogPostReadProvider) {
    if (blogPostReadProvider.isLoading) {
      return Center(child: CircularProgressIndicator());
    } else if (blogPostReadProvider.error != null) {
      return Center(
        child: Text(
          '블로그 포스트를 불러오는 데 실패했습니다.\n${blogPostReadProvider.error}',
          textAlign: TextAlign.center,
          style: TextStyle(color: Colors.red),
        ),
      );
    } else if (blogPostReadProvider.blogPost == null) {
      return Center(child: Text('블로그 포스트를 찾을 수 없습니다.'));
    }

    final blogPost = blogPostReadProvider.blogPost!;
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            blogPost.title,
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 8),
          Text(
            '작성자: ${blogPost.nickname.isEmpty ? "익명" : blogPost.nickname}',
            style: TextStyle(fontSize: 14, color: Colors.grey),
          ),
          SizedBox(height: 8),
          Text(
            '작성일: ${blogPost.createDate}',
            style: TextStyle(fontSize: 14, color: Colors.grey),
          ),
          SizedBox(height: 16),
          Divider(),
          Expanded(
            child: SingleChildScrollView(
              child: _buildHtmlContent(blogPost.content),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHtmlContent(String content) {
    final document = parse(content);  // HTML 파싱
    final elements = document.body!.children;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: elements.map((element) {
        if (element.localName == 'p') {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: Text(element.text),
          );
        } else if (element.localName == 'img') {
          return Image.network(element.attributes['src']!);
        } else {
          return SizedBox();  // 기타 HTML 태그는 기본적으로 처리 안 함
        }
      }).toList(),
    );
  }

  void _showDeleteDialog(
      BuildContext context, BlogPostReadProvider blogPostReadProvider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('블로그 포스트 삭제'),
        content: Text('정말 이 블로그 포스트를 삭제하시겠습니까?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('취소'),
          ),
          TextButton(
            onPressed: () async {
              // await blogPostReadProvider.deleteBoard();
              // Navigator.of(context).pop();
              // Navigator.of(context).pop({'deleted': true});
            },
            child: Text('삭제'),
          ),
        ],
      ),
    );
  }
}