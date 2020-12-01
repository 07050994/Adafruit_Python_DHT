#!/usr/bin/python3
import Adafruit_DHT
import time
import sys
import http.client as http
import urllib
import json
deviceId = "Dg2VIGT9"
deviceKey = "vIP08oYXGUGQPAn9"
def post_to_mcs(payload): 
        headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
        not_connected = 1 
        while (not_connected):
                try:
                        conn = http.HTTPConnection("api.mediatek.com:80")
                        conn.connect() 
                        not_connected = 0 
                except (http.HTTPException, socket.error) as ex: 
                        print ("Error: %s" % ex)
                        time.sleep(10)
			 # sleep 10 seconds 
        conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
        response = conn.getresponse() 
        print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
        data = response.read() 
        conn.close() 


while True:
        h0, t0= Adafruit_DHT.read_retry(11, 4)
        if h0 is not None and t0 is not None:
                print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(t0, h0))

                payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}},
                {"dataChnId":"Temperature","values":{"value":t0}}]} 
                post_to_mcs(payload)
                time.sleep(10) 
        else:
                print('Failed to get reading. Try again!')
                sys.exit(1)


