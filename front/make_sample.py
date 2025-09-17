import pandas as pd

# 예시 데이터 생성
data = [
    {"작업자ID": "worker1", "프로젝트ID": "P001", "프로젝트URL": "http://proj1.com", "작업상태": "진행중", "차수": 1},
    {"작업자ID": "worker1", "프로젝트ID": "P002", "프로젝트URL": "http://proj2.com", "작업상태": "완료", "차수": 2},
    {"작업자ID": "worker2", "프로젝트ID": "P003", "프로젝트URL": "http://proj3.com", "작업상태": "진행중", "차수": 1},
    {"작업자ID": "worker3", "프로젝트ID": "P004", "프로젝트URL": "http://proj4.com", "작업상태": "보류", "차수": 1},
]

df = pd.DataFrame(data)
df.to_csv("task_list.csv", index=False, encoding="utf-8-sig")
print("CSV 생성 완료")
