import 'package:first/common_ui/custom_app_bar.dart';
import 'package:first/kakao_authentication/presentation/providers/kakao_auth_providers.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:provider/provider.dart';

class HomePage extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    final kakaoAuthProvider = Provider.of<KakaoAuthProvider>(context);

    return Scaffold(
      body: CustomAppBar(
        body: Center(
            child: Text(
              kakaoAuthProvider.isLoggedIn
                ? 'Welcome to HomePage'
                : "Use after login",
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            )
        ),
      ),
    );
  }
}