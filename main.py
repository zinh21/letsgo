import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화 216편의 데이터를 다양한 그래프로 살펴봅니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열에서 세로막대(|) 기호로 여러 개 적힌 경우 첫 번째 장르만 사용
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    # openDt를 날짜 형식으로 변환 (여덟 자리 숫자 -> 날짜)
    df['openDt'] = pd.to_datetime(df['openDt'], format='%Y%m%d', errors='coerce')
    
    return df

df = load_data()

# 데이터 미리보기
with st.expander("📋 원본 데이터 미리보기"):
    st.dataframe(df)

st.divider()

# =========================================
# 1. 장르별 영화 편수 - 도넛 그래프
# =========================================
st.header("1. 장르별 영화 편수")

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig1 = go.Figure(data=[go.Pie(
    labels=genre_counts['genre'],
    values=genre_counts['count'],
    hole=0.5,
    hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>'
)])

fig1.update_layout(
    title="장르별 영화 편수 비율",
    legend_title="장르"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 어떤 장르가 가장 많은지, 상위 몇 개 장르가 전체의 얼마를 차지하는지 등)")

st.divider()

# =========================================
# 2. 총 관객 수 분포 - 히스토그램
# =========================================
st.header("2. 총 관객 수 분포")

fig2 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    labels={"total_audi": "총 관객 수"},
    title="영화별 총 관객 수 분포"
)
fig2.update_layout(yaxis_title="영화 편수")

st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 관객 수가 어느 구간에 가장 많이 몰려 있는지 등)")

st.divider()

# =========================================
# 3. 개봉일 스크린수와 총 관객 수의 관계 - 산점도
# =========================================
st.header("3. 개봉일 스크린수와 총 관객 수의 관계")

fig3 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객 수"},
    title="개봉일 스크린수 vs 총 관객 수"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 스크린수가 많을수록 관객 수도 많아지는 경향이 있는지 등)")

st.divider()

# =========================================
# 4. 장르별 총 관객 수 분포 - 박스플롯
# =========================================
st.header("4. 장르별 총 관객 수 분포")

fig4 = px.box(
    df,
    x="genre",
    y="total_audi",
    labels={"genre": "장르", "total_audi": "총 관객 수"},
    title="장르별 총 관객 수 분포"
)
fig4.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 어떤 장르가 관객 수 편차가 큰지, 중앙값이 높은 장르는 무엇인지 등)")

st.divider()

# =========================================
# 5. 10위권 유지 일수와 총 관객 수의 관계 - 산점도
# =========================================
st.header("5. 10위권 유지 일수와 총 관객 수의 관계")

fig5 = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    hover_name="movieNm",
    labels={"days_in_top10": "10위권 유지 일수", "total_audi": "총 관객 수", "first_week_audi": "개봉 첫 주 관객"},
    title="10위권 유지 일수 vs 총 관객 수 (원의 크기 = 개봉 첫 주 관객)"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 오래 상위권에 머문 영화가 총 관객 수도 많은지 등)")

st.divider()

st.caption("데이터 출처: KOBIS(영화진흥위원회) 박스오피스 데이터")
