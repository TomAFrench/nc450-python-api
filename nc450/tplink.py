import base64
import time

import requests

from const import (
    GET_CLOUD,
    GET_ETHERNET,
    GET_LED,
    GET_MOTION,
    GET_OSD,
    GET_PTZ,
    GET_SYSTEM_INFORMATION,
    GET_VIDEO,
    GET_WIFI,
    GET_WIFI_STATUS,
    LOGIN,
    LOGOUT,
    REBOOT,
    SCAN_WIFI,
    SET_ETHERNET,
    SET_LED,
    SET_MOTION,
    SET_OSD,
    SET_PTZ,
    SET_TURN,
    SET_WIFI,
)


class NC450:

    valid_directions = ["n", "nw", "w", "sw", "s", "se", "e", "ne", "c"]

    user_agent = r"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    headers = {"User-Agent": user_agent, "Accept": "text/plain"}

    def __init__(self, url, username="admin", password="admin"):
        self.url = url
        self.headers = NC450.headers
        self.token = None
        self.session = requests.session()

    def _build_endpoint_url(self, endpoint):
        return "http://" + self.url + "/" + endpoint

    def get(self, endpoint):
        url = self._build_endpoint_url(endpoint)
        response = self.session.get(url, headers=self.headers)
        return response

    def post(self, endpoint, data={}):
        url = self._build_endpoint_url(endpoint)
        data = {**data, "token": self.token}
        response = self.session.post(url, headers=self.headers, data=data)
        return response

    #### Basic functions ####

    def login(self, username="admin", password="admin"):
        login_data = {"Username": username, "Password": base64.b64encode(password)}
        response = self.post(LOGIN, login_data)
        print(response.json())
        self.token = response.json()["token"]

    def logout(self):
        response = self.post(LOGOUT)
        self.token = None

    def system_info(self):
        response = self.get(GET_SYSTEM_INFORMATION)
        return response.json()

    def reboot(self):
        self.post(REBOOT, {"token": self.token})

    #### Video ####

    def video(self):
        response = self.get(GET_VIDEO)
        return response.json()

    #### On-Screen Display ####

    def osd(self):
        response = self.get(GET_OSD)
        return response.json()

    def set_osd_options(self, osd_data):
        self.post(SET_OSD, data=osd_data)

    def set_osd_visibility(self, osd_state):
        osd_data = {"osd_enable": osd_state}
        self.set_osd_options(osd_data)

    def set_osd_text(self, text):
        new_osd_text = {"osd_info": base64.b64encode(text.encode("utf-8"))}
        self.set_osd_options(new_osd_text)

    def set_osd_text_color(self, color=16777215):
        new_osd_text = {"osd_color": color}
        self.set_osd_options(new_osd_text)

    #### Camera Motion ####
    def turn(self, direction, timestep=8, operation="start"):
        if direction not in NC450.valid_directions:
            raise ValueError("attempting to move camera in invalid direction.")
        else:
            turn_data = {"direction": direction, "operation": operation}
            self.post(SET_TURN, turn_data)
            if operation == "start" and direction is not "c":
                time.sleep(timestep)
                self.turn(direction, timestep, "stop")

    def velocity(self):
        response = self.get(GET_PTZ)
        return response.json()

    def set_velocity(self, velocity):
        if velocity not in [0, 1, 2]:
            raise ValueError("Attempting to set velocity to invalid value")
        velocity_data = {"value": velocity}
        self.post(SET_PTZ, velocity_data)

    #### Motion Detection ####

    def motion_detection(self):
        response = self.get(GET_MOTION)
        return response.json()

    def set_md_status(self, status):
        md_status = {"is_enable": status}
        self.post(SET_MOTION, md_status)

    def set_md_sensitivity(self, status):
        # add value validation
        md_status = {"precision": status}
        self.post(SET_MOTION, md_status)

    #### LED ####

    def led_status(self):
        response = self.get(GET_LED)
        return response.json()

    def set_led_status(self, status):
        if status not in [0, 1]:
            raise ValueError("Attempting to set led_status to invalid value")
        led_data = {"enable": status}
        response = self.post(SET_LED, led_data)

    #### WiFi ####

    def get_wifi_status(self):
        response = self.get(GET_WIFI_STATUS)
        return response.json()

    def scan_wifi(self):
        response = self.post(SCAN_WIFI)
        return response.json()

    def wifi_settings(self):
        response = self.get(GET_WIFI)
        return response.json()

    def set_wifi_settings(self, data):
        response = self.post(SET_WIFI, data)
        return response.json()

    #### Ethernet ####

    def ethernet_settings(self):
        response = self.get(GET_ETHERNET)
        return response.json()

    def set_ethernet_settings(self, data):
        response = self.post(SET_ETHERNET, data)
        return response.json()

    #### Notification ####

    def ftp_smtp_settings(self):
        response = self.get(GET_MOTION)
        return response.json()
