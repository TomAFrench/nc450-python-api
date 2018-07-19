import requests
import base64
import time

class NC450():

    end_points = {'LOGIN': 'login.fcgi', 'LOGOUT':'logout.fcgi',
                'GET_SYSTEM_INFORMATION': 'getsysinfo.fcgi',
                'GET_LED': 'ledgetting.fcgi','SET_LED': 'ledsetting.fcgi','GET_CLOUD': 'get_cloud.fcgi',
                'GET_VIDEO': 'getvideosetting.fcgi', 'GET_OSD':'getosdandtimedisplay.fcgi',
                'SET_OSD':'setosdandtimedisplay.fcgi', 'SET_TURN': 'setTurnDirection.fcgi',
                'GET_MOTION': 'mdconf_get.fcgi',
                'GET_WIFI_STATUS': 'wireless_status.fcgi', 'SCAN_WIFI': 'wireless_scan.fcgi',
                'GET_WIFI': 'wireless_get.fcgi', 'SET_WIFI': 'wireless_set.fcgi',
                'GET_ETHERNET': 'netconf_get.fcgi',  'SET_ETHERNET': 'netconf_set.fcgi',
                'GET_PTZ': 'getPtzVelocity.fcgi',  'SET_PTZ': 'setPtzVelocity.fcgi',
                'REBOOT': 'reboot.fcgi'}

    request_type = {'LOGIN': 'post','LOGOUT': 'post', 'GET_SYSTEM_INFORMATION': 'post',
                    'GET_LED': 'get','SET_LED': 'post',
                    'GET_CLOUD': 'get', 'GET_VIDEO': 'get',
                    'GET_OSD':'get', 'SET_OSD':'post',
                    'SET_TURN': 'post', 'GET_MOTION': 'get',
                    'GET_WIFI_STATUS': 'get',
                    'SCAN_WIFI': 'post',  'GET_WIFI': 'get',
                    'SET_WIFI': 'post',
                    'GET_ETHERNET': 'get',  'SET_ETHERNET': 'post',
                    'GET_PTZ': 'post',  'SET_PTZ': 'post',
                    'REBOOT': 'post'}

    valid_directions = ['n', 'nw', 'w', 'sw', 's', 'se', 'e', 'ne', 'c']

    user_agent = r'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent, 'Accept': "text/plain"}

    def __init__(self, url, username='admin', password='admin'):
        self.url = url
        self.headers = NC450.headers
        self.params = {'Username': username, 'Password': base64.b64encode(password)}
        self.token = None
        self.session = requests.session()

    def call(self, endpoint, data={}):
        url = 'http://'+ self.url +'/'+ NC450.end_points[endpoint]
        #print(url)
        #print()
        #print(data)
        if NC450.request_type[endpoint] == 'get':
            #print('get')
            response = self.session.get(url, headers=self.headers, data=data)
        elif NC450.request_type[endpoint] == 'post':
            #print('post')
            data = {**data, 'token': self.token}
            response = self.session.post(url, headers=self.headers, data=data)
        else:
            raise ValueError('No valid action for this endpoint')
        return response

    #### Basic functions ####

    def login(self):
        response = self.call('LOGIN', self.params)
        print(response.json())
        self.token = response.json()['token']

    def logout(self):
        response = self.call('LOGOUT')
        self.token = None


    def system_info(self):
        response = self.call('GET_SYSTEM_INFORMATION')
        return response.json()

    def reboot(self):
       self.call('REBOOT',{'token':self.token})

    #### Video ####

    #@property
    def video(self):
        response = self.call('GET_VIDEO')
        return response.json()

    #### On-Screen Display ####

    def osd(self):
        response = self.call('GET_OSD')
        return response.json()

    def set_osd_options(self, osd_data):
        self.call('SET_OSD', osd_data)

    def set_osd_visibility(self, osd_state):
        osd_data = {'osd_enable': osd_state}
        self.set_osd_options(osd_data)

    def set_osd_text(self, text):
        new_osd_text = {'osd_info': base64.b64encode(text.encode('utf-8'))}
        self.set_osd_options(new_osd_text)

    #### Camera Motion ####
    def turn(self, direction, timestep = 8, operation = 'start'):
        if direction not in NC450.valid_directions:
            raise ValueError('attempting to move camera in invalid direction.')
        else:
            turn_data = {'direction': direction, 'operation': operation}
            self.call('SET_TURN', turn_data)
            if operation == 'start' and direction is not 'c':
                time.sleep(timestep)
                self.turn(direction, timestep, 'stop')

    #@property
    def velocity(self):
        response = self.call('GET_PTZ')
        return response.json()

    #@velocity.setter
    def set_velocity(self, velocity):
        if velocity not in [0,1,2]:
            raise ValueError('Attempting to set velocity to invalid value')
        velocity_data = {'value': velocity}
        self.call('SET_PTZ', velocity_data)

    #### Motion Detection ####

    def motion_detection(self):
        response = self.call('GET_MOTION')
        return response.json()

    #### LED ####

    #@property
    def led_status(self):
        response = self.call('GET_LED')
        return response.json()

    #@led_status.setter
    def set_led_status(self, status):
        if status not in [0,1]:
            raise ValueError('Attempting to set led_status to invalid value')
        led_data = {"enable": status}
        response = self.call('SET_LED', led_data)

    #### WiFi ####

    def get_wifi_status(self):
        response = self.call('GET_WIFI_STATUS')
        return response.json()

    def scan_wifi(self):
        response = self.call('SCAN_WIFI')
        return response.json()

    #@property
    def wifi_settings(self):
        response = self.call('GET_WIFI')
        return response.json()

    #@wifi_settings.setter
    def set_wifi_settings(self, data):
        response = self.call('SET_WIFI', data)
        return response.json()

    #### Ethernet ####

    #@property
    def ethernet_settings(self):
        response = self.call('GET_ETHERNET')
        return response.json()

    #@ethernet_settings.setter
    def set_ethernet_settings(self, data):
        response = self.call('SET_ETHERNET', data)
        return response.json()

    #### Notification ####

    def ftp_smtp_settings(self):
        response = self.call('GET_MOTION')
        return response.json()
