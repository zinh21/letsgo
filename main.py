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
# 2. 장르 안에 영화가 들어 있는 트리맵 (크기: 총 관객)
# =========================================
st.header("2. 장르 안의 영화별 총 관객 (트리맵)")

fig2 = px.treemap(
    df,
    path=['genre', 'movieNm'],
    values='total_audi',
    hover_data={'total_audi': True},
    title="장르 - 영화별 총 관객 트리맵"
)
fig2.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객: %{value:,}명<extra></extra>'
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 각 장르 안에서 어떤 영화가 관객을 많이 모았는지, 장르별로 칸의 전체 크기가 어떻게 다른지 등)")

st.divider()

# =========================================
# 3. 총 관객 수 분포 - 히스토그램
# =========================================
st.header("3. 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    labels={"total_audi": "총 관객 수"},
    title="영화별 총 관객 수 분포"
)
fig3.update_layout(yaxis_title="영화 편수")

st.plotly_chart(fig3, use_container_width=True)

# 가장 관객이 많은 영화, 최빈 구간 찾기
max_audi_row = df.loc[df['total_audi'].idxmax()]
bin_counts, bin_edges = pd.cut(df['total_audi'], bins=30, retbins=True)
most_common_bin = bin_counts.value_counts().idxmax()

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 영화는 총 관객 수 **{int(most_common_bin.left):,}명 ~ {int(most_common_bin.right):,}명** "
    f"구간에 몰려 있습니다. 가장 관객이 많은 영화는 **'{max_audi_row['movieNm']}'**로, "
    f"총 **{int(max_audi_row['total_audi']):,}명**을 동원했습니다."
)

st.divider()

# =========================================
# 4. 개봉일 스크린수와 총 관객 수의 관계 - 산점도
# =========================================
st.header("4. 개봉일 스크린수와 총 관객 수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객 수"},
    title="개봉일 스크린수 vs 총 관객 수"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 스크린수가 많을수록 관객 수도 많아지는 경향이 있는지, 장르별로 다른 경향이 있는지 등)")

st.divider()

# =========================================
# 5. 영화 10편 이상 장르의 총 관객 수 박스플롯
# =========================================
st.header("5. 장르별 총 관객 수 분포 (10편 이상 장르만)")

genre_count_series = df['genre'].value_counts()
major_genres = genre_count_series[genre_count_series >= 10].index
df_major = df[df['genre'].isin(major_genres)]

fig5 = px.box(
    df_major,
    x="genre",
    y="total_audi",
    hover_data=['movieNm'],
    labels={"genre": "장르", "total_audi": "총 관객 수"},
    title="장르별 총 관객 수 분포 (영화 10편 이상인 장르)"
)
fig5.update_traces(
    hovertemplate='<b>%{customdata[0]}</b><br>총 관객: %{y:,}명<extra></extra>'
)
fig5.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 어떤 장르가 관객 수 편차가 큰지, 이상치로 튀는 영화는 무엇인지 등)")

st.divider()

# =========================================
# 6. 개봉일 스크린수 vs 총 관객 수 (버블 그래프, 크기: 첫 주 관객)
# =========================================
st.header("6. 개봉일 스크린수와 총 관객 수의 관계 (버블 그래프)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    hover_name="movieNm",
    size_max=40,
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "first_week_audi": "개봉 첫 주 관객"
    },
    title="개봉일 스크린수 vs 총 관객 수 (원의 크기 = 개봉 첫 주 관객)"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 첫 주 관객이 많은 영화가 총 관객 수도 많은지, 원의 크기와 위치 사이에 관계가 있는지 등)")

st.divider()

# =========================================
# 7. 제작 국가 -> 장르 선버스트 그래프
# =========================================
st.header("7. 제작 국가별 장르 분포 (선버스트)")

nation_genre_counts = df.groupby(['nation', 'genre']).size().reset_index(name='count')

fig7 = px.sunburst(
    nation_genre_counts,
    path=['nation', 'genre'],
    values='count',
    title="제작 국가 - 장르별 영화 편수 선버스트"
)
fig7.update_traces(
    hovertemplate='<b>%{label}</b><br>편수: %{value}편<extra></extra>'
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info("여기에 학생이 직접 관찰한 내용을 적어보세요. (예: 어떤 국가에서 어떤 장르 영화를 많이 만드는지, 국가별로 장르 다양성이 어떻게 다른지 등)")

st.divider()

# =========================================
# 8. 첫 주 관객 수가 총 관객 수를 얼마나 잘 예측할까? (산점도 + 추세선)
# =========================================
st.header("8. 첫 주 관객 수가 총 관객 수를 얼마나 잘 예측할까?")

fig8 = px.scatter(
    df,
    x="first_week_audi",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    trendline="ols",
    trendline_scope="overall",
    labels={"first_week_audi": "개봉 첫 주 관객", "total_audi": "총 관객 수"},
    title="첫 주 관객 수가 총 관객 수를 얼마나 잘 예측할까?"
)

st.plotly_chart(fig8, use_container_width=True)

# 상관계수 계산
correlation = df['first_week_audi'].corr(df['total_audi'])

st.markdown("#### 📌 이 그래프로 알 수 있는 것")
st.info(
    f"첫 주 관객 수와 총 관객 수의 상관계수는 **{correlation:.2f}**입니다. "
    f"(1에 가까울수록 강한 비례 관계, 0에 가까울수록 관계가 약함) "
    f"점들이 검은색 추세선에 가깝게 모여 있을수록 첫 주 관객으로 총 관객을 잘 예측할 수 있다는 뜻입니다."
)

st.divider()

st.caption("데이터 출처: KOBIS(영화진흥위원회) 박스오피스 데이터")
