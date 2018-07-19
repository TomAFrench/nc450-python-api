# TP-Link NC450 camera API for Python

This package provides a Python API class using the requests module for controlling TP-Link NC450 cameras.

Author: Tom French

---
## Installation

This API can be installed in a python3 virtual environment by the commands:

```bash
cd /path/to/repo
python3 -m venv .
pip3 install -r requirements.txt
```

The API may then be import as any other python module.

---

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


---

## NC450 URLS

MJEG stream:
```
#imgsrcHD
http://[id_address]:8080/stream/video/mjpeg?resolution=HD&&Username=[username]&&Password=[password]
#imgsrcVGA
http://[id_address]:8080/stream/video/mjpeg?resolution=VGA&&Username=[username]&&Password=[password]
```
Snapshot:
```
#High Definition
http://[id_address]:8080/stream/snapshot.jpg?resolution=HD&&Username=[username]&&Password=[password]+"&&attachment=1
#VGA
http://[id_address]:8080/stream/snapshot.jpg?resolution=VGA&&Username=[username]&&Password=[password]+"&&attachment=1
```
SnapshotIE2:
```
snapshotIE2HD:
http://[id_address]:8080/stream/snapshot.jpg?resolution=HD&&Username=[username]&&Password=[password]&&tempid="+Math.random(),
snapshotIE2VGA:
http://[id_address]:8080/stream/snapshot.jpg?resolution=VGA&&Username=[username]&&Password=[password]&&tempid="+Math.random(),
```
