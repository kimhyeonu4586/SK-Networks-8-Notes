import 'package:flutter/cupertino.dart';
import '../../domain/usecases/search_map/search_map_use_case.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class PathFinderSearchMapProvider with ChangeNotifier {
  final SearchMapUseCase searchMapUseCase;

  PathFinderSearchMapProvider({required this.searchMapUseCase});

  String _searchQuery = '';
  String get searchQuery => _searchQuery;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String _result = '';
  String get result => _result;

  void updateSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  Future<void> searchLocation() async {
    if (_searchQuery.isEmpty) return;

    _isLoading = true;
    _result = '';
    notifyListeners();

    try {
      final searchResult = await searchMapUseCase.execute(_searchQuery);
      _result = searchResult;  // 결과 업데이트
    } catch (e) {
      _result = '검색 실패: ${e.toString()}';
    }

    _isLoading = false;
    notifyListeners();
  }

  // 카카오맵 로드하는 메서드
  void loadMap() {
    final kakaoAppKey = dotenv.env['KAKAO_JAVASCRIPT_APP_KEY'];

    // 카카오 맵 HTML 코드
    _result = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>카카오 맵</title>
      <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=$kakaoAppKey&libraries=services"></script>
      <style>
        #map { width: 100%; height: 100%; }
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script>
        var mapContainer = document.getElementById('map'), 
            mapOption = { 
              center: new kakao.maps.LatLng(37.4979, 127.0276), // 기본 위치 강남역
              level: 3 
            };
        var map = new kakao.maps.Map(mapContainer, mapOption); 
      </script>
    </body>
    </html>
    """;
    notifyListeners();
  }
}