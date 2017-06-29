from paho.mqtt.client import Client

class MqttClient():
    default_config = {
        "host": "api.raptorbox.eu",
        "port": 1883,
    }

    def __init__(self, config):
        '''
        Initialize information for the client

        provide configurations as parameter, if None provided the configurations would be defaults

        see MqttClient.default_config for configurations format
        '''
        self.config = MqttClient.default_config
        if config:
            for k, v in config.iteritems():
                self.config[k] = v

        self.mqtt_client = Client()
        self.mqtt_client.username_pw_set(config["username"], config["password"])

        if "reconnect_min_delay" in config and "reconnect_max_delay" in config:
            self.mqtt_client.reconnect_delay_set(
                config["reconnect_min_delay"],
                config["reconnect_max_delay"],)
        # self.mqtt_client.tls_set()
        self.mqtt_client.enable_logger()


    def connect(self): #TODO consider srv field in dns
        '''
        connect the client to mqtt server with configurations provided by constructor
        and starts listening for topics
        '''
        self.mqtt_client.connect(self.config["host"], self.config["port"])

        self.mqtt_client.loop_start()

    def subscribe(self, topic, callback):
        '''
        register 'callback' to "topic". Every message will be passed to callback in order to be executed
        '''
        self.mqtt_client.message_callback_add(topic, callback)

    def unsubscribe(self, topic):
        '''
        unsubscribe to topic

        topic could be either a string or al list of strings containing to topics to unsubscribe to.

        Returns a tuple (result, mid), where result is MQTT_ERR_SUCCESS
        to indicate success or (MQTT_ERR_NO_CONN, None) if the client is not
        currently connected.
        mid is the message ID for the unsubscribe request. The mid value can be
        used to track the unsubscribe request by checking against the mid
        argument in the on_unsubscribe() callback if it is defined.
        '''
        return self.mqtt_client.unsubscribe(topic)

    def disconnect(self):
        '''
        Disconnects from the server
        '''
        self.mqtt_client.disconnect()

    def reconnect(self):
        '''
        reconnects after a disconnection, this could be called after connection only
        '''
        self.mqtt_client.reconnect()
