sudo apt update
sudo apt install python3-pip -y
python3 -m pip install --upgrade pip
python3 -m pip install streamlit
cd cw_app
nohup  streamlit run front/streamlit_app.py --server.address 0.0.0.0 --server.port 8501 
