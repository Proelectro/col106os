#!/usr/bin/env python3
"""
Hard-coded stress test for FastAPI log endpoint.
Sends concurrent POST requests to http://10.17.5.8:8000/log/
"""

import asyncio
import aiohttp
import random
import platform
import time
import statistics
from datetime import datetime

URL = "http://10.17.5.8:8000/log/"
CONCURRENCY = 200      # number of concurrent requests
TOTAL_REQUESTS = 2000   # total requests to send
TIMEOUT_SEC = 10

def now_ts():
    return datetime.utcnow().isoformat() + "Z"

async def send_one(session, payload, sem, timeout):
    async with sem:
        start = time.perf_counter()
        try:
            async with session.post(URL, json=payload, timeout=timeout) as resp:
                text = await resp.text()
                elapsed = (time.perf_counter() - start) * 1000.0  # ms
                return {"status": resp.status, "elapsed_ms": elapsed, "text": text}
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000.0
            return {"status": None, "elapsed_ms": elapsed, "error": str(e)}

async def run_load():
    sem = asyncio.Semaphore(CONCURRENCY)
    connector = aiohttp.TCPConnector(limit=0, force_close=True)
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=TIMEOUT_SEC, sock_read=TIMEOUT_SEC)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for i in range(TOTAL_REQUESTS):
            payload = {
                "kerberos": f"stress-agent-{i}",
                "counter": i,
                "osname": "stress-test2",
                "key": f"TESTKEY-{i}"
            }
            tasks.append(asyncio.create_task(send_one(session, payload, sem, timeout)))
        results = await asyncio.gather(*tasks)
    return results

def summarize(results):
    total = len(results)
    successes = sum(1 for r in results if r.get("status") and 200 <= r["status"] < 300)
    failures = total - successes
    latencies = [r["elapsed_ms"] for r in results if r.get("elapsed_ms") is not None]
    avg = statistics.mean(latencies) if latencies else float("nan")
    p95 = (sorted(latencies)[int(0.95*len(latencies))-1] if latencies else float("nan"))
    p99 = (sorted(latencies)[int(0.99*len(latencies))-1] if latencies else float("nan"))

    print("\n=== Stress Test Summary ===")
    print(f"Total requests : {total}")
    print(f"Successes      : {successes}")
    print(f"Failures       : {failures}")
    print(f"Avg latency ms : {avg:.2f}")
    print(f"P95 latency ms : {p95:.2f}")
    print(f"P99 latency ms : {p99:.2f}")

    if failures:
        print("\nSample failures (up to 5):")
        shown = 0
        for r in results:
            if not (r.get("status") and 200 <= r["status"] < 300):
                print(f"  status={r.get('status')} elapsed={r.get('elapsed_ms'):.1f}ms err={r.get('error', r.get('text',''))}")
                shown += 1
                if shown >= 5:
                    break

def main():
    print(f"[{now_ts()}] Starting stress test for {URL}")
    print(f"→ Concurrency: {CONCURRENCY}, Total: {TOTAL_REQUESTS}, Timeout: {TIMEOUT_SEC}s")

    start = time.perf_counter()
    results = asyncio.run(run_load())
    duration = time.perf_counter() - start

    print(f"[{now_ts()}] Completed in {duration:.2f}s")
    summarize(results)

if __name__ == "__main__":
    main()
