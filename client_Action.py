import argparse
from wit import Wit
import json
import paho.mqtt.client as mqtt
import speech_recognition as sr


class ClientAction():
    def __init__(self, TokenFile, Ip, Port):
        with open(TokenFile, 'r') as File:
            self._Token = File.readline()
        self._ClientWit = Wit(self._Token)
        self._ClientMqtt = mqtt.Client()
        self._Recognizer = sr.Recognizer()
        self._Speech = sr.Microphone()
        self._Ip = Ip
        self._Port = Port

    def AudioMessage(self):
        with self._Speech as source:
            self._Recognizer.adjust_for_ambient_noise(source)
            audio = self._Recognizer.listen(source)
            msg = self._Recognizer.recognize_wit(audio, key=self._Token)
        return self.TextMessage(msg)

    def TextMessage(self, msg):
        # send the message to the wit.ai server
        return self._ClientWit.message(msg)

    def SendMessage(self, msg):
        # send the message to BOBB3E
        self._ClientMqtt.connect(self._Ip, self._Port, 1)
        self._ClientMqtt.publish("Action", json.dumps(msg))
        self._ClientMqtt.disconnect()
