import 'package:first/path_finder/domain/usecases/search_map/search_map_use_case.dart';

import '../../../infrastructures/repository/search_map_repository.dart';


class SearchMapUseCaseImpl implements SearchMapUseCase {
  final SearchMapRepository searchMapRepository;

  SearchMapUseCaseImpl({required this.searchMapRepository});

  @override
  Future<String> execute(String searchQuery) async {
    try {
      // Repository를 통해 데이터를 가져옵니다.
      return await searchMapRepository.searchMap(searchQuery);
    } catch (e) {
      throw Exception('지도 검색 실패: ${e.toString()}');
    }
  }
}
