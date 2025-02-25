import * as axiosUtility from "../../utility/axiosInstance"

export const dataAnalysisAction = {
  async requestDataAnalysis(excelFile) {
    const { fastapiAxiosInst } = axiosUtility.createAxiosInstances();

    if (!excelFile) {
      alert("Please select a file first.");
      return;
    }
    try {
      const formData = new FormData();
      formData.append("file", excelFile);

      const response = await fastapiAxiosInst.post("/game-software-data/analysis", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log(`response.data: ${response.data}`)

      const { 
        averagePurchaseCostImageBase64, 
        topRevenueImageBase64, 
        quartileImageBase64,
        heatmapImageBase64,
      } = response.data;

      // 데이터 유효성 확인
      if (!averagePurchaseCostImageBase64 || !topRevenueImageBase64 || !quartileImageBase64 || !heatmapImageBase64) {
        throw new Error("Base64 data is missing from the response.");
      }

      console.log('requestDataAnalysis() return data')

      return { 
        averagePurchaseCostImageBase64, 
        topRevenueImageBase64,
        quartileImageBase64,  // 4분위수 그래프 추가
        heatmapImageBase64,
      };
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("File upload failed.");
      throw error
    }
  },

  base64ToBlob(base64, mimeType) {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length).map((_, i) => byteCharacters.charCodeAt(i));
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  },
}