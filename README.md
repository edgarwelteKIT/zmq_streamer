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

To use the orbbec script (which uses the orbbec SDK to capture images from an Orbbec camera), you will need to install the orbbec SDK and its Python bindings. Run the following command to install the required packages:
```bash
./install_orbbecsdk.sh
```

## Usage

Start the script to begin streaming video frames:
```bash
python zmq_image_streamer.py
```

Start an example script to receive and display the streamed images:
```bash
python zmq_image_receiver.py --ip=localhost --port=5555
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