import asyncio
import websockets
import msgpack

async def receive_messages():
    async with websockets.connect('ws://10.0.4.13:8001') as websocket:
        while True:
            message = await websocket.recv()
            decode_message = msgpack.unpackb(message);
            print(decode_message)

async def main():
    await receive_messages()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
