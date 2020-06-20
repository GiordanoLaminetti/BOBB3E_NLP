import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlNumber
from pyforms.controls import ControlButton
from pyforms.controls import ControlTextArea
from client_Action import ClientAction
import speech_recognition as sr
import os


class BOBB3EClient(BaseWidget):

    def __init__(self):
        super(BOBB3EClient, self).__init__('BOBB3E NLP')

        # Definition of the forms fields
        self._ip = ControlText('IP', default='ev3dev.local')
        self._port = ControlNumber('Port', default=1883, maximum=65535)
        self._tokenfile = ControlText('Tokenfile', default='token')
        self._msg = ControlText('Message', visible=False)
        self._buttonMsg = ControlButton('Send Text Message', visible=False)
        self._buttonAudio = ControlButton('Send Audio Audio', visible=False)
        self._buttonConnect = ControlButton('Connect', visible=True)
        self._log = ControlTextArea('log', '', readonly=True)
       # add the action to the button
        self._buttonMsg.value = self.__buttonMsgAction
        self._buttonAudio.value = self.__buttonAudioAction
        self._buttonConnect.value = self.__buttonConnect

        self.formset = [('_ip', '_port', '_tokenfile', '_buttonConnect'),
                        '_msg', ('_buttonMsg', '_buttonAudio'), '_log']

    def __buttonConnect(self):
        self._clientAction = ClientAction(
            self._tokenfile.value, self._ip.value, self._port.value)
        self._log.value = str(self._log.value) + \
            'log : ip = '+self._ip.value+', port =' + \
            str(self._port.value)+' \n '
        self._tokenfile.hide()
        self._ip.hide()
        self._port.hide()
        self._buttonConnect.hide()
        self._msg.show()
        self._buttonMsg.show()
        self._buttonAudio.show()

    def __buttonMsgAction(self):
        """Send the text message to BOBB3E"""
        resp = self._clientAction.TextMessage(self._msg)
        msgMqtt = dict()
        for key, value in resp['entities'].items():
            msgMqtt[key] = value[0]['value']
        # Send the action to BOBB3E
        self._log.value = str(self._log.value) + \
            'log : sent message to BOBB3E \n '
        try:

            self._clientAction.SendMessage(msgMqtt)
        except:
            self._log.value = str(self._log.value) + \
                "Error : cannot  connect with mosquitto server \n"

    def __buttonAudioAction(self):
        """Recording Audio and Send it to BOBB3E"""
        self._log.value = str(self._log.value) + "say something!!….  \n"
        try:
            resp = self._clientAction.AudioMessage()
        except sr.UnknownValueError:
            self._log.value = str(self._log.value) +  \
                "could not understand audio \n"
        except sr.RequestError as e:
            self._log.value = str(self._log.value) + \
                "Could not request results ; {0} \n".format(e)
        except:
            self._log.value = str(self._log.value) +  \
                " Error : token Error \n"
        msgMqtt = dict()
        for key, value in resp['entities'].items():
            msgMqtt[key] = value[0]['value']
        # Send the action to BOBB3E
        self._log.value = str(self._log.value) +  \
            'log : sent message to BOBB3E \n '
        try:
            self._clientAction.SendMessage(msgMqtt)
        except:
            self._log.value = str(self._log.value) + \
                "Error : can't  connect with mosquitto server \n"


# Execute the application
if __name__ == "__main__":
    pyforms.settings.PYFORMS_STYLESHEET = 'style.css'
    pyforms.start_app(BOBB3EClient)
