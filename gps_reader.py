import redis
import configparser
import os
import time

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
gps_config = configparser.ConfigParser()

gps_config.read("{}/config/gps.ini".format(WORKING_DIR))

REDIS_HOST = gps_config.get("redis", "host")
REDIS_PORT = gps_config.getint("redis", "port")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def get_mng(rget):
    return rget.decode() if rget else '--.--'


def console_screen():
    os.system('clear')

    print('Press Ctrl+C to Quit')
    print('========================================')
    print('GPS status  :', get_mng(r.get('gps:message')))
    print('----------------------------------------')
    print('latitude    :', get_mng(r.get('gps:latitude')))
    print('longitude   :', get_mng(r.get('gps:longitude')))
    print('time utc    :', get_mng(r.get('gps:utc')))
    print('altitude (m):', get_mng(r.get('gps:altitude')))
    print('speed (m/s) :', get_mng(r.get('gps:speed')))


if __name__ == "__main__":
   try:
       while True:
           console_screen()
           time.sleep(1)
   except (KeyboardInterrupt, SystemError):
       exit(0)