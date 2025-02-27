import 'package:second/path_finder/infrastructures/repository/search_map_repository.dart';

import '../data_sources/path_finder_remote_data_source.dart';

class SearchMapRepositoryImpl implements SearchMapRepository {
  final PathFinderRemoteDataSource remoteDataSource;

  SearchMapRepositoryImpl({required this.remoteDataSource});

  @override
  Future<String> searchMap(String searchQuery) async {
    try {
      return await remoteDataSource.fetchSearchResults(searchQuery);
    } catch (e) {
      throw Exception('지도 검색 실패: ${e.toString()}');
    }
  }
}
