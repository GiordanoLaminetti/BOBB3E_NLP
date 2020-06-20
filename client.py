from wit import Wit
import json
import paho.mqtt.client as mqtt

client_mqtt = mqtt.Client()
client_wit = Wit('NDIMDGI22K2R3XMCJQWUHUIRJRG5XSRX')
while True:
    msg = input('insert mssage here: ')
    resp = client_wit.message(msg)
    msg_mqtt = dict()
    print(resp)
    for key, value in resp['entities'].items():
        msg_mqtt[key] = value[0]['value']
    client_mqtt.connect("ev3dev.local", 1883, 60)
    client_mqtt.publish("Action", json.dumps(msg_mqtt))
    print(msg_mqtt)
    client_mqtt.disconnect()
