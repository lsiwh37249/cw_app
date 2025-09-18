import pandas as pd
import os
import sys

def add_module(data):
    print("module test")
    return data

def get_worker_list(df, worker_id):
    filtered_df = df[df["Worker ID"] == int(worker_id)]
    filtered_df = filtered_df[["Worker ID", "작업자 닉네임", "프로젝트ID", "CO 모니터링 URL"]]
    filtered_df["프로젝트ID"] = filtered_df["프로젝트ID"].astype(int)
    filtered_df["Worker ID"] = filtered_df["Worker ID"].astype(int)
    worker_name = filtered_df["작업자 닉네임"].iloc[0]
    return filtered_df, worker_name
