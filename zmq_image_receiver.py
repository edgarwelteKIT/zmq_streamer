import time
import zmq
import cv2
import numpy as np
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="ZMQ Image Receiver")
    parser.add_argument('--ip', type=str, default='localhost', help='IP address of the sender')
    parser.add_argument('--port', type=int, default=5555, help='Port number')
    args = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{args.ip}:{args.port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    print(f"[Receiver] Connected to stream at tcp://{args.ip}:{args.port}")

    last_time = time.time()
    frames = []

    while True:
        msg = socket.recv()
        img = cv2.imdecode(np.frombuffer(msg, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            frames.append(img)
            if len(frames) > 10:
                frames.pop(0)
            current_time = time.time()
            diff = current_time - last_time
            last_time = current_time
            if diff > 0:
                print(f"FPS: {1/diff:.2f}")

            cv2.imshow("Live Stream", img)
            img = np.transpose(img, (2, 0, 1))

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
