from paho.mqtt.client import Client
from multiprocessing import Process, Manager
from time import sleep
from math import floor
import random

NUMBERS = 'numbers'
CLIENTS = 'clients'
TIMER_STOP = f'{CLIENTS}/timerstop'
HUMIDITY = 'humidity'


def is_integer(n):
    if floor(n) == n:
        return True
    else:
        return False

def timer(time, data):
    mqttc = Client()
    mqttc.connect(data['broker'])
    msg = f'timer working. timeout: {time}'
    print(msg)
    mqttc.publish(TIMER_STOP, msg)
    sleep(time)
    msg = f'timer working. timeout: {time}'
    mqttc.publish(TIMER_STOP, msg)
    print('timer end working')
    mqttc.disconnect()


def on_message(mqttc, data, msg):
    print(f"MESSAGE:data:{data}, msg.topic:{msg.topic}, payload:{msg.payload}")
    try:
        if is_integer(float(msg.payload)):
            print(f"Message is an integer")
        else:
            print("Message is a real number")
        sleep(random.random()*10)
    except ValueError as e:
        print(e)
        pass
    
    
def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)
    
    
def main(broker):
    data = {'client':None,
            'broker': broker}
    mqttc = Client(client_id="numbers_prop", userdata=data)
    data['client'] = mqttc
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_log = on_log
    mqttc.connect(broker)
    mqttc.subscribe(NUMBERS)
    mqttc.loop_forever()
    
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)