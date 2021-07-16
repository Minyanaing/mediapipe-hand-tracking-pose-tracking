# MediaPipe tutorials
This repo contains simple project files using [MediaPipe](https://google.github.io/mediapipe/)

Customized modules for hand tracking using **MediaPipe** is located in `./Module` folder.

The required packages can be installed:
- pip install opencv-python
- pip install mediapipe

### Volume Control with Hand
Controlling the volume of the system using hand-landmarks. To control the system volume of the Ubuntu from the python script, we will need [alsaaudio](https://pypi.org/project/pyalsaaudio/). 

*If you are using windows, you can use [pycaw](https://github.com/AndreMiras/pycaw) and some lines of code need to be changed*. 

The test code can be run using:
```
python3 Volume_control.py
```