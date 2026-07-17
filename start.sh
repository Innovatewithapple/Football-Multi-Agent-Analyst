#!/bin/sh

echo "Starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

sleep 5

echo "Checking FastAPI..."
curl http://127.0.0.1:8000/docs || echo "FastAPI not running"

echo "Starting Streamlit..."
streamlit run streamlit_app.py \
    --server.port=${PORT:-7860} \
    --server.address=0.0.0.0