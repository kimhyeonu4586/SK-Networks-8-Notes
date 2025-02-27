import 'package:second/path_finder/presentation/providers/path_finder_search_map_provider.dart';
import 'package:second/path_finder/presentation/ui/path_finder_search_map_page.dart';
import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';
import 'package:provider/single_child_widget.dart';

import 'domain/usecases/search_map/search_map_use_case_impl.dart';
import 'infrastructures/data_sources/path_finder_remote_data_source.dart';
import 'infrastructures/repository/search_map_repository_impl.dart';

class PathFinderModule {
  static final pathFinderRemoteDataSource = PathFinderRemoteDataSource();
  static final searchMapRepository = SearchMapRepositoryImpl(remoteDataSource: pathFinderRemoteDataSource);

  static final searchMapUseCase = SearchMapUseCaseImpl(searchMapRepository: searchMapRepository);

  static List<SingleChildWidget> provideCommonProviders() {
    return [
      Provider(create: (_) => searchMapUseCase),
    ];
  }

  static Widget providePathFinderSearchMapPage() {
    return MultiProvider(
      providers: [
        ...provideCommonProviders(),
        ChangeNotifierProvider(
          create: (_) =>
              PathFinderSearchMapProvider(searchMapUseCase: searchMapUseCase),
        )
      ],
      child: PathFinderSearchMapPage(),
    );
  }
}