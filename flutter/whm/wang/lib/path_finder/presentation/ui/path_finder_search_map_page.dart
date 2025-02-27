import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PathFinderSearchMapPage extends StatefulWidget {
  @override
  _PathFinderSearchMapPageState createState() =>
      _PathFinderSearchMapPageState();
}

class _PathFinderSearchMapPageState extends State<PathFinderSearchMapPage> {
  late final WebViewController _controller;
  double? latitude;
  double? longitude;
  bool isGpsLoaded = false;
  TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()..setJavaScriptMode(JavaScriptMode.unrestricted);
    getGPSData();
  }

  /// GPS 데이터를 가져온 후 WebView를 로드
  Future<void> getGPSData() async {
    // GPS 데이터 처리 로직
    // 기본값으로 서울 위치를 설정합니다.
    setState(() {
      latitude = 37.4979;
      longitude = 127.0276;
      isGpsLoaded = true;
    });

    _controller.loadHtmlString(await _getHtmlContent());
  }

  /// HTML 콘텐츠 생성
  Future<String> _getHtmlContent() async {
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
    var mapContainer = document.getElementById('map');
    var mapOption = {
        center: new kakao.maps.LatLng($lat, $lng),
        level: 3
    };
    var map = new kakao.maps.Map(mapContainer, mapOption);
    var geocoder = new kakao.maps.services.Geocoder();

    // 현재 위치에 마커 추가
    var markerPosition = new kakao.maps.LatLng($lat, $lng);
    var marker = new kakao.maps.Marker({
        position: markerPosition
    });

    marker.setMap(map);

    // 마커 클릭 시 정보 창 표시
    var infowindow = new kakao.maps.InfoWindow({
        content: '<div style="padding:5px;">현재 위치</div>'
    });

    kakao.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
    });
  </script>
</body>
</html>
    ''';
  }

  /// 실제 주소 검색 API 호출
  Future<void> searchAddress() async {
    String address = searchController.text.trim();
    if (address.isEmpty) {
      print("❌ 입력된 주소가 없습니다.");
      return;
    }

    // 주소 검색
    var location = await locationSearch(address);
    if (location != null) {
      double? lat = location['latitude'];
      double? lng = location['longitude'];

      // HTML 콘텐츠에 위치 업데이트
      String updatedHtmlContent = await _getHtmlContentWithNewLocation(lat!, lng!);
      _controller.loadHtmlString(updatedHtmlContent);
    } else {
      print("주소 검색 실패");
    }
  }

  Future<String> _getHtmlContentWithNewLocation(double lat, double lng) async {
    String kakaoJavaScriptAppKey = dotenv.env['KAKAO_JAVASCRIPT_APP_KEY'] ?? '';
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
    var mapContainer = document.getElementById('map');
    var mapOption = {
        center: new kakao.maps.LatLng($lat, $lng),
        level: 3
    };
    var map = new kakao.maps.Map(mapContainer, mapOption);
    var geocoder = new kakao.maps.services.Geocoder();

    var markerPosition = new kakao.maps.LatLng($lat, $lng);
    var marker = new kakao.maps.Marker({
        position: markerPosition
    });

    marker.setMap(map);

    var infowindow = new kakao.maps.InfoWindow({
        content: '<div style="padding:5px;">주소 위치</div>'
    });

    kakao.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
    });
  </script>
</body>
</html>
    ''';
  }

  /// 주소 검색 요청을 위한 API 호출
  Future<Map<String, double>?> locationSearch(String address) async {
    String restAPIKey = dotenv.env['KAKAO_REST_API_KEY'] ?? 'default_api_key';  // 여기에 실제 카카오 REST API 키 입력
    print('restAPIKey: ${restAPIKey}');
    try {
      final response = await http.get(
        Uri.parse(
            'http://dapi.kakao.com/v2/local/search/address.json?query=$address'),
        headers: {'Authorization': 'KakaoAK $restAPIKey'},
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['documents'].isNotEmpty) {
          final firstResult = data['documents'][0];

          // String에서 double로 변환
          final lat = double.tryParse(firstResult['y'].toString()) ?? 0.0;  // Convert to double
          final lng = double.tryParse(firstResult['x'].toString()) ?? 0.0;  // Convert to double

          return {'latitude': lat, 'longitude': lng};
        }
      }
    } catch (e) {
      print('주소 검색 실패: $e');
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('카카오 맵')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: searchController,
                    decoration: InputDecoration(
                      hintText: '주소를 입력하세요',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => searchAddress(),
                  ),
                ),
                SizedBox(width: 8),
                ElevatedButton(
                  onPressed: searchAddress,
                  child: Text('검색'),
                ),
              ],
            ),
          ),
          Expanded(
            child: isGpsLoaded
                ? WebViewWidget(controller: _controller)
                : Center(child: CircularProgressIndicator()),
          ),
        ],
      ),
    );
  }
}