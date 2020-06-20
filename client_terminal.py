import argparse
import speech_recognition as sr
from client_Action import ClientAction

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

clientAction = ClientAction(args.file, args.ip, args.port)

while True:
    # convert the audio to text
    if(args.voice):
        input('press enter when you are ready to send a message')
        print("say something!!….")
        try:
            resp = clientAction.AudioMessage()
        except sr.UnknownValueError:
            print("could not understand audio")
        except sr.RequestError as e:
            print("Could not request results ; {0}".format(e))
        except:
            print(" Error : token Error ")
            break
    else:
        try:
            msg = input("insert mssage here: ")
            resp = clientAction.TextMessage(msg)
        except:
            print(" Error : token Error ")
            break

    # Parse the output from Wit.ai
    msgMqtt = dict()
    for key, value in resp['entities'].items():
        msgMqtt[key] = value[0]['value']

    # Send the action to BOBB3E
    print('sent message to BOBB3E ')
    try:

        clientAction.SendMessage(msgMqtt)
    except:
        print("Error : can't  connect with mosquitto server ")
