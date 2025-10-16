build cmd from client
```
g++ client.cpp -o client -lcurl -std=c++17
./client # for continuous logging
```

install commands for server
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

for running server
```
gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000
```

server ip and port
10.17.5.8:8000