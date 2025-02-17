import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager

from game_software_analysis.repository.game_software_analysis_repository import GameSoftwareAnalysisRepository


class GameSoftwareAnalysisRepositoryImpl(GameSoftwareAnalysisRepository):

    def loadDataFromFile(self, filePath: str) -> pd.DataFrame:
        try:
            data = pd.read_excel(filePath)
            return data
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def analyzeAgeGroupData(self, data: pd.DataFrame):
        # 연령대 계산 (예: 10대, 20대, 30대 등으로 나누기)
        data['age_group'] = data['age'].apply(lambda x: f"{(x // 10) * 10}s")  # 예: 20대, 30대, ...

        # 연령대별로 게임 소프트웨어의 구매 건수와 구매 총액 계산
        ageGroupData = data.groupby(['age_group', 'game_software_title']).agg(
            total_purchase_count=pd.NamedAgg(column='quantity', aggfunc='sum'),
            total_purchase_cost=pd.NamedAgg(column='total_price', aggfunc='sum')
        ).reset_index()

        # 연령대별로 가장 많이 구매한 게임 소프트웨어 정렬
        ageGroupData['average_purchase_cost'] = ageGroupData['total_purchase_cost'] / ageGroupData[
            'total_purchase_count']

        return ageGroupData

    # sudo apt update
    # sudo apt install -y fonts-nanum fonts-noto-cjk
    # sudo apt install fonts-nanum
    def plotAveragePurchaseCost(self, ageGroupData: pd.DataFrame):
        # 정확한 한글 폰트 경로 설정
        fontPath = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 실제 폰트 경로 확인
        fontProp = font_manager.FontProperties(fname=fontPath)

        # matplotlib의 기본 폰트 설정
        plt.rcParams['font.family'] = fontProp.get_name()  # 올바른 폰트 이름 사용
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호가 깨지지 않도록 설정

        plt.figure(figsize=(10, 6))

        # 'game_software_title'을 색상별로 구분하는 그래프 그리기
        sns.barplot(data=ageGroupData, x='age_group', y='average_purchase_cost', hue='game_software_title')

        # 제목과 축 레이블 설정
        plt.title('연령대별 평균 구매 금액')
        plt.xlabel('연령대')
        plt.ylabel('평균 구매 금액')

        # x축 레이블 가운데 정렬 및 회전
        plt.xticks(rotation=45, ha='center')

        # 범례 위치를 하단 가운데로 설정
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

        # 그래프 이미지를 파일로 저장
        graphPath = os.path.join(os.getcwd(), "resource", "age_group_purchase_cost.png")
        plt.savefig(graphPath, bbox_inches='tight')  # bbox_inches='tight'로 레이아웃이 잘리는 문제 방지
        plt.close()

        print(f"Graph saved to: {graphPath}")
        return graphPath

    def plotTopRevenueGame(self, data: pd.DataFrame):
        # 게임별 총 매출 계산
        gameRevenueData = data.groupby('game_software_title').agg(
            total_revenue=pd.NamedAgg(column='total_price', aggfunc='sum')
        ).reset_index()

        # 매출이 높은 순으로 정렬
        topRevenueData = gameRevenueData.sort_values(by='total_revenue', ascending=False).head(10)

        # 정확한 한글 폰트 경로 설정
        fontPath = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 실제 폰트 경로 확인
        fontProp = font_manager.FontProperties(fname=fontPath)

        # matplotlib의 기본 폰트 설정
        plt.rcParams['font.family'] = fontProp.get_name()  # 올바른 폰트 이름 사용
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호가 깨지지 않도록 설정

        plt.figure(figsize=(12, 6))

        # 매출이 높은 순으로 게임 비교
        sns.barplot(data=topRevenueData, x='game_software_title', y='total_revenue')

        # 제목과 축 레이블 설정
        plt.title('매출이 높은 게임 비교')
        plt.xlabel('게임 소프트웨어')
        plt.ylabel('총 매출')

        # x축 레이블 가운데 정렬 및 회전
        plt.xticks(rotation=45, ha='center')

        # 그래프 이미지를 파일로 저장
        graphPath = os.path.join(os.getcwd(), "resource", "top_revenue_game.png")
        plt.savefig(graphPath, bbox_inches='tight')  # bbox_inches='tight'로 레이아웃이 잘리는 문제 방지
        plt.close()

        print(f"Graph saved to: {graphPath}")
        return graphPath

    def plotQuartileVisualization(self, data: pd.DataFrame):
        """모든 게임 타이틀에 대해 연령대별로 총 구매 금액(total_purchase_cost)의 4분위수를 계산하고 하나의 그래프에 시각화하는 함수"""

        # 데이터의 컬럼 출력
        print(f"Columns in the data: {data.columns}")
        print(f"data: {data}")

        unique_game_titles = data['game_software_title'].unique()
        print(f"Unique game titles in the data: {unique_game_titles}")

        # 여러 게임에 대한 4분위수 데이터를 저장할 리스트
        all_quartiles = []

        # 모든 게임 타이틀에 대해 처리
        for game_title in unique_game_titles:
            # 특정 게임 데이터를 필터링
            gameData = data[data['game_software_title'] == game_title]

            # 연령대별로 구매 금액에 대한 4분위수 계산
            quartiles = gameData.groupby('age_group')['total_purchase_cost'].describe(percentiles=[.25, .5, .75])

            # describe() 결과에서 4분위수 (25%, 50%, 75%)만 추출
            quartiles = quartiles[['25%', '50%', '75%']].reset_index()
            quartiles['game_software_title'] = game_title  # 게임 타이틀 추가

            # 4분위수 데이터를 리스트에 추가
            all_quartiles.append(quartiles)

        # 모든 게임에 대한 4분위수 데이터를 하나로 합침
        all_quartiles_df = pd.concat(all_quartiles)

        # 4분위수 데이터 확인
        print(f"Combined quartile data:\n{all_quartiles_df}")

        # 정확한 한글 폰트 경로 설정
        fontPath = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 실제 폰트 경로 확인
        fontProp = font_manager.FontProperties(fname=fontPath)

        # matplotlib 기본 폰트 설정
        plt.rcParams['font.family'] = fontProp.get_name()
        plt.rcParams['axes.unicode_minus'] = False

        # 그래프 크기 확대 (16x10 크기로 설정)
        plt.figure(figsize=(16, 10))

        # 색상 팔레트 설정 (게임 타이틀별 색상 다르게 지정)
        palette = sns.color_palette("tab10", n_colors=len(unique_game_titles))

        # 연령대별로 각 게임 타이틀에 대한 박스 플롯을 색상 구분하여 그리기
        ax = sns.boxplot(
            data=data,
            x='age_group',
            y='total_purchase_cost',
            hue='game_software_title',
            showfliers=False,
            linewidth=3,  # 선 굵기 강조
            palette=palette  # 수동 색상 팔레트 적용
        )

        # 각 연령대별로 상위 3개의 게임 표시
        for age_group in data['age_group'].unique():
            # 해당 연령대의 데이터 필터링
            age_group_data = data[data['age_group'] == age_group]

            # 상위 3개 게임 찾기 (total_purchase_cost 기준으로 내림차순)
            top_3_games = age_group_data.groupby('game_software_title')['total_purchase_cost'] \
                              .sum() \
                              .sort_values(ascending=False)[:3]

            # 상위 3개 게임에 대해 마커 표시
            for game in top_3_games.index:
                top_game_data = age_group_data[age_group_data['game_software_title'] == game]
                max_purchase_cost = top_game_data['total_purchase_cost'].max()

                # 게임 이름과 해당 구매 금액 위치에 표시
                plt.text(
                    x=age_group,
                    y=max_purchase_cost + 500000,  # 약간 위쪽에 텍스트 표시
                    s=game,
                    horizontalalignment='center',
                    fontsize=10,
                    weight='bold',
                    color='black'
                )
                plt.scatter(
                    x=[age_group] * len(top_3_games.index),
                    y=top_3_games.values,
                    color='red',
                    s=100,
                    marker='o',
                    edgecolor='black',
                    label=game
                )

        # 제목과 축 레이블 설정
        plt.title('모든 게임의 연령대별 구매 금액 4분위수 박스 플롯', fontsize=16)
        plt.xlabel('연령대', fontsize=12)
        plt.ylabel('총 구매 금액', fontsize=12)

        # 범례 위치 설정
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=10)

        # 그래프 이미지를 파일로 저장
        graphPath = os.path.join(os.getcwd(), "resource", "quartile_visualization_all_games_colored_with_top3.png")
        plt.savefig(graphPath, bbox_inches='tight')
        plt.close()

        print(f"Graph saved to: {graphPath}")
        return graphPath

    def plotHeatmap(self, data: pd.DataFrame):
        print(f"plotHeatmap() data:\n{data}")
        # 연령대별 게임 타이틀의 총 구매 금액 데이터 준비
        heatmapData = (
            data.groupby(['age_group', 'game_software_title'])['total_price']
            .sum()  # 연령대별 게임 타이틀의 총 구매 금액 합계 계산
            .unstack()  # 행: 연령대, 열: 게임 타이틀로 변환
        )
        print(f"plotHeatmap() heatmapData:\n{heatmapData}")

        # NaN 값을 0으로 대체
        heatmapData.fillna(0, inplace=True)

        # 정확한 한글 폰트 경로 설정
        fontPath = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 실제 폰트 경로 확인
        fontProp = font_manager.FontProperties(fname=fontPath)

        # matplotlib 기본 폰트 설정
        plt.rcParams['font.family'] = fontProp.get_name()
        plt.rcParams['axes.unicode_minus'] = False

        # 히트맵 시각화
        plt.figure(figsize=(12, 8))  # 그래프 크기 설정
        sns.heatmap(
            heatmapData,
            cmap="YlGnBu",  # 색상 팔레트 지정
            annot=True,  # 셀 안에 값 표시
            fmt=".0f",  # 값 형식 지정 (정수로 표시)
            linewidths=0.5,  # 셀 간 경계선 설정
            cbar_kws={'label': '총 구매 금액'},  # 컬러바 레이블 설정
        )

        # 제목 및 축 레이블 설정
        plt.title('연령대와 게임 타이틀별 총 구매 금액 히트맵', fontsize=16)
        plt.xlabel('게임 소프트웨어', fontsize=12)
        plt.ylabel('연령대', fontsize=12)

        # x축 레이블 가운데 정렬 및 회전
        plt.xticks(rotation=45, ha='center')

        # 그래프 이미지를 파일로 저장
        graphPath = os.path.join(os.getcwd(), "resource", "age_group_game_heatmap.png")
        plt.savefig(graphPath, bbox_inches='tight')  # bbox_inches='tight'로 레이아웃이 잘리는 문제 방지
        plt.close()

        print(f"Graph saved to: {graphPath}")
        return graphPath
