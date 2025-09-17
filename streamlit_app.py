import streamlit as st
import pandas as pd

# CSV 불러오기
df = pd.read_csv("task_list.csv")

st.title("작업자별 작업 목록 조회")

# 작업자 ID 입력
worker_id = st.text_input("작업자 ID를 입력하세요:")

if worker_id:
    filtered_df = df[df["작업자ID"] == worker_id]
    
    if not filtered_df.empty:
        st.subheader(f"{worker_id}님의 작업 목록")
        st.table(filtered_df)
    else:
        st.warning("해당 작업자의 작업 내역이 없습니다.")
