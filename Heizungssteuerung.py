# P-Seminar Stratosphaerenflug, 22 January 2021
# Version 1.0

# PREDEFINED CODE AND VARIABLES

# Libraries needed for this script: gpiozero, time
from gpiozero import OutputDevice, CPUTemperature
from time import sleep

# Adjustable Variables
minSOCTemperature           = 20                                                                # SOC temperature threshold which triggers the heating-circuit (degrees Celcius)
maxSOCTemperature           = 80                                                                # SOC temperature at which the heating will be stopped (set to 100 degrees Celcius to ignore)
temperatureOffsetSOC        = 0                                                                 # Adjust possible temperature offsets

usedPinNumber               = 17                                                                # Index of the GPIO-Pin to be used
consideredMeasurements      = 10                                                                # Amount of measurements averaged in order to compensate for lacking precision/spikes
measurementFrequency        = 1                                                                 # Amount of measurements per second (hertz)
                                                                                                # The maximum reaction time (seconds) caused by the averaging logic can be calculated by: 
                                                                                                # consideredMeasurements/measurementFrequency = reaction time

sepTempSensorPath           = "/sys/bus/w1/devices/28-000009586bf6/w1_slave"                    # File path to w1_slave file of the seperate internal temperature sensor
minSepSensorTemperature     = 0                                                                 # Seperately measured temperature threshold which triggers the heating-circuit (degrees Celcius)
maxSepSensorTemperature     = 30                                                                # Seperately measured temperature at which the heating will be stopped (degrees Celcius)
temperatureOffsetSepSensor  = 0                                                                 # Adjust possible temperature offsets

# Predefined functions
# Average all given values in the list
def averageValueFromList(listIn = list()):
    accumulatedAmount = 0

    ii = 0
    while ii < len(listIn):
        accumulatedAmount += listIn[ii]
        ii += 1

    return accumulatedAmount/len(listIn)

# Read the log/output file of the seperate temperature sensor
def readSepTempSensor():
    out = -1

    file = open(sepTempSensorPath, "r")

    if file:
        m = file.read()
        file.close()
        
        if len(m.split("t=")) > 1:
            out = float(m.split("t=")[1])/1000

        print("Read value: ", out, " from w1_slave\n")
    else:
        print("Error: Failed to open w1_slave!\n")

    return out


# PROGRAM CODE
print("Heating-Circuit software starting...\n")

# Retrieve handles to the temperature sensor and the GPIO-Pin
gpioPin = OutputDevice(usedPinNumber)                      
tempSensSOC = CPUTemperature(min_temp = 0, max_temp = 85)

# Get the first SOC temperature readings
measurementsSOC = list()

i = 0
while i < consideredMeasurements:
    measurementsSOC.append(tempSensSOC.temperature)
    i += 1

averageSOCTemperature = averageValueFromList(measurementsSOC)

# Get the first seperate sensor readings
measurementsSepSensor = list()

tempValue = readSepTempSensor()

i = 0
while i < consideredMeasurements:
    measurementsSepSensor.append(tempValue)
    i += 1

averageSepSensorTemperature = tempValue

# Heating routine
print("Heating-Circuit software running...\n")

i = 0
while True:
    # Include new SOC measurement and calculate averageTemperature
    measurementsSOC[i] = tempSensSOC.temperature
    averageSOCTemperature = averageValueFromList(measurementsSOC)

    print("AverageSOCTemperature: ", averageSOCTemperature, "°C\n")

    # Include new seperate sensor measurement and calculate averageTemperature
    measurementsSepSensor[i] = readSepTempSensor()
    averageSepSensorTemperature = averageValueFromList(measurementsSepSensor)

    print("AverageSepSensorTemperature: ", averageSepSensorTemperature, "°C\n")

    # Increase/reset i
    i += 1

    if i >= consideredMeasurements:
        i = 0

    # Turn the heating-cicuit on, if the average SOC temperature sinks below the defined minimum temperature
    # There should be a ~3.3V difference between the GPIO-Pin and a Ground-Pin on the Pi-board
    if averageSOCTemperature <= minSOCTemperature + temperatureOffsetSOC:
        gpioPin.on()
        print("Heating-Circuit on: minSOCTemperature\n")

    # Turn the heating-cicuit on, if the average seperate sensor temperature sinks below the defined minimum temperature
    # There should be a ~3.3V difference between the GPIO-Pin and a Ground-Pin on the Pi-board
    if averageSepSensorTemperature <= minSepSensorTemperature + temperatureOffsetSepSensor:
        gpioPin.on()
        print("Heating-Circuit on: minSepSensorTemperature\n")
    
    # Turn the heating-circuit off, if the average SOC temperature rises above the defined deactivation temperature
    # There should be no or only a small voltage difference between the GPIO-Pin and a Ground-Pin on the Pi-board
    if averageSOCTemperature >= maxSOCTemperature + temperatureOffsetSOC:
        gpioPin.off()
        print("Heating-Circuit off: maxSOCTemperature\n")

    # Turn the heating-circuit off, if the average seperate sensor temperature rises above the defined deactivation temperature
    # There should be no or only a small voltage difference between the GPIO-Pin and a Ground-Pin on the Pi-board
    if averageSepSensorTemperature >= maxSepSensorTemperature + temperatureOffsetSepSensor:
        gpioPin.off()
        print("Heating-Circuit off: maxSepSensorTemperature\n")

    # Pause until next measurement
    sleep(1/measurementFrequency)

# SCRIPT END