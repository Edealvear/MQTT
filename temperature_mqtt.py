from threading import Lock
from paho.mqtt.client import Client
from time import sleep

def on_message(mqttc, data, msg):
    print ('on_message', msg.topic, msg.payload)
    n = len('temperature/')
    lock = data['lock']
    lock.acquire()
    try:
        key = msg.topic[n:]
        if key in data:
            data['temp'][key].append(float(msg.payload))
        else:
            data['temp'][key]=[float(msg.payload)]
    finally:
        lock.release()
    print ('on_message', data)

def orden(a):
    return max(a)

def main(broker):
    data  = {'lock':Lock(), 'temp':{}}
    mqttc = Client(userdata=data)
    mqttc.on_message = on_message
    mqttc.connect(broker)
    mqttc.subscribe('temperature/t1')
    mqttc.loop_start()
    while True:
        sleep(5)
        maxim = max(data['temp'].values(), key = orden)
        print(maxim)
        minimum = min(data['temp'].values(), key = orden)
        print(f'maximum temperature recorded: {maxim} \nminimum temperature recorded {minimum}')
            
            
if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)