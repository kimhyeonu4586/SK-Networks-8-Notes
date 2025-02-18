import 'package:flutter/material.dart';

import '../../domain/entity/blog_post.dart';
import '../../domain/usecases/update/update_blog_post_usecase.dart';

class BlogPostModifyProvider extends ChangeNotifier {
  final UpdateBlogPostUseCase updateBlogPostUseCase;
  final int boardId;

  bool isLoading = false;
  String? errorMessage;

  BlogPostModifyProvider({
    required this.updateBlogPostUseCase,
    required this.boardId,
  });

  Future<BlogPost?> updateBlogPost(
      String title, String content, String userToken) async {
    try {
      isLoading = true;
      notifyListeners();

      print('BlogPostModifyProvider Updating board with ID: $boardId');
      print(
          'BlogPostModifyProvider New Title: $title, New Content: $content, UserToken: $userToken');

      final updatedBlogPost =
          await updateBlogPostUseCase.execute(boardId, title, content, userToken);

      print(
          'BoardModifyProvider Board updated successfully: ${updatedBlogPost?.toJson()}');

      errorMessage = null;
      isLoading = false;
      notifyListeners();

      return updatedBlogPost;
    } catch (e) {
      isLoading = false;
      errorMessage = 'Failed to update board: $e';
      notifyListeners();
      print('Error during update: $errorMessage');

      throw Exception(errorMessage);
    }
  }

  void clearError() {
    errorMessage = null;
    notifyListeners();
  }
}
