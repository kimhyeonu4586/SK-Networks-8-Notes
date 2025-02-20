
import 'package:second/blog_post/domain/usecases/read/read_blog_post_usecase.dart';

import '../../../infrastructures/repository/blog_post_repository.dart';
import '../../entity/blog_post.dart';

class ReadBlogPostUseCaseImpl implements ReadBlogPostUseCase {
  final BlogPostRepository blogPostRepository;

  ReadBlogPostUseCaseImpl(
    this.blogPostRepository
  );

  @override
  Future<BlogPost?> execute(int blogPostId) async {
    try {
      print("blogPostId: ${blogPostId}");
      final board = await blogPostRepository.readBlogPost(blogPostId);
      return board;
    } catch (e) {
      return null;
    }
  }
}