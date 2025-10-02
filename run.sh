cd cw_app
nohup streamlit run front/'메인.py' --server.address 0.0.0.0 --server.port 8501 &
nohup gunicorn -w 1 -b 0.0.0.0:5000 webhook_server:app \
    > /home/ubuntu/cw_app/webhook.log 2>&1 &

