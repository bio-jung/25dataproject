import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='cp949')
    df = df[df.columns.drop(list(df.filter(regex='총인구수|연령구간인구수')))]
    df = df.rename(columns={df.columns[0]: "지역"})
    df = df.replace(",", "", regex=True)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# 지역 리스트 생성
region_list = sorted(df["지역"].unique())
selected_region = st.selectbox("지역을 선택하세요", region_list)

# 선택된 지역 필터링
region_data = df[df["지역"] == selected_region].T.reset_index()
region_data.columns = ["연령", "인구수"]
region_data = region_data[1:]  # 지역명이 들어간 첫 줄 제외

# 연령 이름 정제
region_data["연령"] = region_data["연령"].str.extract(r"(\d+세|100세 이상)")
region_data["인구수"] = region_data["인구수"].astype(int)

# 시각화
fig = px.bar(region_data, x="연령", y="인구수", title=f"{selected_region} 연령별 인구 분포", labels={"연령": "연령", "인구수": "인구 수"})
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig)
