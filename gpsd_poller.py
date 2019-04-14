import threading
from gps import *
import redis
import configparser
import os


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
gps_config = configparser.ConfigParser()

gps_config.read("{}/config/gps.ini".format(WORKING_DIR))
GPS_TIMEOUT = float(gps_config.get("gps", "timeout"))
DEF_LAT = gps_config.getfloat("gps", "default_lat")
DEF_LNG = gps_config.getfloat("gps", "default_lng")

gps_data_default = {
    'latitude': DEF_LAT,
    'longitude': DEF_LNG,
    'altitude': 0,
    'utc': '',
    'speed': 0,
    'distance': 0,
    'azimuth': 0,
    'message': 'switched off'
}

REDIS_HOST = gps_config.get("redis", "host")
REDIS_PORT = gps_config.getint("redis", "port")
REDIS_PASSWD = gps_config.get("redis", "password")
REDIS_EXP = gps_config.getint("redis", "expiration")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

gpsd = None


class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()


def gps_switch():
    '''
    Function check the configuration file i.e. the need for
    GPS data
    :return: True if GPS data is needed/expected or False otherwise
    '''
    gps_config.read("{}/config/gps.ini".format(WORKING_DIR))
    GPS_ON = gps_config.getboolean("gps", "switch")
    return GPS_ON


if __name__ == '__main__':
    gps_data = gps_data_default
    try:
        gpsp = GpsPoller()
        try:
            gpsp.start()
            while True:
                gps_data = (
                    gps_data_default,
                    dict(
                        latitude=gpsd.fix.latitude,
                        longitude=gpsd.fix.longitude,
                        altitude=gpsd.fix.altitude,
                        utc=gpsd.utc,
                        speed=gpsd.fix.speed,
                        message='ok'
                    ))[gps_switch()]
                print(gps_data)
                # For loop comprehension ...
                [r.set('gps:' + k, v, ex=REDIS_EXP) for k, v in gps_data.items()]
                time.sleep(GPS_TIMEOUT)
        except (KeyboardInterrupt, SystemExit):
            gpsp.running = False
            gpsp.join()
    except (OSError, ConnectionError, NameError) as e:
        gps_data['message'] = 'error'
        while True:
            print(gps_data)
            time.sleep(GPS_TIMEOUT)

