from paho.mqtt.client import Client
from math import floor 
from time import sleep
import random 

TEMP = 'temperature'
HUMIDITY = 'humidity'
NUMBERS = 'numbers'
K0 = 25
K1 = 75

def is_integer(n):
    if floor(n) == n:
        return True
    else:
        return False


def on_message(mqttc, data, msg):
    print (f'message:{msg.topic}:{msg.payload}:{data}')
    if data["status"] == 0:
        temp = int(msg.payload)
        data["temp"].append(temp)
        if temp > K0:
            print(f'Superado  K0 = {temp}')
            mqttc.subscribe(HUMIDITY)
            data["status"] = 1
    elif data["status"] == 1:
        if msg.topic == HUMIDITY:
            humidity = int(msg.payload)
            data["hum"].append(humidity)
            if humidity > K1:
                print(f'Superado K1 = {humidity} ')
                mqttc.unsubscribe(HUMIDITY)
                data["hum"] = []
                data["status"] = 2
                mqttc.subscribe(NUMBERS)
        elif TEMP in msg.topic:
            temp = int(msg.payload)
            if temp <= K0:
                print(f'temperatura {temp} por debajo de K0')
                data["status"] = 3
                data["hum"] = []
                mqttc.subscribe(NUMBERS)
    elif data["status"] == 2:
        if msg.topic == NUMBERS:
            num = int(msg.payload)
            data["numbers"] = num * data["numbers"]/2
        elif msg.topic == "temp":
            if data["numbers"] / max(float(msg.payload),2):
                mqttc.publish("clients/publicaciones", data["numbers"])
                data["numbers"] = 0
                data["status"] = 0
    elif data["status"] == 3:
        if msg.topic == NUMBERS:
            data["numbers"] += float(msg.payload)
        elif msg.topic == HUMIDITY:
            data["numbers"] = data["numbers"]/3
            mqttc.publish("clients/publicaciones", str(data["numbers"] + float(msg.payload)))
            sleep(random.randint(0,12))
        elif msg.topic == TEMP:
            data["numbers"] = data["numbers"]/max(float(msg.payload),2)
            if data["numbers"] < 2:
                data["numbers"] = 0
                data["status"] = 1
                data["temp"] = []
                

            
def on_log(mqttc, data, level, string):
    print(f'LOG: {data}: {string}')
    
def main(broker):

    data = {"temp" : [], "hum" : [] , "numbers": 0,"status" : 0 }
    mqttc = Client(userdata=data)
    mqttc.on_message = on_message
    mqttc.enable_logger()
    mqttc.connect(broker)
    mqttc.subscribe(f'{TEMP}/t1')
    mqttc.loop_forever()
if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)