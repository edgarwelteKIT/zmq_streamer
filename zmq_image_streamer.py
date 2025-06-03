#!/usr/bin/env python3

import zmq
import cv2
import time
import sys
import argparse

class ZMQImageStreamer:
    def __init__(self, port=5555, cam_id=2, fps=30):
        self.port = port
        self.cam_id = cam_id
        self.fps = fps

        # Initialize ZeroMQ publisher
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{self.port}")
        print(f"[Streamer] ZMQ publisher bound to tcp://*:{self.port}")

        # OpenCV camera
        self.cap = cv2.VideoCapture(self.cam_id)
        if not self.cap.isOpened():
            print(f"[Error] Failed to open camera with index {self.cam_id}")
            sys.exit(1)

        print("[Streamer] Started, broadcasting frames...")

    def stream(self):
        try:
            while True:
                start_time = time.time()
                ret, frame = self.cap.read()
                if not ret:
                    continue

                # Compress as JPEG
                success, jpeg = cv2.imencode('.jpg', frame)
                if success:
                    self.socket.send(jpeg.tobytes())

                # Throttle to desired FPS
                elapsed_time = time.time() - start_time
                sleep_time = max(0, (1.0 / self.fps) - elapsed_time)
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("[Streamer] Interrupted by user. Exiting...")
        finally:
            self.cleanup()

    def cleanup(self):
        self.cap.release()
        self.socket.close()
        self.context.term()
        print("[Streamer] Shutdown complete.")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="ZMQ Image Streamer")
    parser.add_argument('--port', type=int, default=5555, help='Port to bind the ZMQ publisher')
    parser.add_argument('--cam_id', type=int, default=0, help='Camera index for OpenCV')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second to stream')
    args = parser.parse_args()

    streamer = ZMQImageStreamer(port=args.port, cam_id=args.cam_id, fps=args.fps)
    streamer.stream()
