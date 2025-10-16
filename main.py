from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import asyncio

app = FastAPI()

DB_PATH = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            client_ip TEXT,
            kerberos TEXT,
            counter INTEGER,
            osname TEXT,
            key TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()
lock = asyncio.Lock()

class Packet(BaseModel):
    kerberos: str
    counter: int
    osname: str
    key: str

@app.post("/log/")
async def log(packet: Packet, request: Request):
    client_ip = request.client.host
    timestamp = datetime.utcnow().isoformat()

    async with lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (timestamp, client_ip, kerberos, counter, osname, key)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, client_ip, packet.kerberos, packet.counter, packet.osname, packet.key))
        conn.commit()
        conn.close()

    return {"status": "ok", "ip": client_ip, "logged_at": timestamp}
