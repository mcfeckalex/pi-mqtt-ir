import paho.mqtt.client as mqtt
from subprocess import call
import os
import time
import RPi.GPIO as GPIO
path= os.path.dirname(os.path.realpath(__file__))
broker_address = "192.168.1.111"

# This pin is also referred to as GPIO23
OUTPUT_WIRE = 7

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(OUTPUT_WIRE, GPIO.OUT)

def on_message(client, userdata, message):
    #GPIO.output(OUTPUT_WIRE, 0) 
    print("message received: " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    message = str(message.payload.decode("utf-8")).replace("\'", "")
    message = message.replace("(","")
    message = message.replace(")","")
    message = message.replace(" ","")
    command = message.split(",")
    print command
    call(["python", path+"/irrp.py", "-p", "-g23", "-f", path+"/"+command[0], command[1]])

def on_disconnect(client, userdata, rc):
    client.loop_stop()

def on_connect(Client, userdate, flag, rc):
    print "Connected.."


client = mqtt.Client("P1") #create new instance
client.on_message=on_message        #attach function to callback
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.connect(broker_address) #connect to broker
client.loop_start()    #start the loop
client.subscribe("heatpump/command")

while(1):
    pass
    