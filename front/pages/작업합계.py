import pandas as pd
import streamlit as st
from datetime import datetime
import pandasql as ps  # pandasql 사용

# --- Streamlit 페이지 설정 ---
st.set_page_config(
    page_title="작업자/검수자 통계 현황",
    page_icon="📋",
    layout="wide"
)

# --- CSV 불러오기 ---
df = pd.read_csv("./data/250917.csv")

# 오늘 날짜
today = datetime.today().date()

st.subheader(f"{today} 오전 8시 30분까지 작업자별 통계")

# --- SQL 쿼리: 작업자 집계 ---
worker_query = f"""
SELECT
    "Worker ID",
    "작업자 닉네임",
    COUNT("데이터 ID") AS "작업 수량",
    SUM("유효 오브젝트 수") AS "유효 오브젝트_수 합계"
FROM df
WHERE "작업 종료일" IS NOT NULL
  AND DATE("작업 종료일") <= DATE('{today}')
GROUP BY "Worker ID", "작업자 닉네임"
ORDER BY "Worker ID"
"""

worker_result = ps.sqldf(worker_query, locals())

# --- SQL 쿼리: 검수자 집계 ---
checker_query = f"""
SELECT
    "Checker ID",
    "검수자 닉네임",
    COUNT("데이터 ID") AS "작업 수량",
    SUM("유효 오브젝트 수") AS "유효 오브젝트_수 합계"
FROM df
WHERE "검수 종료일" IS NOT NULL
  AND DATE("검수 종료일") <= DATE('{today}')
GROUP BY "Checker ID", "검수자 닉네임"
ORDER BY "Checker ID"
"""

checker_result = ps.sqldf(checker_query, locals())

# --- Streamlit UI 표시 ---
st.subheader("작업자 집계")
st.dataframe(worker_result)

st.subheader("검수자 집계")
st.dataframe(checker_result)
