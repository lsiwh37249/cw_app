import pandas as pd
import os
import sys

def add_module(data):
    print("module test")
    return data

def get_worker_list(df, worker_id):
    filtered_df = df[df["Worker ID"] == int(worker_id)]
    filtered_df = filtered_df[["Worker ID", "작업자 닉네임", "검수자 닉네임", "프로젝트ID", "CO 모니터링 URL","작업 종료일"]]
    filtered_df["프로젝트ID"] = filtered_df["프로젝트ID"].astype(int)
    filtered_df["Worker ID"] = filtered_df["Worker ID"].astype(int)
    worker_name = filtered_df["작업자 닉네임"].iloc[0]
    filtered_df = filtered_df.sort_values(by="작업 종료일", ascending=False)
    filtered_df = filtered_df[["Worker ID", "작업자 닉네임", "검수자 닉네임", "프로젝트ID", "CO 모니터링 URL"]]
    return filtered_df, worker_name

def get_checker_list(df, checker_id):
    filtered_df = df[df["Checker ID"] == int(checker_id)]
    filtered_df = filtered_df[["Checker ID", "작업자 닉네임", "검수자 닉네임", "프로젝트ID", "CO 모니터링 URL","작업 종료일"]]
    filtered_df["프로젝트ID"] = filtered_df["프로젝트ID"].astype(int)
    filtered_df["Checker ID"] = filtered_df["Checker ID"].astype(int)
    worker_name = filtered_df["검수자 닉네임"].iloc[0]
    filtered_df = filtered_df.sort_values(by="작업 종료일", ascending=False)
    filtered_df = filtered_df[["Checker ID", "작업자 닉네임", "검수자 닉네임", "프로젝트ID", "CO 모니터링 URL"]]
    return filtered_df, worker_name
