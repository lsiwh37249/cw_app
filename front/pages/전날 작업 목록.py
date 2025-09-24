import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import pandasql as ps  # pandasql 사용
import io
from io import BytesIO
import xlsxwriter
import duckdb

# --- Streamlit 페이지 설정 ---
st.set_page_config(
    page_title="전날 작업 목록",
    page_icon="📋",
    layout="wide"
)

# --- CSV 불러오기 ---
df = pd.read_csv("./data/250917.csv")
# 오늘 날짜
today = datetime.today().date()
yesterday = today - timedelta(days=1)
# --- SQL 쿼리: 작업자 집계 ---
query = f"""
SELECT
    "프로젝트ID",
    "데이터 ID",
    "작업자 닉네임",
    "검수자 닉네임",
    "검수 종료일",
    "CO 모니터링 URL"
FROM df
WHERE "검수 종료일" IS NOT NULL
  AND DATE("검수 종료일") <= DATE('{yesterday}')
  AND DATE("검수 종료일") >= DATE('{yesterday}')
"""
result = duckdb.query(query).to_df()

# --- Excel 변환 함수 ---
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="작업자통계")
    processed_data = output.getvalue()
    return processed_data

excel_result = convert_df_to_excel(result)


# --- Streamlit UI 표시 ---
st.subheader("전날 작업 목록")

st.download_button(
    label=" 엑셀 다운로드",
    data=excel_result,
    file_name=f"통계_{yesterday}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.dataframe(result)


