# This file contains the main loop

from time import sleep
import bh1750
import tca9548a
from simplemqtt import MQTTClient
import veml7700

def sort_readings(item):
    return item[1]


def work(scl_pin, sda_pin, tca_address, intervall, sensor_mappings, factor_sunny, mqtt_broker, mqtt_client_id, mqtt_port, mqtt_user, mqtt_password, mqtt_topic):
    tca = tca9548a.TCA9548A(scl_pin, sda_pin, tca_address)
    mqtt_client = MQTTClient(mqtt_client_id, mqtt_broker, mqtt_port, mqtt_user, mqtt_password)

    while True:
        try:
            mqtt_client.connect()
            sensor_readings = []
            for row in sensor_mappings:
                tca.switch_channel(row[0])
                if row[1] == "BH1750":
                    sensor = bh1750.BH1750(tca.bus)
                    sensor.reset()
                    reading = sensor.luminance(bh1750.BH1750.ONCE_HIRES_1) * row[4]
                    mqtt_client.publish(mqtt_topic + row[2], str(reading))
                    if row[3]:
                        sensor_readings.append([row[2], reading])
                    sensor.off()
                    print("Sensor readings: " + str(sensor_readings))
                elif row[1] == "VEML7700":
                    sensor = veml7700.VEML7700(address=0x10, i2c=tca.bus, it=25, gain=1/8)
                    reading = sensor.read_lux() * row[4]
                    mqtt_client.publish(mqtt_topic + row[2], str(reading))
                    if row[3]:
                        sensor_readings.append([row[2], reading])
                    print("Sensor readings: " + str(sensor_readings))
                else:
                    print("Unknown sensor or bad config!")
                
                print("Sensor readings: " + str(sensor_readings))
                sensor_readings.sort(key=sort_readings)
                print("Sensor readings: " + str(sensor_readings))

                sunny_sides = []                 
                for row in sensor_readings:
                    if row[1] >= sensor_readings[1][1] * factor_sunny:
                        sunny_sides.append(row[0])

                print("Sunny sides: " + str(sunny_sides))    
                if len(sunny_sides) >= 1:
                    mqtt_client.publish(mqtt_topic + "direction", str(sunny_sides))
                else:
                    mqtt_client.publish(mqtt_topic + "direction", "none")
            mqtt_client.disconnect()
        except:
            print("Error in workcycle")
        print("Workcycle complete. Will sleep now for " +
              str(intervall) + " seconds")
        sleep(intervall)
