
from datetime import datetime
import streamlit as st
import pandas as pd
import os
import sys
import math

st.title("작업 상태 통계")

st.set_page_config(
    page_title="작업 상태 통계계",  # 브라우저 탭 이름
    layout="wide"
)

# CSV 불러오기
df = pd.read_csv("./data/250917.csv")

# 먼저 "검수 종료일"을 datetime으로 변환
df["검수 종료일"] = pd.to_datetime(df["검수 종료일"])

start_dt = st.date_input("시작일")
start_time = st.time_input("시작 시간")
start_datetime = datetime.combine(start_dt, start_time)

end_dt = st.date_input("종료일")
end_time = st.time_input("종료 시간")
end_datetime = datetime.combine(end_dt, end_time)

st.write("시작:", start_datetime)
st.write("종료:", end_datetime)


if start_datetime and end_datetime:
    # "작업 상태" "ALL_FINISHED","WORK_END", "CHECK_END", "CHECK_ING", "CHECK_REWARD", "CHECK_REJECT"
    # "작업 상태" 칼럼이 "CHECK_END"인 것만 추출
    df = df[df["작업 상태"] == "CHECK_END"]
    # "검수 종료일"이 start_date와 end_date 사이에 있는 것만 추출
    # 필터링 (비트 연산자 & 사용)
    mask = (df["검수 종료일"] >= start_date) & (df["검수 종료일"] <= end_date)
    df_filtered = df[df["작업 상태"] == "CHECK_END"]  # 작업 상태 먼저 필터
    df_filtered = df_filtered[mask]
    st.dataframe(df_filtered)

    # 프로젝트ID 별 작업 개수 계산
    status_counts = df_filtered.groupby("프로젝트ID").size().to_dict()
    # 한줄 씩 출력
    for project_id, count in status_counts.items():
        st.text(f"{project_id}: {count}")