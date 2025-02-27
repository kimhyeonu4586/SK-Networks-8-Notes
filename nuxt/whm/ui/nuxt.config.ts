import { defineNuxtConfig } from "nuxt/config";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  extends: [
    "./home/nuxt.config.ts",
    "./pandas_basic/nuxt.config.ts",
    "./account/nuxt.config.ts",
    "./kakaoAuthentication/nuxt.config.ts",
    "./gameSoftware/nuxt.config.ts",
    "./board/nuxt.config.ts",
    "./cart/nuxt.config.ts",
    "./order/nuxt.config.ts",
    "./payments/nuxt.config.ts",
    "./imageGallery/nuxt.config.ts",
    "./blogPost/nuxt.config.ts",
  ],

  css: [
    "vuetify/styles",
    "@mdi/font/css/materialdesignicons.min.css",
    "quill/dist/quill.snow.css",
  ],

  build: {
    transpile: [
      "vuetify",
      "vue-toastification",
      // "@vueup/vue-quill", "quill-delta"
    ],
  },

  vite: {
    ssr: {
      noExternal: ["vuetify"],
    },
  },

  components: [
    {
      path: "~/navigationBar",
      extensions: ["vue"],
    },
  ],

  modules: [
    "vuetify-nuxt-module",
    "@pinia/nuxt",
    "~/home/index.ts",
    "~/pandas_basic/index.ts",
    "~/account/index.ts",
    "~/kakaoAuthentication/index.ts",
    "~/gameSoftware/index.ts",
    "~/board/index.ts",
    "~/cart/index.ts",
    "~/order/index.ts",
    "~/payments/index.ts",
    "~/imageGallery/index.ts",
    "~/blogPost/index.ts",
  ],

  imports: {
    dirs: ["./stores"],
  },

  runtimeConfig: {
    public: {
      MAIN_API_URL: process.env.VUE_APP_BASE_URL,
      AI_BASE_URL: process.env.VUE_APP_AI_BASE_URL,
      TOSS_CLIENT_KEY: process.env.TOSS_CLIENT_KEY,
      TOSS_SECRET_KEY: process.env.TOSS_SECRET_KEY,
      AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID,
      AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY,
      AWS_REGION: process.env.AWS_REGION,
      AWS_BUCKET_NAME: process.env.AWS_BUCKET_NAME,
    },
  },
});
