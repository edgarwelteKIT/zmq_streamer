# ZMQ Streamer

## ZMQ Image Streamer

This script captures video from a webcam and streams JPEG-compressed frames over a ZeroMQ PUB socket.

## Requirements
- Python 3.6+
- OpenCV
- pyzmq

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Usage
```bash
python zmq_image_streamer.py
```
## Configuration
You can configure the following parameters in the script:
- `cam_id`: The index of the camera to use (default is 0).
- `port`: The port number for the ZeroMQ PUB socket (default is 5555).
- `fps`: The frames per second to capture (default is 30).


## Example
```bash
python zmq_image_streamer.py --cam_id 1 --fps 30
```
