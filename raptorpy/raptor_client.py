'''
Contents:
=========

This package contains the class RaptorClient which is a wrapper for mqtt and rest clients
'''
from clients import mqtt, rest

class RaptorClient():
    '''
    This class is an interface to Raptor
    '''
    default_config = {
        "global": {
            "username": None,
            "password": None,
        },
        "mqtt": mqtt.MqttClient.default_config,
        "rest": rest.RestClient.default_config
    }

    def __init__(self, config):
        '''
        Initializes the clients for raptor, passing them the needed config

        Note that you have to provide valid credentials for raptor if needed 

        config = {
            "global": { #informations shared between the clients
                "username": "user",
                "password": "pass",
            },
            "mqtt": {#data for configuring the mqtt client, see raptorpy.clients.mqtt }
            "rest": {#data for configuring the rest client, see raptorpy.clients.rest }
        }
        '''

        self.config = RaptorClient.default_config
        if config:
            for k, v in config.iteritems():
                self.config[k] = v

        self.rest_client  = None
        self.mqtt_client  = None

    def getRestClient(self):
        '''
        Returns the instance of the RestClient contained in RaptorClient
        '''
        if not self.rest_client:
            rest_configs = config["global"]
            rest_configs.update(config['rest'])

            self.rest_client = mqtt.RestClient(rest_configs)

        return self.rest_client

    def getMqttClient(self):
        '''
        Returns the instance of the MqttClient contained in RaptorClient
        '''
        if not self.mqtt_client:
            mqtt_configs = config["global"]
            mqtt_configs.update(config['mqtt'])

            self.mqtt_client = mqtt.MqttClient(mqtt_configs)

        return self.mqtt_client

    def connectMqttClient(self):
        '''
        Start the mqtt client and connect it to the provided url from configurations
        '''
        mqtt = self.getMqttClient()
        mqtt.connect()
