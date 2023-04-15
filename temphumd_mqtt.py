from paho.mqtt.client import Client

TEMP = 'temperature'
HUMIDITY = 'humidity'
K0 = 25
K1 = 75

def on_message(mqttc, data, msg):
    print (f'message:{msg.topic}:{msg.payload}:{data}')
    if data == 0:
        temp = int(msg.payload)
        if temp > K0:
            print(f'Superado  K0 = {temp}')
            mqttc.subscribe(HUMIDITY)
            data = 1
    elif data == 1:
        if msg.topic == HUMIDITY:
            humidity = int(msg.payload)
            if humidity > K1:
                print(f'Superado K1 = {humidity} ')
                mqttc.unsubscribe(HUMIDITY)
                data= 0
        elif TEMP in msg.topic:
            temp = int(msg.payload)
            if temp <= K0:
                print(f'temperatura {temp} por debajo de K0')
                data = 0 
                mqttc.unsubscribe(HUMIDITY)
                
def on_log(mqttc, data, level, string):
    print(f'LOG: {data}: {string}')
    
def main(broker):
    data = 0
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