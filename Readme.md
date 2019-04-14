# Description

## Simple GPS Poller with Redis backend

* `gpsd_poller.py`

Generally speaking program polls data from running gpsd service and puts it in Redis and append 'message'
about validity of sent gps data. Expiration time had added to the gps data sent to Redis so the old data
 could not persist.

The cases are:
1. The switch key in config set to True.
    * Everything is normal, gps and gpsd are working - the message 'ok' appended to gps data.  
    * gps or gpsd are not working or running properly - the message 'error' appended to 
    default gps position (default position is in the config file).

2. The switch key in config file set to False.
    * the message 'switched off' appended to default gps position (default position is in the config file).
    

* `gps_reader.py`

Reads gps data from Redis