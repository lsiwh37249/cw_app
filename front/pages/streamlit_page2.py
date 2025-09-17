# preset 데이터 csv 불러오기
import pandas as pd
import os
import sys
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

df = pd.read_csv("/home/kim/code/gcs/data/combined/combined.csv")

# url 입력
input = st.text_input("URL을 입력하세요:")

# url 입력 후 버튼 클릭
if st.button("프리셋 데이터 조회"):

    # 사용할 URL 컬럼 자동 선택
    url_col_candidates = ["dataID"]
    chosen_col = None
    for c in url_col_candidates:
        if c in df.columns:
            chosen_col = c
            break  # 첫 번째 일치 컬럼을 찾으면 바로 종료
    
    if chosen_col:
        df_filtered = df[df[chosen_col] == int(input)]
        st.dataframe(df_filtered)
    else:
        st.error("URL 컬럼을 찾을 수 없습니다.")

