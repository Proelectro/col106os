python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000