<template>
  <v-container fluid class="d-flex justify-center align-center pa-0" 
  		:style="{ backgroundImage: `url(${loginBgImage})`, backgroundSize: 'cover', backgroundPosition: 'center', height: '100vh' }">
    <v-row justify="center" align="center" class="fill-height ma-0">
      <v-col cols="12" sm="8" md="6" class="text-center">
        <v-btn class="kakao-login-btn" @click="goToKakaoLogin" block>
          <!-- 카카오 로그인 -->
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import loginBgImage from '@/assets/images/fixed/login_bg2.webp';

import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/accountStore';
import { useKakaoAuthenticationStore } from '../../../kakaoAuthentication/stores/kakaoAuthenticationStore'

const router = useRouter();

const form = ref(false);
const email = ref(null);
const password = ref(null);
const visible = ref(false);
const loading = ref(false);
const login_flag = ref(true);
const isEmailCollect = ref(false);
const isPasswordCollect = ref(false);

// Pinia store 상태
const account = useAccountStore();
const kakaoAuthentication = useKakaoAuthenticationStore();

// Google, Kakao, Naver 로그인 함수들
const goToKakaoLogin = async () => {
  // sessionStorage.setItem("loginType", "KAKAO");
  await kakaoAuthentication.requestKakaoLoginToDjango();
};

</script>

<style scoped>
/* 로그인 및 회원가입 버튼 설정 */
.v-btn {
  width: 100%;
  height: 50px;
  margin: 1.3vh auto;
}

.introduction {
  color: rgb(255, 255, 255);
  word-break: break-word;
}

@media (max-width: 768px) {
  .v-btn {
    height: 45px; /* 모바일 환경에서는 높이를 줄임 */
  }
  .login_logo {
    height: 19vh;
  }
}

@media (max-width: 480px) {
  .v-btn {
    height: 33px; /* 작은 모바일 환경에서는 더 작게 설정 */
  }
  .login_logo {
    height: 13vh;
  }
  .introduction {
  white-space: pre-wrap;
}

}

/* Kakao 로그인 버튼 설정 */
.kakao-login-btn {
  position: relative;
  top: 40vh;
  width: 200px !important;
  height: 150px !important; /* Force height change */
  background-image: url("@/assets/images/fixed/btn_login_kakao.png");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FFEA00;
  border-radius: 1.4vh;
  cursor: pointer;
}

.v-text-field input {
  background-color: transparent !important;
  color: black !important;
  /* 입력값을 검정색으로 설정 */
}

.v-label {
  color: black !important;
  /* 레이블을 검정색으로 설정 */
}


/* 로그인 폼의 텍스트 필드 라벨 색상 설정 */
:deep(.v-label.v-field-label) {
  color: rgba(255, 255, 255, 0.8) !important;
}

/* 로그인 폼의 텍스트 필드 입력값 색상 설정 */
:deep(.v-text-field input) {
  color: #fff;
}

/* 눈 아이콘 색상 설정 */
:deep(.mdi-eye::before),
:deep(.mdi-eye-off::before) {
  color: rgba(255, 255, 255, 0.8) !important;
}

/* 오류 메시지 스타일링 */
:deep(.v-messages__message) {
  color: rgb(0, 0, 255) !important;
  /* 메시지 색상 */
  font-size: 12px;
  /* 메시지 폰트 크기 */
}

/* 텍스트 필드 에러 상태의 레이블 색상을 초록색으로 변경 */
:deep(.v-field--error:not(.v-field--disabled) .v-label.v-field-label) {
  color: rgba(0, 0, 255) !important;
  /* 에러 상태의 레이블 색상을 초록색으로 변경 */
}
</style>