import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import duckdb
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="그래프 확인",
    page_icon="📋",
    layout="wide"
)

#일별 변화율
today_date = datetime.today().date()
today_str = today_date.strftime('%Y%m%d')

df = pd.read_csv(f"./data/{today_str}.csv")
df["작업 종료일"] = pd.to_datetime(df["작업 종료일"], format='ISO8601').dt.date

start_date = (today_date - timedelta(days=7)).strftime('%Y-%m-%d')
end_date = (today_date - timedelta(days=1)).strftime('%Y-%m-%d')

# 일별 변화율 그래프
query = f"""
SELECT
    "작업 종료일",
    COUNT("데이터 ID") AS "작업 수량"
FROM df
WHERE "작업 종료일" >= '{start_date}' AND "작업 종료일" <= '{end_date}'
AND "작업 상태" IN ('ALL_FINISHED', 'CHECK_END')
GROUP BY "작업 종료일"
ORDER BY "작업 종료일" ASC
"""
result = duckdb.query(query).to_df()
result["작업 종료일"]= result["작업 종료일"].astype(str)

# 제목과 설명
st.title("일별 작업 현황")
# 2개 컬럼으로 나누기 (차트를 더 크게)
col1, col2 = st.columns([1, 2])

# 왼쪽 컬럼: 데이터 테이블
with col1:
    st.subheader("📋 작업 데이터")
    st.markdown(f"**기간**: {start_date} ~ {end_date}")
    st.dataframe(result, use_container_width=True)

# 오른쪽 컬럼: 차트
with col2:
    
    # Plotly로 꾸민 차트
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=result["작업 종료일"],
        y=result["작업 수량"],
        mode='lines+markers',
        name='작업 수량',
        line=dict(color='#4a90e2', width=3),
        marker=dict(size=8, color='#ff6b6b', symbol='circle'),
        hovertemplate='<b>%{x}</b><br>작업 수량: %{y}건<extra></extra>'
    ))
    
    # 차트 꾸미기
    fig.update_layout(
        title={
            'text': "최근 7일간 작업 완료 현황",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#4a4a4a'}
        },
        xaxis_title="작업 종료일",
        yaxis_title="작업 수량 (건)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500  # 차트 높이 증가
    )
    
    # x축 설정
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        tickangle=45,
        linecolor='#666666',
        tickcolor='#666666'
    )
    
    # y축 설정
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='#666666',
        linecolor='#666666',
        tickcolor='#666666'
    )
    
    st.plotly_chart(fig, use_container_width=True)
