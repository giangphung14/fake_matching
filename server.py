import asyncio
import websockets
import random
import time
import msgpack
import math

open_price = random.randint(10000, 99999)
data = {
    "timestamp": math.floor(time.time()),
    "open": open_price,
    "close": open_price,
    "high": random.randint(10000, 99999),
    "low": random.randint(10000, 99999),
    "volume": random.randint(100, 999),
}

async def send_message(websocket, candle, time_range):
    count = 1
    while count < candle/time_range:
        encode_message = msgpack.packb(data);
        await websocket.send(encode_message)
        if count + 1 == candle/time_range:
            data["timestamp"] = math.floor(time.time())
        data["open"] = data["close"]
        data["close"] = random.randint(10000, 99999)
        data["high"] = random.randint(10000, 99999)
        data["close"] = random.randint(10000, 99999)
        data["volume"] = random.randint(100, 999)
        count += 1
        await asyncio.sleep(time_range)

async def set_candle(websocket, candle, time_range):
    while True:
        for _ in range(candle):
            await send_message(websocket, candle, time_range)
        await asyncio.sleep(candle)

async def main(candle, time_range):
    wrapper_set_candle = lambda websocket: set_candle(websocket, candle, time_range)
    async with websockets.serve(wrapper_set_candle, "localhost", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(60, 0.25))