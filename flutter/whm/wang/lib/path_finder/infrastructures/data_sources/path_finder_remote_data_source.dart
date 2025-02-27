import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class PathFinderRemoteDataSource {
  final String baseUrl = 'https://dapi.kakao.com/v2/local/search/keyword.json';

  PathFinderRemoteDataSource();

  Future<String> fetchSearchResults(String searchQuery) async {
    // dotenv를 사용하여 환경 변수에서 카카오 API 키를 가져옵니다.
    final apiKey = dotenv.env['KAKAO_JAVASCRIPT_APP_KEY'] ?? '';

    if (apiKey.isEmpty) {
      throw Exception('Kakao API Key is missing');
    }

    final response = await http.get(
      Uri.parse('$baseUrl?query=$searchQuery'),
      headers: {
        'Authorization': 'KakaoAK $apiKey',  // 'KakaoAK' 뒤에 API 키를 넣어줍니다.
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return _generateHtmlContent(data);
    } else {
      throw Exception('지도 검색 실패: ${response.statusCode}');
    }
  }

  String _generateHtmlContent(Map<String, dynamic> data) {
    final places = data['documents'] as List;
    String htmlContent = '<html><body>';

    for (var place in places) {
      final placeName = place['place_name'] ?? '알 수 없음';
      final latitude = place['y'] ?? '0.0';
      final longitude = place['x'] ?? '0.0';
      htmlContent += '''
        <div>
          <h3>$placeName</h3>
          <p>위도: $latitude, 경도: $longitude</p>
        </div>
      ''';
    }

    htmlContent += '</body></html>';
    return htmlContent;
  }
}