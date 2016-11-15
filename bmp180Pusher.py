import sys
import time
import requests
import pprint
import json
import random
from collections import OrderedDict

class MockSensor:
    temp = 20.0
    pressure = 1000.0
    alti = 150.0
    sea_alti = 1.0
    
    def read_temperature(self):
        self.temp = self.randomVal(20.0,self.temp)
        return self.temp
    
    def read_pressure(self):
        self.pressure = self.randomVal(1000.0, self.pressure)
        return self.pressure
            
    def read_altitude(self):
        self.alti = self.randomVal(150.0, self.alti)
        return self.alti
                
    def read_sealevel_pressure(self):
        self.sea_alti = self.randomVal(1.0, self.sea_alti)
        return self.sea_alti
            
    def randomVal(self, avg, current):
        if random.random() * (current/avg) > 0.5:
            return current - random.random();
        else:
            return current + random.random();

def readValues(sensor):
    return dict(
            temperature       = {'value':sensor.read_temperature(),       'unit':'*C'},
            pressure          = {'value':sensor.read_pressure(),          'unit':'Pa'},
            altitude          = {'value':sensor.read_altitude(),          'unit':'m'},
            sealevel_pressure = {'value':sensor.read_sealevel_pressure(), 'unit':'Pa'}
           )

def pushSensorValues(sensor, url, freqMs):
    while True:
        values = OrderedDict(readValues(sensor))
        print('Pushing to {} the data:\n{}\n ...'.format(url, pprint.pformat(values)))
        try:
            r = requests.put(url, data={'var':json.dumps(values)},timeout=1)
            print ('Status: %s' % r.reason)
        except Exception as e:
            print (e)
        time.sleep(freqMs / 1000.0)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        pushSensorValues(sensor=MockSensor(), url=sys.argv[1], freqMs=int(sys.argv[2]))

    elif len(sys.argv) == 4:
        import Adafruit_BMP.BMP085 as BMP085
        sensor = BMP085.BMP085(busnum=int(sys.argv[3]))
        pushSensorValues(sensor=sensor, url=sys.argv[1], freqMs=int(sys.argv[2]))

    else:
        print('usage (BMP085):    <restUrl> <frequencyMs> <busNumber>')
        print('usage (simulated): <restUrl> <frequencyMs>')
        exit(1)
