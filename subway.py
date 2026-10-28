import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="부산 지하철 이용객 지도", layout="wide")

st.title("🚇 부산 지하철 역별 이용객 수 지도 분석")

# 1. 파일 업로드 기능
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # CSV 파일 읽기
    df = pd.read_csv(uploaded_file)

    # 호선별 지정 색상 (1호선 주황, 2호선 초록, 3호선 갈색, 4호선 파랑)
    color_map = {
        '1호선': 'orange',
        '2호선': 'green',
        '3호선': 'brown',
        '4호선': 'blue'
    }

    # ① 호선 선택 멀티셀렉트 필터 (기본값: 전체 선택)
    lines = df['호선'].unique().tolist()
    selected_lines = st.multiselect("조회할 호선을 선택하세요", lines, default=lines)

    # 선택된 호선만 데이터 필터링
    filtered_df = df[df['호선'].isin(selected_lines)]

    # ② 이용객 상위 5개 역 표로 표시
    st.subheader("🏆 이용객 상위 5개 역")
    top5_df = filtered_df.sort_values(by='이용객수', ascending=False).head(5)
    st.dataframe(top5_df[['호선', '역명', '이용객수']])

    # ③ folium 지도 생성 및 마커 추가
    st.subheader("🗺️ 역별 이용객 수 지도")
    m = folium.Map(location=[35.1795543, 129.0756416], zoom_start=11)

    scale_factor = 0.05

    # 필터링된 데이터만 지도에 표시
    for idx, row in filtered_df.iterrows():
        radius_size = np.sqrt(row['이용객수']) * scale_factor

        # 호선에 맞는 색상 가져오기 (없는 호선은 기본 'gray')
        line_color = color_map.get(row['호선'], 'gray')

        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=radius_size,
            color=line_color,
            fill=True,
            fill_color=line_color,
            fill_opacity=0.6,
            tooltip=f"역명: {row['역명']} ({row['호선']})",
            popup=f"{row['역명']}역 이용객 수: {row['이용객수']:,}명"
        ).add_to(m)

    st_folium(m, width=800, height=500)

else:
    st.info("시작하려면 busan_subway.csv 파일을 업로드해 주세요.")