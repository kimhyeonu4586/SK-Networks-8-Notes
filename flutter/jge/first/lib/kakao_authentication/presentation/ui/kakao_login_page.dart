import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../common_ui/custom_app_bar.dart';
import '../providers/kakao_auth_providers.dart';

class KakaoLoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomAppBar(
        body: Consumer<KakaoAuthProvider>(
            builder: (context, provider, child) {
              if (provider.isLoading) {
                return Center(child: CircularProgressIndicator());
              }

              return Center(
                child: provider.isLoggedIn ?
                  Column(mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      "로그인 성공!",
                      style: TextStyle(fontSize: 20),
                    )
                  ]) :
                  Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton(
                        onPressed: provider.isLoading ? null : () => provider.login(),
                        child: Text("카카오 로그인")
                      )
                    ]),
              );
            }),
        title: 'Kakao Login'
      )
    );
  }
}