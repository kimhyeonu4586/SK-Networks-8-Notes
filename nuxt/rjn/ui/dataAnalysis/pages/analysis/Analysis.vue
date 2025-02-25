<template>
  <v-container class="pa-4">
    <v-card elevation="2" class="pa-4">
      <v-card-title class="text-h5">File Upload</v-card-title>
      <v-card-text>
        <v-file-input
          v-model="selectedFile"
          label="Select a file"
          outlined
          dense
          prepend-icon="mdi-file-upload"
          accept=".xlsx,.xls,.csv"
        />
      </v-card-text>
      <v-card-actions>
        <v-btn
          :disabled="!selectedFile"
          color="primary"
          class="ml-auto"
          @click="uploadFile"
        >
          <v-icon left>mdi-cloud-upload</v-icon>
          Upload
        </v-btn>
      </v-card-actions>
      <v-divider class="my-4"></v-divider>

      <!-- Average Purchase Cost Graph -->
      <v-img
        v-if="averagePurchaseCostImage"
        :src="averagePurchaseCostImage"
        alt="Average Purchase Cost Graph"
        max-height="500"
        contain
      />
      <!-- Top Revenue Graph -->
      <v-img
        v-if="topRevenueImage"
        :src="topRevenueImage"
        alt="Top Revenue Graph"
        max-height="500"
        contain
      />
      <!-- 4분위수 Graph -->
      <v-img
        v-if="quartileImage"
        :src="quartileImage"
        alt="Quartile Graph"
        max-height="500"
        contain
      />
      <!-- Heatmap Graph -->
      <v-img
        v-if="heatmapImage"
        :src="heatmapImage"
        alt="Heatmap Graph"
        max-height="500"
        contain
      />
    </v-card>

    <!-- Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMessage }}
      <template #action>
        <v-btn color="pink" text @click="snackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { useDataAnalysisStore } from "~/dataAnalysis/stores/dataAnalysisStore";

export default {
  data() {
    return {
      selectedFile: null, // 선택한 파일
      averagePurchaseCostImage: null, // 평균 구매 비용 그래프 이미지
      topRevenueImage: null, // 최고 매출 그래프 이미지
      quartileImage: null, // 4분위수
      heatmapImage: null, // 히트맵 그래프 이미지
      snackbar: false, // Snackbar 표시 여부
      snackbarMessage: "", // Snackbar 메시지
      snackbarColor: "", // Snackbar 색상
    };
  },
  methods: {
    async uploadFile() {
      const dataAnalysisStore = useDataAnalysisStore();
      if (!this.selectedFile) {
        this.snackbarMessage = "Please select a file first.";
        this.snackbarColor = "error";
        this.snackbar = true;
        return;
      }
      try {
        const { 
          averagePurchaseCostImageBase64, 
          topRevenueImageBase64,
          quartileImageBase64,
          heatmapImageBase64
        } = await dataAnalysisStore.requestDataAnalysis(this.selectedFile);

        // Base64 데이터에 접두사 추가
        this.averagePurchaseCostImage = `data:image/png;base64,${averagePurchaseCostImageBase64}`;
        this.topRevenueImage = `data:image/png;base64,${topRevenueImageBase64}`;
        this.quartileImage = `data:image/png;base64,${quartileImageBase64}`;
        this.heatmapImage = `data:image/png;base64,${heatmapImageBase64}`;

        this.snackbarMessage = "File uploaded successfully!";
        this.snackbarColor = "success";
        this.snackbar = true;
      } catch (error) {
        console.error("Error uploading file:", error);
        this.snackbarMessage = "File upload failed.";
        this.snackbarColor = "error";
        this.snackbar = true;
      }
    },
  },
};
</script>

<style scoped>
.v-file-input {
  max-width: 400px;
}
</style>
