from paho.mqtt import Client

class Raptor():
    default = {
        "global": {
            "username": None,
            "password": None,
        }
        "mqtt": {
            "host": "api.rapotorbox.eu",
            "port": 1883,
        },
        "rest": {
            "url": "https://api.raptorbox.eu",
            "routes": None
        }
    }

    def __init__(self, config):
        '''
        Raptor accepts mqtt connections for subscribing only to topics, but you cannot push
        for pushing data it's needed to use a restful api
        '''

        #init mqtt Client

        #init Rest client


    def connect(self): #TODO consider srv field in dns
