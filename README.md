# BOBB3E_NLP
an action recognition for BOBB3E (Lego Mindstorm EV3 ) robot , using a Wit.ai nets

## Table of Contents
1. [Download Repo](#Download_Repo)
2. [Set up Client](#Client)
3. [Set up Broker](#Broker)
4. [Set up Server(EV3)](#Server)
5. [Set up Wit.ai](#Wit.ai)
6. [Run](#Run)

## <a name='Download_Repo'>Download Repo</a>
first you need to clone this repository on your device and on EV3DEV

## <a name='Client'>Set up Client</a>

The client is the device that you want to use to connect with the EV3,
you need install the require library using

```
pip3 install -r requirement.txt
```

if mosquitto is not present on your device you can install it. from it's [website](https://mosquitto.org/download/)


## <a name='Broker'>Set up Broker</a>

the broker is the device uset to keep the message between client and server, in this case is based on mosquitto A message broker that implements the MQTT protocol.
The device need mosquitto, you can start a broker on a linux based System simplyfy using

```
sudo mosquitto
```

## <a name='Server'>Set up Server</a>

the EV3DEV distribution already has a mosquitto daemon, but you need install the python library to use them via
```
pip3 install -r requirement_server.txt
```

## <a name='Wit.ai'>Set up Wit.ai</a>
This project require a Project on Wit.ai, to set up this project you neeed to create an account, after the creaction you can click the **New App**, in the new app pannel, under the **Import From a Backup** you can add the zip file in the **wit** folder of the repo.

after the creation of the application under setting you get the **Server Access Token** that you might copy and insert in an file *token* in the client device on the root folder of the project


## <a name='Run'>Run</a>
### Run Server
on ev3 to start you can digit
```
python3 message_sever.py
```
by default the broker is located on EV3 so ip is *localhost* and the port is *1883* , you can change this via **-i** and **-p** options

### Run Client
the client can run either on terminal or usign a simply GUI based on Pyform
to run the client in terminal you can use
```
python3 client_terminal.py
```
by default it use the tokenfile *token* and the ip *ev3dev.local* and port *1883* of the borker ,  you can change this via **-i**, **-p** and **-f** options, usign the **-v** you can use your voice to tell action.

to run in a GUI mode you run 
```
python3 client_GUI.py
```
and follow the istruction on the GUI
