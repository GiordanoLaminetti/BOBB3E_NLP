import argparse
from wit import Wit
import json
import paho.mqtt.client as mqtt
import speech_recognition as sr

parser = argparse.ArgumentParser(
    description='client message for the action recognition')

parser.add_argument('-i', '--ip', nargs='?', type=str, default="ev3dev.local",
                    help='ip address of the Broker (Default: ev3dev.local)')

parser.add_argument('-p', '--port', nargs='?', type=int, default=1883,
                    help='port of the Broker (Default: 1883)')

parser.add_argument('-f', '--file', nargs='?', type=str, default='Token',
                    help='file with the token  (Default: Token)')

parser.add_argument('-v', '--voice', action='store_true',
                    help='use the voice interface (Default: Token)')

args = parser.parse_args()

# Initialize the client class
client_mqtt = mqtt.Client()

# initialize the spechrecognition
if(args.voice):
    r = sr.Recognizer()
    speech = sr.Microphone()

with open(args.file, 'r') as File:
    token = File.readline()
    client_wit = Wit(token)


while True:
    # convert the audio to text
    if(args.voice):
        input('press enter when you are ready to send a message')
        with speech as source:
            print("say something!!….")
            audio = r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            msg = r.recognize_wit(audio, key=token)
        except sr.UnknownValueError:
            print("could not understand audio")
        except sr.RequestError as e:
            print("Could not request results ; {0}".format(e))
        except:
            print(" Error : token Error ")
            break
    else:
        msg = input("insert mssage here: ")

    print(msg)
    try:
        # send the input to the Wit.ai net to recognize the action
        resp = client_wit.message(msg)
    except:
        print(" Error : token Error ")
        break

    # Parse the output from Wit.ai
    print(resp)
    msg_mqtt = dict()
    for key, value in resp['entities'].items():
        msg_mqtt[key] = value[0]['value']

    # Send the action to BOBB3E
    try:
        client_mqtt.connect(args.ip, args.port, 1)
        client_mqtt.publish("Action", json.dumps(msg_mqtt))
        client_mqtt.disconnect()
    except:
        print("Error : can't  connect with mosquitto server ")
