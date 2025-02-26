import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:geolocator/geolocator.dart';

class PathFinderSearchMapPage extends StatefulWidget {
  @override
  _PathFinderSearchMapPageState createState() => _PathFinderSearchMapPageState();
}

class _PathFinderSearchMapPageState extends State<PathFinderSearchMapPage> {
  late final WebViewController _controller;
  double? latitude;
  double? longitude;
  bool isGpsLoaded = false;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted);

    // GPS 데이터가 준비된 후 WebView 로드
    getGPSData();
  }

  /// GPS 데이터를 가져온 후 WebView를 로드
  Future<void> getGPSData() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      print("GPS 서비스가 비활성화됨");
      return;
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.deniedForever) {
        print("위치 권한이 영구적으로 거부됨");
        return;
      }
    }

    Position position = await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high,
    );

    print("위도: ${position.latitude}, 경도: ${position.longitude}");

    setState(() {
      latitude = position.latitude;
      longitude = position.longitude;
      isGpsLoaded = true;
    });

    // GPS 데이터 반영 후 WebView에 HTML 로드
    _controller.loadHtmlString(_getHtmlContent());
  }

  /// HTML 콘텐츠 생성
  String _getHtmlContent() {
    String kakaoJavaScriptAppKey = dotenv.env['KAKAO_JAVASCRIPT_APP_KEY'] ?? '';
    double lat = latitude ?? 37.4979; // GPS가 없을 때 기본값
    double lng = longitude ?? 127.0276;

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
          center: new kakao.maps.LatLng($lat, $lng),
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
      body: isGpsLoaded
          ? WebViewWidget(controller: _controller)
          : Center(child: CircularProgressIndicator()), // GPS 데이터가 로딩될 때 로딩 UI 표시
    );
  }
}