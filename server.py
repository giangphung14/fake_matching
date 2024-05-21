import asyncio
import websockets
import random
import time
import msgpack
import math
import redis
import json

r = redis.Redis(host="10.0.4.14", port=6379, db=0)

try:
    r.ping()
    print("Kết nối Redis thành công!")
except redis.ConnectionError:
    print("Kết nối Redis thất bại!")

open_price = random.randint(30000, 80000)
data = {
    "t": math.floor(time.time()),
    "o": open_price,
    "c": open_price,
    "h": random.randint(80000, 99999),
    "l": random.randint(10000, 30000),
    "v": random.randint(100, 999),
}

r.zadd("myzset", {json.dumps(data): data["t"]})

async def send_message(websocket, candle, time_range):
    count = 1
    while count < candle/time_range:
        encode_message = msgpack.packb(data);
        await websocket.send(encode_message)
        if count + 1 == candle/time_range:
            data["t"] = math.floor(time.time())
        data["o"] = data["c"]
        data["c"] = random.randint(30000, 80000)
        data["h"] = random.randint(80000, 99999)
        data["l"] = random.randint(10000, 30000)
        data["v"] = random.randint(100, 999)
        count += 1
        await asyncio.sleep(time_range)

async def set_candle(websocket, path, candle, time_range):
    while True:
        for _ in range(candle):
            await send_message(websocket, candle, time_range)
        await asyncio.sleep(candle)

async def main(candle, time_range):
    async def handler(websocket, path):
        await set_candle(websocket, path, candle, time_range)
    
    async with websockets.serve(handler, "0.0.0.0", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(1, 0.25))