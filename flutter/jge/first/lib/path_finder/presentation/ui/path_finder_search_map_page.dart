import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:webview_flutter/webview_flutter.dart';

class PathFinderSearchMapPage extends StatefulWidget {
  @override
  _PathFinderSearchMapPageState createState() => _PathFinderSearchMapPageState();
}

class _PathFinderSearchMapPageState extends State<PathFinderSearchMapPage> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();

    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadHtmlString(_getHtmlContent());
  }

  String _getHtmlContent() {
    String kakaoJavaScriptAppKey = dotenv.env['KAKAO_JAVASCRIPT_APP_KEY'] ?? '';
    print('kakaoJavaScriptAppKey: ${kakaoJavaScriptAppKey}');

    return '''
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>카카오 맵</title>
  <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=$kakaoJavaScriptAppKey&libraries=services"></script>
  <style>
    html, body { margin: 0; padding: 0; height: 100%; }
    #map { width: 100%; height: 100%; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script>
    window.onload = function() {
      var mapContainer = document.getElementById('map');
      var mapOption = {
          center: new kakao.maps.LatLng(37.4979, 127.0276),
          level: 3
      };
      var map = new kakao.maps.Map(mapContainer, mapOption);
    };
  </script>
</body>
</html>
    ''';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('카카오 맵')),
      body: WebViewWidget(controller: _controller),
    );
  }
}
