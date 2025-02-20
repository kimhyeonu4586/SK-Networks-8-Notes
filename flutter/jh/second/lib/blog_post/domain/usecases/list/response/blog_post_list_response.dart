import 'package:second/board/domain/entity/board.dart';

import '../../../entity/blog_post.dart';

class BlogPostListResponse {
  final List<BlogPost> blogPostList;
  final int totalItems;
  final int totalPages;

  BlogPostListResponse({
    required this.blogPostList,
    required this.totalItems,
    required this.totalPages
  });
}