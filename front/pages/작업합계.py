import pandas as pd
import streamlit as st
from datetime import datetime
import pandasql as ps  # pandasql 사용
import io
from io import BytesIO
import xlsxwriter
import duckdb

# --- Streamlit 페이지 설정 ---
st.set_page_config(
    page_title="작업자/검수자 통계 현황",
    page_icon="📋",
    layout="wide"
)

today = datetime.today().date().strftime('%Y%m%d')
# --- CSV 불러오기 ---
df = pd.read_csv(f"./data/{today}.csv")

# 오늘 날짜
today = datetime.today().date()

st.subheader(f"{today} 오전 8시 30분까지 작업자별 통계")

# --- SQL 쿼리: 작업자 집계 ---
worker_query = f"""
SELECT
    "Worker ID",
    "작업자 닉네임",
    COUNT("데이터 ID") AS "작업 수량",
    COUNT(CASE WHEN "작업불가여부" = 'Y' THEN 1 END) AS "작업 불가 여부 합계",
    COUNT("데이터 ID") - COUNT(CASE WHEN "작업불가여부" = 'Y' THEN 1 END) AS "인정 작업 수량",
    SUM("유효 오브젝트 수") AS "유효 오브젝트_수 합계",

FROM df
WHERE "작업 종료일" IS NOT NULL
  AND DATE("작업 종료일") <= DATE('{today}')
GROUP BY "Worker ID", "작업자 닉네임"
ORDER BY "Worker ID"
"""
worker_result = duckdb.query(worker_query).to_df()


# --- SQL 쿼리: 검수자 집계 ---
checker_query = f"""
SELECT
    "Checker ID",
    "검수자 닉네임",
    COUNT("데이터 ID") AS "작업 수량",
    COUNT(CASE WHEN "작업불가여부" = 'Y' THEN 1 END) AS "작업 불가 여부 합계",
    COUNT("데이터 ID") - COUNT(CASE WHEN "작업불가여부" = 'Y' THEN 1 END) AS "인정 작업 수량",
    SUM("유효 오브젝트 수") AS "유효 오브젝트_수 합계",
FROM df
WHERE "검수 종료일" IS NOT NULL
  AND DATE("검수 종료일") <= DATE('{today}')
GROUP BY "Checker ID", "검수자 닉네임"
ORDER BY "Checker ID"
"""

checker_result = duckdb.query(checker_query).to_df()


# --- Excel 변환 함수 ---
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="작업자통계")
    processed_data = output.getvalue()
    return processed_data

worker_excel = convert_df_to_excel(worker_result)
checker_excel = convert_df_to_excel(checker_result)

# --- Streamlit UI 표시 ---
st.subheader("작업자 집계")

st.download_button(
    label="작업자 통계 엑셀 다운로드",
    data=worker_excel,
    file_name=f"작업자 통계_{today}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.dataframe(worker_result)

st.subheader("검수자 집계")

st.download_button(
    label="검수자 통계 엑셀 다운로드",
    data=checker_excel,
    file_name=f"검수자_통계_{today}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.dataframe(checker_result)

