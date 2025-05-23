import 'package:third/kakao_authentication/presentation/providers/kakao_auth_providers.dart';
import 'package:third/kakao_authentication/presentation/ui/kakao_login_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:provider/provider.dart';

import 'domain/usecase/fetch_user_info_usecase_impl.dart';
import 'domain/usecase/login_usecase_impl.dart';
import 'domain/usecase/request_user_token_usecase_impl.dart';
import 'infrastructure/data_sources/kakao_auth_remote_data_source.dart';
import 'infrastructure/repository/kakao_auth_repository.dart';
import 'infrastructure/repository/kakao_auth_repository_impl.dart';

class KakaoAuthModule {
  static Widget provideKakaoLoginPage() {
    dotenv.load();
    String baseServerUrl = dotenv.env['BASE_URL'] ?? '';

    return MultiProvider(
      providers: [
        Provider<KakaoAuthRemoteDataSource>(
            create: (_) => KakaoAuthRemoteDataSource(baseServerUrl)
        ),
        ProxyProvider<KakaoAuthRemoteDataSource, KakaoAuthRepository>(
          update: (_, remoteDataSrouce, __) =>
              KakaoAuthRepositoryImpl(remoteDataSrouce),
        ),
        ProxyProvider<KakaoAuthRepository, LoginUseCaseImpl>(
            update: (_, repository, __) =>
                LoginUseCaseImpl(repository)
        ),
        ChangeNotifierProvider<KakaoAuthProvider>(
          create: (context) => KakaoAuthProvider(
            loginUseCase: context.read<LoginUseCaseImpl>(),
            fetchUserInfoUseCase: context.read<FetchUserInfoUseCaseImpl>(),
            requestUserTokenUseCase: context.read<RequestUserTokenUseCaseImpl>(),
          ),
        ),
      ],
      child: KakaoLoginPage()
    );
  }
}