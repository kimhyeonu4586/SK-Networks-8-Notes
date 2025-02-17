import base64

import pandas as pd

from game_software_analysis.repository.game_software_analysis_repository_impl import GameSoftwareAnalysisRepositoryImpl
from game_software_analysis.service.game_software_analysis_service import GameSoftwareAnalysisService


class GameSoftwareAnalysisServiceImpl(GameSoftwareAnalysisService):
    def __init__(self):
        self.__gameSoftwareAnalysisRepository = GameSoftwareAnalysisRepositoryImpl()

    async def requestAnalysis(self, filePath: str):
        data = self.__gameSoftwareAnalysisRepository.loadDataFromFile(filePath)

        if data is None:
            raise Exception("Error reading data from the file.")

        # 연령대별 분석 수행
        analysisResult = self.__gameSoftwareAnalysisRepository.analyzeAgeGroupData(data)
        gaveragePurchaseCostImagePath = self.__gameSoftwareAnalysisRepository.plotAveragePurchaseCost(analysisResult)
        topRevenueImagePath = self.__gameSoftwareAnalysisRepository.plotTopRevenueGame(data)

        # 4분위수 그래프 생성
        # quartileImagePath = self.__gameSoftwareAnalysisRepository.plotQuartileVisualization(analysisResult,
        #                                                                                     'average_purchase_cost')
        quartileImagePath = self.__gameSoftwareAnalysisRepository.plotQuartileVisualization(analysisResult)

        # 히트맵 생성
        heatmapImagePath = self.__gameSoftwareAnalysisRepository.plotHeatmap(data)

        averagePurchaseCostImageBase64 = self.convertImageToBase64(gaveragePurchaseCostImagePath)
        topRevenueImageBase64 = self.convertImageToBase64(topRevenueImagePath)
        quartileImageBase64 = self.convertImageToBase64(quartileImagePath)
        heatmapImageBase64 = self.convertImageToBase64(heatmapImagePath)

        # 결과 및 그래프 경로 반환
        return {
            "averagePurchaseCostImageBase64": averagePurchaseCostImageBase64,
            "topRevenueImageBase64": topRevenueImageBase64,
            "quartileImageBase64": quartileImageBase64,
            "heatmapImageBase64": heatmapImageBase64
        }

    def convertImageToBase64(self, imagePath: str) -> str:
        print(f"imagePath: {imagePath}")
        """이미지 파일을 Base64로 변환하는 함수"""
        try:
            with open(imagePath, "rb") as imgFile:
                return base64.b64encode(imgFile.read()).decode("utf-8")

        except Exception as e:
            print(f"Error encoding image: {e}")
            return None