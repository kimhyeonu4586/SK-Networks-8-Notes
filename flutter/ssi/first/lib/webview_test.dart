import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(MaterialApp(home: WebViewTestPage()));
}

class WebViewTestPage extends StatefulWidget {
  @override
  _WebViewTestPageState createState() => _WebViewTestPageState();
}

class _WebViewTestPageState extends State<WebViewTestPage> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted) // JavaScript 실행 허용
      ..loadRequest(Uri.parse('https://apis.map.kakao.com/web/sample/basicMap/')); // Kakao API 테스트
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Kakao API Test')),
      body: WebViewWidget(controller: _controller),
    );
  }
}
