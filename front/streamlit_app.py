import streamlit as st
import pandas as pd
import os
import sys

from back.back import add_module, get_worker_list

# CSV 불러오기
df = pd.read_csv("./data/250917.csv")

st.title("작업자별 작업 목록 조회")

# 작업자 ID 입력
worker_id = st.text_input("작업자 ID를 입력하세요:")

if worker_id:

    filtered_df, worker_name = get_worker_list(df, worker_id)

    if not filtered_df.empty:
        st.subheader(f"{worker_name}님의 작업 목록")
        # 프로젝트 ID 별로 나누기
        project_ids = filtered_df['프로젝트ID'].unique()  # 프로젝트 ID 컬럼 이름 확인
        for pid in project_ids:
            project_df = filtered_df[filtered_df['프로젝트ID'] == pid]
            st.table(project_df)
    else:
        st.warning("해당 작업자의 작업 내역이 없습니다.")

# 예시 218121
