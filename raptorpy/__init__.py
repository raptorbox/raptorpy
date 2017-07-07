'''
RaptorPY Client
===============

RaptorPy is a client library for Raptor <https://github.com/raptorbox/raptor>

RaptorClient class provides an interface to mqtt(MqttClient) and a restfull api(RestClient).
According to Raptor implementation the mqtt client is used for mangling events
while the rest apis are provided for handling the data structure used by raptor and
for publishing events. For more informations see raptory.clients module
'''

import raptor_client
