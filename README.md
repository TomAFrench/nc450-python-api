# TP-Link NC450 camera API for Python

This repository provides a Python API using the `requests` module for controlling TP-Link NC450 cameras.

Author: Tom French

## Installation

This API can be installed in a python3 virtual environment by the commands:

```bash
cd /path/to/repo
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
```

The API may then be imported as any other python module.


## Example

The API can be used to connect to an NC450 camera at the ip address `ip_addr` with login details `username` and `password`
```py
from tplink import NC450

camera = NC450(ip_addr, username, password)
camera.login()

#Turn camera to right for 2 seconds
camera.turn('e',2)

#Turn on camera led
camera.set_led_status(1)

#Recentre camera
camera.turn('c')

#logout
camera.logout()
```


## NC450 URLS

MJEG stream:
```
HD: http://[id_address]:8080/stream/video/mjpeg?resolution=HD&&Username=[username]&&Password=[password]

VGA: http://[id_address]:8080/stream/video/mjpeg?resolution=VGA&&Username=[username]&&Password=[password]
```
Snapshot:
```
HD: http://[id_address]:8080/stream/snapshot.jpg?resolution=HD&&Username=[username]&&Password=[password]&&attachment=1

VGA: http://[id_address]:8080/stream/snapshot.jpg?resolution=VGA&&Username=[username]&&Password=[password]&&attachment=1
```
SnapshotIE2:
```
HD: http://[id_address]:8080/stream/snapshot.jpg?resolution=HD&&Username=[username]&&Password=[password]&&tempid=[tempid],

VGA: http://[id_address]:8080/stream/snapshot.jpg?resolution=VGA&&Username=[username]&&Password=[password]&&tempid=[tempid]
```
