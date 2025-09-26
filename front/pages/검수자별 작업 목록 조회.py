import streamlit as st
import pandas as pd
import os
import sys
import math
from datetime import datetime

from back.back import get_checker_list

def paginate_dataframe(df, page_size=10):
    total_pages = math.ceil(len(df) / page_size)
    page = st.number_input("페이지 선택", min_value=1, max_value=total_pages, value=1)
    start = (page - 1) * page_size
    end = start + page_size
    st.table(df.iloc[start:end])

st.title("검수자별 작업 목록 조회")

st.set_page_config(
    page_title="검수 조회 페이지",  # 브라우저 탭 이름
    page_icon="📋",                # 아이콘 (선택)
    layout="wide"
)

today = datetime.today().date().strftime('%Y%m%d')
# --- CSV 불러오기 ---
df = pd.read_csv(f"./data/{today}.csv")

# 검수자 ID 입력
worker_id = st.text_input("검수자 ID를 입력하세요:")

if worker_id:
    filtered_df, worker_name = get_checker_list(df, worker_id)

    if not filtered_df.empty:
        # 프로젝트 ID 별로 나누기
        project_ids = filtered_df['프로젝트ID'].unique()  # 프로젝트 ID 컬럼 이름 확인
        st.subheader(f"{worker_name}님의 작업 목록")
        paginate_dataframe(filtered_df, page_size=10)
    else:
        st.warning("해당 작업자의 작업 내역이 없습니다.")
