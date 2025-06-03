#!/usr/bin/env python3

import zmq
import cv2
import time
import sys
import argparse
import numpy as np

from pyorbbecsdk import *

def frame_to_bgr_image(frame: VideoFrame):
    width = frame.get_width()
    height = frame.get_height()
    color_format = frame.get_format()
    data = np.asanyarray(frame.get_data())
    image = np.zeros((height, width, 3), dtype=np.uint8)
    if color_format == OBFormat.RGB:
        image = np.resize(data, (height, width, 3))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif color_format == OBFormat.BGR:
        image = np.resize(data, (height, width, 3))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif color_format == OBFormat.YUYV:
        image = np.resize(data, (height, width, 2))
        image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_YUYV)
    elif color_format == OBFormat.MJPG:
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    elif color_format == OBFormat.I420:
        image = i420_to_bgr(data, width, height)
    elif color_format == OBFormat.NV12:
        image = nv12_to_bgr(data, width, height)
    elif color_format == OBFormat.NV21:
        image = nv21_to_bgr(data, width, height)
    elif color_format == OBFormat.UYVY:
        image = np.resize(data, (height, width, 2))
        image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_UYVY)
    else:
        print("Unsupported color format: {}".format(color_format))
        return None
    return image

class ZMQImageOrbbecStreamer:
    def __init__(self, port=5555, fps=30):
        self.port = port
        self.fps = fps

        # Initialize ZMQ
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{self.port}")
        print(f"[Streamer] ZMQ publisher bound to tcp://*:{self.port}")

        # Setup Orbbec camera pipeline
        self.pipeline = Pipeline()
        self.config = Config()

        try:
            profile_list = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            try:
                color_profile = profile_list.get_video_stream_profile(640, 0, OBFormat.RGB, self.fps)
            except OBError as e:
                print(e)
                color_profile = profile_list.get_default_video_stream_profile()
                print("[Streamer] Using default color profile:", color_profile)
            self.config.enable_stream(color_profile)
            self.pipeline.start(self.config)
            print("[Streamer] Orbbec pipeline started")
        except Exception as e:
            print(f"[Error] Failed to initialize Orbbec camera: {e}")
            sys.exit(1)

    def stream(self):
        try:
            while True:
                start_time = time.time()
                frames = self.pipeline.wait_for_frames(100)
                if frames is None:
                    continue

                color_frame = frames.get_color_frame()
                if color_frame is None:
                    continue

                color_image = frame_to_bgr_image(color_frame)
                if color_image is None:
                    continue

                success, jpeg = cv2.imencode('.jpg', color_image)
                if success:
                    self.socket.send(jpeg.tobytes())

                # FPS Throttling
                elapsed_time = time.time() - start_time
                sleep_time = max(0, (1.0 / self.fps) - elapsed_time)
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("[Streamer] Interrupted by user. Exiting...")
        finally:
            self.cleanup()

    def cleanup(self):
        self.pipeline.stop()
        self.socket.close()
        self.context.term()
        print("[Streamer] Shutdown complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ZMQ Orbbec Image Streamer")
    parser.add_argument('--port', type=int, default=5555, help='Port to bind the ZMQ publisher')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second to stream')
    args = parser.parse_args()

    streamer = ZMQImageOrbbecStreamer(port=args.port, fps=args.fps)
    streamer.stream()
