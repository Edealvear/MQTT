from paho.mqtt.client import Client
from multiprocessing import Process, Manager
from time import sleep
import paho.mqtt.publish as publish
import time

TOPIC = "clients/temporiz"

def timer(mqttc,msg):
    TimTopMsg = msg.payload.split(", ")#Recibe el mensaje que deberá ser mandado "tiempo, topic, mensaje"
    sleep(float(TimTopMsg[0]))
    mqttc.publish(TimTopMsg[1], TimTopMsg[2])

def on_message(mqttc, data, msg):
    try:
        p = Process(target= timer, args=(mqttc, msg)) 
        p.start()
    except Exception as e:
        print(e)
    
def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)
    
def main(broker):
    data={'status' : 0}
    mqttc = Client(userdata=data)
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_log = on_log
    mqttc.connect(broker)
    mqttc.subscribe(TOPIC)
    mqttc.pub
    mqttc.loop_forever
    
if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)