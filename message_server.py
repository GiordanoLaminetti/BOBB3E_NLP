import argparse
import paho.mqtt.client as mqtt
import json
from robot import *

parser = argparse.ArgumentParser(
    description='message server for the action recognition')

parser.add_argument('-i', '--ip', nargs='?', type=str, default='localhost',
                    help='ip address of the Broker (Default: localhost)')

parser.add_argument('-p', '--port', nargs='?', type=int,  default=1883,
                    help='port of the Broker (Default: 1883)')


def on_connect(client, userdata, flags, rc):
    client.subscribe("Action")
    print('Conncect to Action')


def on_message(client, userdata, msg):
    # retrive the action
    a = msg.payload.decode()
    action = json.loads(a)
    try:
        # parse the action and Execute them
        if action['intent'] == 'exit':
            print('disconnect')
            client.disconnect()
        else:
            print('action to execute', action['intent'])
            method_to_call = globals()[action['intent']]
            print(method_to_call)
            method_to_call(**action)
    except:
        error()


if __name__ == "__main__":
    # connect to the mosquitto server
    args = parser.parse_args()
    try:
        client = mqtt.Client()
        client.connect(args.ip, args.port, 60)
        hello()
        client.on_connect = on_connect
        client.on_message = on_message

        client.loop_forever()
    except:
        print("can't connect to the broker")
