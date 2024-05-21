import random
import time
import msgpack
import redis

r = redis.Redis(host="10.0.4.14", port=6379, db=0)

try:
    r.ping()
    print("Kết nối Redis thành công!")
except redis.ConnectionError:
    print("Kết nối Redis thất bại!")

open_price = random.randint(10000, 99999)

def send_message(data, candle):
    count = 1
    while data["t"] < time.time():
        encode_message = msgpack.packb(data)
        assert isinstance(encode_message, bytes)
        r.zadd("myzset", {encode_message: data["t"]})
        data["t"] = data["t"] + candle
        data["o"] = data["c"]
        data["c"] = random.randint(10000, 99999)
        data["h"] = random.randint(10000, 99999)
        data["l"] = random.randint(10000, 99999)
        data["v"] = random.randint(100, 999)
        count += 1
    print(count)

def main(t, candle):
    data = {
        "t": t,
        "o": open_price,
        "c": open_price,
        "h": random.randint(10000, 99999),
        "l": random.randint(10000, 99999),
        "v": random.randint(100, 999),
    }
    send_message(data, candle)
    print("Successfully!!")

if __name__ == "__main__":
    main(1640970000, 60)