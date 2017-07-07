import requests
import logging


####DEBUG
from pprint import pprint as pp
####DEBUG

def parse_return(func):
    def wrapper(restClient, *args, **kwargs):
        attempts = 0
        while(attempts<2):
            response = func(restClient, *args, **kwargs)
            if response.ok:
                if response.text:
                    return response.json()
                else:
                    return True
            else:
                if response.status_code == 401: #maybe the token has expired => try to login again
                    if restClient.login() and attempts<1:
                        attempts+=1 #Attempt only one time to login
                    else:
                        return response.status_code
                else:
                    return response.status_code
    return wrapper

# def http_request(method):
#     def decorator(func):
#         def wrapper(restClient, location, data, *args, **kwargs):
#             '''
#             sends data to raptorbox with the given method
#             it sets also the authorization header
#
#             returns the Response
#             '''
#             restClient, method, location, data
#             method = getattr(requests, method)
#             header = None
#             if hasattr(restClient, "token"):
#                 header = {"Authorization": "Bearer {}".format(restClient.token)}
#
#             return method(
#                 "{}{}".format(restClient.config["url"], location),
#                 json=data,
#                 headers=header if header else None)
#         return wrapper
#     return decorator

class RestClient:
    default_config = {
        "url": "https://api.raptorbox.eu",
        "routes": {
            "login":            "auth/login",
            "device_search":    "search"
            "device":           "{device_id}",
            "device_tree":      "{device_id}/tree/{children_id}",
            "event":            "{device_id}/streams/{stream_name}",
            "actions":          "{device_id}/actions/{action_id}",
            "stream":           "{device_id}/stream/{stream}",
            "stream_list":      "{device_id}/stream/{stream}/list", #FIXME missing /
            "stream_search":    "{device_id}/stream/{stream}/search", #FIXME missing /
        }
    }

    def __init__(self, config):
        '''
        creates a RestClient for raptorbox, inside config username and password should be provided
        when the object is created it logs to specified url(or default) and sets the token
        '''
        self.config = RestClient.default_config
        if config:
            for k, v in config.iteritems():
                self.config[k] = v

        self.config["url"] += "" if self.config["url"][-1] == "/" else "/" #add a / at the end of the url if not present
        self.token = None
        # if self.login():
        #     #login succeded, got token
        #     logging.debug("Token: {}".format(self.token))
        # else:
        #     ##Authentication error TODO maybe it's better to define a custom error
        #     raise RuntimeError("Unable to authenticate @{}{}".format(self.config["url"], self.config["routes"]["login"]))

    def login(self):
        '''
        log the client toward raptorbox specified url

        returns True if logged correctly
                False otherwise
        '''
        res = self.post(
            self.config["routes"]["login"],
            {
                "username": self.config["username"],
                "password": self.config["password"]
            }
        )

        if res:
            res_json = res.json()
            self.token = res_json["token"]

            return True
        else:
            return False

    @parse_return
    def getDevicesList(self, offset=None, limit=None, **kwargs):
        '''
        Get the list of the devices defined in raptorbox
        '''
        return self.get(
            self.config["routes"]["device"].format(device_id=""),
            # {"offset": offset, "limit": limit} #TODO check if this is correctly placed inside of get parameters
            **kwargs
        )

    @parse_return
    def getDeviceDefinition(self, device_id, **kwargs): #TODO test
        '''
        Get the Definition of the device with device_id
        '''
        return self.get(
            self.config["routes"]["device"].format(device_id=device_id),
            **kwargs)

    @parse_return
    def searchDeviceDefinition(self, query, **kwargs): #TODO test
        '''
        Search for a device definition

        Query structure:
        ``
        {
            "index": "string",
            "type": "string",
            "limit": 0,
            "offset": 0,
            "sort": {
                "sort": "ASC",
                "field": "string"
            },
            "search": "string",
            "name": "string",
            "description": "string",
            "customFields": {
                "additionalProp1": {},
                "additionalProp2": {},
                "additionalProp3": {}
            }
        }
        ``
        '''
        args = locals()
        data = {}

        for arg, val in args.iteritems():
            if val and val != self:
                data[arg] = val

        return self.post(
            self.config["routes"]["device_search"],
            query,
            **kwargs
        )

    @parse_return
    def createDevice(self, name, description=None, streams=None, customFields=None, actions=None, **kwargs):
        '''
        Create a new device specifing fields according to raptorbox apis
        returns the response json data
        '''
        args = locals()
        data = {}

        for arg, val in args.iteritems():
            if val and val != self:
                data[arg] = val

        return self.post(
                self.config["routes"]["device"].format(device_id=""),
                data,
                **kwargs
            )

    @parse_return
    def updateDevice(self, device_id, name=None, description=None, streams=None, customFields=None, actions=None, **kwargs):
        '''
        Update an existing device

        returns the response json data
        '''
        args = locals()
        data = {}

        for arg, val in args.iteritems():
            if val and val != self:
                data[arg] = val

        return self.put(
                self.config["routes"]["device"].format(device_id=device_id),
                data,
                **kwargs
            )

    @parse_return
    def deleteDevice(self, device_id, **kwargs):
        '''
        Delete a device definition if any

        returns true if it went ok, False otherwise
        '''
        return self.delete(
            self.config["routes"]["device"].format(device_id=device_id),
            **kwargs
        )

    @parse_return
    def pushEvent(self, device_id, stream_name, event, **kwargs):
        '''
        push an evet to raptorbox

        returns the response json data
        '''
        return self.put(
            self.config["routes"]["event"].format(device_id=device_id, stream_name=stream_name),
            event,
            **kwargs
        )

    @parse_return
    def getDeviceChildren(self, device_id, **kwargs): #TODO test
        '''
        Get all the device children of the given device_id
        '''
        return self.get(self.config["routes"]["device_tree"].format(device_id=device_id, children_id=""))

    @parse_return
    def setChildrenDevices(self, device_id, devices, **kwargs): #TODO test
        '''
        Set a list of devices as children of device_id
        '''
        #TODO ask for clarification about devices parameter meaning and return value
        return self.post(
            self.config["routes"]["device_tree"].format(device_id=device_id, children_id=""),
            devices,
            **kwargs
        )

    @parse_return
    def addChildrenDevice(self, device_id, children_id, **kwargs): #TODO test
        '''
        add a device with children_id to device_id children
        '''
        return self.put(
            self.config["routes"]["device_tree"].format(device_id=device_id, children_id=children_id),
            devices,
            **kwargs
        )

    @parse_return
    def removeChildrenDevice(self, device_id, children_id, **kwargs): #TODO test
        '''
        Remove a device with children_id from device_id children
        '''
        return self.delete(
            self.config["routes"]["device_tree"].format(device_id=device_id, children_id=children_id),
            devices,
            **kwargs
        )

    @parse_return
    def getActions(self, device_id, **kwargs):
        '''
        Returns the list of actions definition
        '''
        return self.get(
            self.config["routes"]["actions"].format(device_id=device_id, action_id=""),
            **kwargs
        )

    @parse_return
    def getActionState(self, device_id, action_id, **kwargs):
        '''
        Returns the status of an action
        '''
        return self.get(
            self.config["routes"]["actions"].format(device_id=device_id, action_id=action_id),
            **kwargs
        )


    @parse_return
    def setActionState(self, device_id, action_id, state, **kwargs):
        '''
        Returns the status of an action
        '''
        return self.post(
            self.config["routes"]["actions"].format(device_id=device_id, action_id=action_id),
            state,
            **kwargs
        )

    @parse_return
    def deleteActionState(self, device_id, action_id, **kwargs):
        '''
        Returns the status of an action
        '''
        return self.delete(
            self.config["routes"]["actions"].format(device_id=device_id, action_id=action_id),
            **kwargs
        )

    @parse_return
    def listChannels(self, device_id, **kwargs):
        '''
        returns a list of the defined channels
        '''
        return self.get(
            self.config["routes"]["stream"].format(device_id=device_id, stream=""),
            **kwargs
        )

    @parse_return
    def getLastRecordFrom(self, device_id, stream, **kwargs):
        '''
        Returns the last record from a stream
        '''
        return self.get(
            self.config["routes"]["stream"].format(device_id=device_id, stream=stream),
            **kwargs
        )

    @parse_return
    def storeRecordTo(self, device_id, stream, record, **kwargs):
        '''
        Returns the last record from a stream
        '''
        return self.put(
            self.config["routes"]["stream"].format(device_id=device_id, stream=stream),
            record,
            **kwargs
        )

    @parse_return
    def removeRecordsFrom(self, device_id, stream, **kwargs):
        '''
        Returns the last record from a stream
        '''
        return self.delete(
            self.config["routes"]["stream"].format(device_id=device_id, stream=stream),
            **kwargs
        )

    @parse_return
    def getRecords(self, device_id, stream, **kwargs):
        '''
        Return all the records sorted from the more recent

        he maximum amount of data that can be returned per request is 1000 records.
        Use the pagination modifiers in the query (offset and limit) to control the data retrieval.
        '''
        return self.get(
            self.config["routes"]["stream_list"].format(device_id=device_id, stream=stream),
            **kwargs
        )

    def searchForRecords(self, device_id, stream, query, **kwargs):
        '''
        Search on a stream for records matching the query.
        ==================================================

        Query structure
        ``
        {
            "index": "string",
            "type": "string",
            "limit": 0,
            "offset": 0,
            "sort": {
                "sort": "ASC",
                "field": "string"
            },
            "queryList": [
                null
            ],
            "numericrange": true,
            "numericrangefrom": 0,
            "numericrangeto": 0,
            "timerange": true,
            "timerangefrom": 0,
            "timerangeto": 0,
            "numericrangefield": "string",
            "limitcount": 0,
            "geodistance": true,
            "pointlat": 0,
            "pointlon": 0,
            "geodistancevalue": 0,
            "geodistanceunit": "inches",
            "geoboundingbox": true,
            "geoboxupperleftlat": 0,
            "geoboxupperleftlon": 0,
            "geoboxbottomrightlat": 0,
            "geoboxbottomrightlon": 0,
            "match": true,
            "matchfield": "string",
            "matchstring": "string"
        }
        ``
        '''
        args = locals()
        data = {}

        for arg, val in args.iteritems():
            if val and val != self:
                data[arg] = val

        return self.post(
            self.config["routes"]["stream_search"].format(device_id=device_id, stream=stream),
            query,
            **kwargs
        )

    def http_request(self, method, location, data=None, **kwargs):
        '''
        sends data to raptorbox with the given method
        it sets also the authorization header

        returns the Response
        '''
        method = getattr(requests, method)
        header = None
        if self.token:
            header = {"Authorization": "Bearer {}".format(self.token)}

        def url_parameters():
            res = {k:kwargs["params"][k] for k in ('limit','offset') if k in kwargs}
            return res if res else None

        return method(
            "{}{}".format(self.config["url"], location),
            json=data,
            headers=header,
            params=url_parameters())

        ###DEBUG
        # def ppr(req):
        #     """
        #     At this point it is completely built and ready
        #     to be fired; it is "prepared".
        #
        #     However pay attention at the formatting used in
        #     this function because it is programmed to be pretty
        #     printed and may differ from the actual request.
        #     """
        #     print('{}\n{}\n{}\n\n{}\n{}'.format(
        #         '-----------START-----------',
        #         req.method + ' ' + req.url,
        #         '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        #         req.body,
        #         '------------END------------'
        #     ))
        #
        # req = requests.Request(method.upper(),
        #     "{}{}".format(self.config["url"], location),
        #     json=data,
        #     headers=header if header else None)
        #
        # prep = req.prepare()
        # ppr(prep)
        # s = requests.Session()
        # resp = s.send(prep)
        #
        # return resp
        # ###DEBUG

    def put(self, location, data=None, **kwargs):
        '''
        sends data to raptorbox with put method
        it sets also the authorization header

        returns the Response
        '''
        return self.http_request("put", location, data, **kwargs)

    def post(self, location, data=None, **kwargs):
        '''
        sends data to raptorbox with post method
        it sets also the authorization header

        returns the Response
        '''
        return self.http_request("post", location, data, **kwargs)

    def get(self, location, data=None, **kwargs):
        '''
        sends data to raptorbox with get method
        it sets also the authorization header

        returns the Response
        '''
        return self.http_request("get", location, data, **kwargs)

    def delete(self, location, data=None, **kwargs):
        '''
        sends data to raptorbox with delete method
        it sets also the authorization header

        returns the Response
        '''
        return self.http_request("delete", location, data, **kwargs)
