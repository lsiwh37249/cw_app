import streamlit as st
import pandas as pd
import os
import sys
import math
from datetime import datetime
import traceback
from back.back import get_checker_list, get_worker_list

def paginate_dataframe(df, page_size=10):
    total_pages = math.ceil(len(df) / page_size)
    page = st.number_input("페이지 선택", min_value=1, max_value=total_pages, value=1)
    start = (page - 1) * page_size
    end = start + page_size
    st.table(df.iloc[start:end])


st.set_page_config(
    page_title="검수 조회 페이지",  # 브라우저 탭 이름
    page_icon="📋",                # 아이콘 (선택)
    layout="wide"
)

today = datetime.today().date().strftime('%Y%m%d')
# --- CSV 불러오기 ---
df = pd.read_csv(f"./data/{today}.csv")

# 좌우 컬럼 생성 (비율 조정 가능)
col1, col2 = st.columns(2)

with col1:
    st.subheader("검수자별 작업 목록 조회")

    # 작업자 ID 입력
    worker_id = st.text_input("작업자 ID를 입력하세요:")
    # 에러/경고 표시용 플레이스홀더
    worker_msg = st.empty()
    # 결과를 그릴 컨테이너 (여기에 표/페이징 출력)
    worker_area = st.container()

    if worker_id:
        try:
            filtered_df, worker_name = get_worker_list(df, worker_id)
            worker_msg.empty()  # 이전 메시지 지우기
            if not filtered_df.empty:
                worker_area.subheader(f"{worker_name}님의 작업 목록")
                # paginate_dataframe가 내부적으로 st.*를 쓴다면 그대로 호출해도 이 컬럼 안에 표시됩니다.
                paginate_dataframe(filtered_df, page_size=10)
            else:
                worker_msg.warning("해당 작업자의 작업 내역이 없습니다.")
        except Exception as e:
            tb = traceback.format_exc()
            worker_msg.error(f"에러 발생: {e}")
            # 상세 스택트레이스는 코드 블록으로 보여주기
            worker_area.text("상세 에러:")
            worker_area.code(tb)

with col2:
    st.subheader("검수자 작업 목록")
    # 검수자 ID 입력
    checker_id = st.text_input("검수자 ID를 입력하세요:")
    checker_msg = st.empty()
    checker_area = st.container()

    if checker_id:
        try:
            filtered_df, checker_name = get_checker_list(df, checker_id)
            checker_msg.empty()
            if not filtered_df.empty:
                checker_area.subheader(f"{checker_name}님의 작업 목록")
                paginate_dataframe(filtered_df, page_size=10)
            else:
                checker_msg.warning("해당 작업자의 작업 내역이 없습니다.")
        except Exception as e:
            tb = traceback.format_exc()
            checker_msg.error(f"에러 발생: {e}")
            checker_area.text("상세 에러:")
            checker_area.code(tb)
