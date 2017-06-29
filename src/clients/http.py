import requests

class RestClient:
    default_config = {
        "url": "https://api.raptorbox.eu",
        "routes": {
            "login": "auth/login",
            "device": "{device_id}",
            "event": "{device_id}/streams/{stream_name}",
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

        if self.login():
            #login succeded, got token
            print("Token: {}".format(self.token))
        else:
            ##Authentication error TODO maybe it's better to define a custom error
            raise RuntimeError("Unable to authenticate @{}{}".format(self.config["url"], self.config["routes"]["login"]))

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

    def create_device(self, name, description, streams, customFields, actions):
        '''
        Create a new device specifing fields according to raptorbox apis
        returns the response json data
        '''
        data = {
            "name": name,
            "description": description,
            "streams": streams,
            "customFields": customFields,
            "actions": actions,
        }

        return self.post(
                self.config["routes"]["device"].format(device_id=""),
                data
            ).json()

    def update_device(self, device_id, name, description, streams, customFields, actions):
        '''
        Update an existing device

        returns the response json data
        '''
        data = {
            "name": name,
            "description": description,
            "streams": streams,
            "customFields": customFields,
            "actions": actions,
        }

        return self.put(
                self.config["routes"]["device"].format(device_id=device_id),
                data
            ).json()

    def push_event(self, device_id, stream_name, event):
        '''
        push an evet to raptorbox

        returns the response json data
        '''
        return self.put(
                self.config["routes"]["event"].format(device_id=device_id, stream_name=stream_name),
                event
            ).json()


    def message(self, method, location, data):
        '''
        sends data to raptorbox with the given method
        it sets also the authorization header

        returns the Response
        '''
        method = getattr(requests, method)
        header = None
        if hasattr(self, "token"):
            header = {"Authorization": "Bearer | {}".format(self.token)}

        return method(
            "{}{}".format(self.config["url"], location),
            json=data,
            headers=header if header else None) #TODO chek if this work

    def put(self, location, data):
        '''
        sends data to raptorbox with put method
        it sets also the authorization header

        returns the Response
        '''
        return self.message("put", location, data)

    def post(self, location, data):
        '''
        sends data to raptorbox with post method
        it sets also the authorization header

        returns the Response
        '''
        return self.message("post", location, data)
