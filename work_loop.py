import uasyncio as asyncio
from config import get_config

from log_file import log_debug, log_vals

async def main_loop():
    # GET CONFIG
    CONFIG = get_config()

    if not CONFIG:
        trySecs = 5
        log_debug('error', 'No config found. Trying again in ' +str(trySecs)+ ' seconds')

        while not CONFIG:
            CONFIG = get_config()
            asyncio.sleep(trySecs)

    ZONES = CONFIG['zones'];
    SENSORS = CONFIG['sensors'];
    SOLENOIDS = CONFIG['solenoids'];
    PARAMS = CONFIG['params'];

    if len(ZONES) == 0 or len(SENSORS) == 0 or len(SOLENOIDS) == 0:
        log_debug('error', 'Not all config data found');
        return False


    while True:
        inactiveZones = 0

        for zoneKey in ZONES:
            zone = ZONES[zoneKey]
        
            if zone['active'] == False:
                inactiveZones =+ 1
                log_debug('info', 'Inactive zone found. Skipping...', zoneKey)
                continue

            # LOAD SENSORS
            zoneSensors = zone['sensors']
            if len(zoneSensors) == 0:
                inactiveZones =+ 1
                log_debug('info', 'No active senors for zone. Skipping...', zoneKey)
                continue


            # START MEASURING
            log_debug('info', 'Starting to read moistures', zoneKey)

            totalReadings = PARAMS['moistureSensorReadings'];

            sensorReadings = {}
            for sensorKey in zoneSensors:
                vals = []

                sensorError = False

                for i in range(totalReadings):
                    # try:
                    val = get_sensor_reading(sensorKey)

                    if not val:
                        sensorError = True
                        break

                    vals.append(val)
                
                if sensorError:
                    log_debug('error', 'Sensor ['+str(sensorKey)+'] has error: '+str(sensorError), zoneKey)
                    continue

                log_debug('info', 'Sensor ['+str(sensorKey)+'] found total moisture values: ['+",".join(vals)+']', zoneKey)

                sensorReadings[sensorKey] = vals

            # LOG VALUES TO FILE
            if len(sensorReadings):
                log_debug('error', 'All sensor reading are empty, continuing...', zoneKey)
                continue

            
            moisVal = 0
            for sensorKey in sensorReadings:
                vals = sensorReadings[sensorKey]

                val_sum = sum(vals)
                val_len = len(vals)

                # GET AVARAGE VAL
                moisVal =+ val_sum / val_len

            
            # GET AVARAGE READING OF MULTIPLE SENSORS
            moisture = moisVal / len(zoneSensors);

            log_debug('info', 'Avarage moisture reading: '+str(moisture), zoneKey)

            # GET MIN MOISTURE OF THE ZONE
            minMoisture = zone['minMoisture']

            if moisture > minMoisture:
                log_debug('info', 'Moisture level OK. Min: '+str(minMoisture))
                continue




            # ACTIVATE SOLENOIDS
            solenoids = zone['solenoids']

            if len(solenoids) == 0:
                print('No defined solenoids for zone')
                break

            totalFlow = 0
            for solenoidKey in solenoids:
                solenoid = solenoids[solenoidKey]

                openTime = 100
                if 'openTime' in solenoid: openTime = solenoid['openTime']

                flow = activate_solenoid(solenoidKey, openTime)

                if not flow:
                    break

                totalFlow =+ flow

            if totalFlow == 0:
                print('No water dispensed!')
                break

            # CHECK MIN MAX FLOW
            minFlow = zone['minFlow']
            maxFlow = zone['maxFlow']

            if totalFlow < minFlow:
                print('Shortage of flow with dif: '+ str(totalFlow - minFlow))
            elif totalFlow > maxFlow:
                print('Too much water dispensed with diff: '+ str(totalFlow - maxFlow))
        await asyncio.sleep(5)





def get_sensor_reading(key):
    if not key: return False

    # GET DATA
    if not key in SENSORS:
        print('Sensor with key: '+str(key)+ ' not found')
        return False

    sensor = SENSORS[key]

    if sensor['active'] == False:
        print('Sensor with key: '+ str(key) + ' not active')
        return False
    
    if not 'pin' in sensor:
        print('Sensor with key: '+str(key)+ ' PIN not defined')
        return False

    PIN = sensor['pin'];

    if not PIN: return False
    
    # GET VALUE WITH PIN
    print('Getting moisture value')
    return 20


def activate_solenoid(key, openTime):
    if not key: return False

    # GET DATA
    if not key in SOLENOIDS:
        print('Solenoid with key: '+str(key)+ ' not found')
        return False

    solenoid = SOLENOIDS[key]

    if solenoid['active'] == False:
        print('Solenoid with key: '+ str(key) + ' not active')
        return False

    if not openTime:
        if 'openTime' in solenoid:
            openTime = solenoid['openTime']
        else:
            print('Solenoid with key: '+str(key)+ ' time not defined')
            return False
    
    if not 'pin' in solenoid:
        print('Solenoid with key: '+str(key)+ ' PIN not defined')
        return False

    PIN = solenoid['pin']

    if not PIN: return False

    # ACTIVATE SENSOR AND WHILE FLOW SENSOR IS ALSO ACTIVE
    flow = get_flow()
    # ACTIVATE SOLENOID
    print('Activating solenoid')
    time.sleep(openTime)

    # DEACTIVATE SOLENOID
    print('Deactivating solenoid')

    return flow

def get_flow():
    if not 'flow0' in SENSORS:
        print('Flow sensor not found in config')
        return False
    
    data = SENSORS['flow0']

    if data['active'] == False:
        print('Flow sensor not active')
        return False
    
    if not 'pin' in data:
        print('Flow sensor PIN not defined')
        return False

    PIN = data['pin']

    # GET DATA - HOW MUCH FLOWED WATER
    return 12