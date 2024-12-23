import asyncio
import cv2
import io
import numpy
import sys
import websockets

from PIL import Image

'''
    https://qiita.com/NegishiS/items/478055cb632cb02bff75
    ※そのままだと動かなかったのでいじってます
'''

class WebSocketsServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.cap = None
        # self.width = 640
        # self.height = 480
        self.width = 1280
        self.height = 720

        self.isJpeg = True

    def _cv2pil(self, image):
        new_image = image.copy()
        if new_image.ndim == 2:  # mono
            # not supported
            return None
        elif new_image.shape[2] == 3:  # RGB
            if self.isJpeg:
                img_fmt = cv2.COLOR_BGR2RGB
            else:
                img_fmt = cv2.COLOR_BGR2RGBA
        elif new_image.shape[2] == 4:  # RGBA
            if self.isJpeg:
                img_fmt = cv2.COLOR_BGRA2RGB
            else:
                img_fmt = cv2.COLOR_BGRA2RGBA

        new_image = cv2.cvtColor(new_image, img_fmt)
        new_image = Image.fromarray(new_image)
        return new_image

    #async def _handler(self, websocket, path):
    async def _handler(self, websocket):
        # print("start streaming... {path}")
        recv_data = await websocket.recv()

        self.cap = cv2.VideoCapture(r'rtsp://admin:qu64zQrc@192.168.120.32/Streaming/Channels/1')
        if not self.cap.isOpened():
            print("cannot connect RTSP server.")
            sys.exit(1)

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                continue

            # w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            # h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # print (f"capture w:{w}, h:{h}")

            image = self._cv2pil(cv2.resize(frame, (self.width, self.height)))

            if self.isJpeg:
                with io.BytesIO() as image_temp:
                    image.save(image_temp, format="jpeg", quality=80)
                    await websocket.send(image_temp.getvalue())
            else:
                image_np = numpy.array(image)
                await websocket.send(image_np.tobytes())

    async def run(self):
        async with websockets.serve(self._handler, self.address, self.port):
            print(f"Server running at ws://{self.address}:{self.port}")
            await asyncio.Future()  # run forever

if __name__ == '__main__':
    address = '0.0.0.0'
    port = 60000
    wss = WebSocketsServer(address, port)

    asyncio.run(wss.run())
