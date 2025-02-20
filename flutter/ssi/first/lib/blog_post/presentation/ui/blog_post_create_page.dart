import 'dart:convert';
import 'dart:io' as io show Directory, File;

import 'package:first/blog_post/blog_post_module.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_quill/flutter_quill.dart';
import 'package:flutter_quill_extensions/flutter_quill_extensions.dart';
import 'package:provider/provider.dart';
import 'package:path/path.dart' as path;
import 'package:uuid/uuid.dart';

import '../providers/blog_post_create_provider.dart';

class BlogPostCreatePage extends StatefulWidget {
  @override
  _BlogPostCreatePageState createState() => _BlogPostCreatePageState();
}

class _BlogPostCreatePageState extends State<BlogPostCreatePage> {
  final TextEditingController titleController = TextEditingController();
  final FocusNode _editorFocusNode = FocusNode();
  final ScrollController _editorScrollController = ScrollController();

  final QuillController _quillController = QuillController.basic(
    config: QuillControllerConfig(
      clipboardConfig: QuillClipboardConfig(
        enableExternalRichPaste: true,
        onImagePaste: (imageBytes) async {
          if (kIsWeb) {
            return null;
          }
          final newFileName = 'image-${DateTime.now().toIso8601String()}.png';
          final newPath = path.join(io.Directory.systemTemp.path, newFileName);
          final file = await io.File(newPath).writeAsBytes(imageBytes, flush: true);
          return file.path;
        },
      ),
    ),
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('블로그 포스트 작성'),
        actions: [
          IconButton(
            icon: Icon(Icons.output),
            tooltip: 'Delta JSON 출력',
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('JSON Delta가 콘솔에 출력되었습니다.')),
              );
              debugPrint(jsonEncode(_quillController.document.toDelta().toJson()));
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Consumer<BlogPostCreateProvider>(
          builder: (context, provider, child) {
            return Column(
              children: [
                TextField(
                  controller: titleController,
                  decoration: InputDecoration(labelText: '제목'),
                ),
                SizedBox(height: 10),

                QuillSimpleToolbar(
                  controller: _quillController,
                  config: QuillSimpleToolbarConfig(
                    embedButtons: FlutterQuillEmbeds.toolbarButtons(),
                    showClipboardPaste: true,
                  ),
                ),

                SizedBox(height: 10),

                Expanded(
                  child: QuillEditor(
                    controller: _quillController,
                    focusNode: _editorFocusNode,
                    scrollController: _editorScrollController,
                    config: QuillEditorConfig(
                      placeholder: '내용을 입력하세요...',
                      padding: EdgeInsets.all(8),
                      embedBuilders: [
                        ...FlutterQuillEmbeds.editorBuilders(),
                      ],
                    ),
                  ),
                ),

                SizedBox(height: 20),

                if (provider.isLoading) CircularProgressIndicator(),
                if (provider.message.isNotEmpty)
                  Text(
                    provider.message,
                    style: TextStyle(color: Colors.red),
                  ),

                ElevatedButton(
                  onPressed: () async {
                    final title = titleController.text.trim();
                    final contentJson = _quillController.document.toDelta().toJson();

                    if (title.isEmpty || contentJson.isEmpty) {
                      provider.message = '제목 및 내용을 모두 입력하세요';
                      provider.notifyListeners();
                      return;
                    }

                    // Delta -> HTML 변환 후 S3 업로드
                    String compressedHtml = provider.convertDeltaToHtml(contentJson);
                    final blogPost = await provider.createBlogPost(title, compressedHtml);

                    if (blogPost != null) {
                      print("게시물 등록 완료");

                      Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(
                            builder: (context) => BlogPostModule.provideBlogPostReadPage(blogPost.id),
                          )
                      );
                    }
                  },
                  child: Text('등록'),
                )
              ],
            );
          },
        ),
      ),
    );
  }

  @override
  void dispose() {
    _quillController.dispose();
    _editorScrollController.dispose();
    _editorFocusNode.dispose();
    super.dispose();
  }
}