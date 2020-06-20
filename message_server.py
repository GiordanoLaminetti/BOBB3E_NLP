from robot import *
import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    client.subscribe("Action")
    print('Conncect to Action')


def on_message(client, userdata, msg):
    a = msg.payload.decode()
    action = json.loads(a)
    # try:
    if action['intent'] == 'exit':
        print('disconnect')
        client.disconnect()
    else:
        print('action to execute', action['intent'])
        method_to_call = globals()[action['intent']]
        print(method_to_call)
        method_to_call(**action)
    '''
    except:
        error()
    '''


client = mqtt.Client()
client.connect("localhost", 1883, 60)
hello()
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
