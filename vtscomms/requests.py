import os, sys, json, secrets, websocket, string
from log import ws_logger as logging

# TODO cleanup, maybe refactor to be async? - websocket seems like does not mesh well with this, and websocket already seems slow :( sadge
# TODO centralize websocket connection, maybe one separate for startup, and a keepalive during main session
"""
    Steps:
    - get websocket client running
    - get ws client to connect to vts
"""
class VTSRequests:
    def __init__(self):
        self.auth_token: string = ""
        # self.web_socket = websocket.WebSocketApp("ws://localhost:8001")
        config_filename = "VTS-Shapeshift/files/images/plugin_config.json"
        if os.path.isfile(config_filename):
            with open(config_filename) as file_handler:
                raw_config = file_handler.read()
                try:
                    self.plugin_config = json.loads(raw_config)
                except:
                    self.plugin_config = self._default_plugin_config()
        else:
            self.plugin_config = self._default_plugin_config()
        
    def _default_plugin_config(self):
        return {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": "1.0",
                    "pluginName": "VTS-Shapeshift",
                    "pluginDeveloper": "Randy Panopio"}

    def init_websocket(self):
        try:
            websocket.enableTrace(True)
            self.url = "ws://localhost:8001"
            logging.info("Initializing websocket :" + self.url)
            self.ws = websocket.WebSocketApp(self.url,
                                            on_message = lambda ws,msg: self.on_message(ws, msg)
                                            # on_error = lambda ws, msg: self.on_error(ws, msg),
                                            # on_close = lambda ws: self.on_close(ws),
                                            # on_open = lambda ws: self.on_open(ws),
                                            )
            self.ws.run_forever(reconnect=5)
            logging.info("Initalized websocket connection to port: " + self.url)
        except Exception as e:
            logging.error("failed to initialize websocket connection: " +str(e))

    def on_error(self, ws, message):
        logging.error("Websocket: {}, recieved error: {}".format(ws.url, message))

    def on_open(self, ws):
        logging.info("Websocket: {} connection opened: {}".format(ws.url))

    def on_close(self, ws):
        logging.info("Websocket: {} connection closed: {}".format(ws.url))
        #TODO add check for reconnection, but probably not needed since most likely an intentional ws disconnect             

    def on_message(self, ws, message):
        logging.info("Websocket: {}, recieved message: {}".format(ws.url, message))
        response = json.loads(message)

        type = response["messageType"]        
        if response:
            if type == "APIStateRequest":
                # self.check_status()
                logging.info("check status response\n" + message)
            elif type == "AuthenticationTokenRequest":
                logging.info("get auth token response\n" + message)
                if "data" in response:
                    data = response["data"]
                    if "authenticationToken" in data:
                        self.auth_token = data["authenticationToken"]
                    elif "errorID" in response:
                        logging.error("Error ID: {}, message: {}".format(data["errorID"], data["message"]))
                    else:
                        logging.error("Something went terribly wrong during authentication")
            elif type == "AuthenticationTokenRequest": 
                logging.info("authenticate response\n" + message)
                if "data" in response:
                    data = response["data"]
                    if data["authenticated"] is False:
                        logging.warning("failed to authenticate")
                    else:
                        logging.info("Authenticated session")
            else:
                logging.warning("Recieved unknown message from ws {} message:\n{}".format(ws.url, message))

    def check_status(self):
        msg = self.standard_payload("APIStateRequest")
        self.ws.send(json.dumps(msg))

    def get_auth_token(self):
        msg = self.standard_payload("AuthenticationTokenRequest")
        self.ws.send(json.dumps(msg))

    def authenticate(self, auth_token: string):
        msg = self.standard_payload("AuthenticationTokenRequest")
        msg["data"].update({"authenticationToken": auth_token })
        self.ws.send(json.dumps(msg))

    def base_payload(self, req_type: str, req_id: str = secrets.token_hex(32)):
        request_payload = {
            "apiName": self.plugin_config["apiName"],
            "apiVersion": self.plugin_config["apiVersion"],
            "requestID": req_id,
            "messageType": req_type,
            "data": {}
        }
        return request_payload
    
    def standard_payload(self, req_type: str, req_id: str = secrets.token_hex(32)):
        request_payload = self.base_payload(req_type)
        request_payload["data"].update({
            "pluginName": self.plugin_config["pluginName"],
            "pluginDeveloper": self.plugin_config["pluginDeveloper"]
        })
        return request_payload


# ================================================================================================================ 
    def test(self):
        self.init_websocket()
        # self.check_status()
        self.get_auth_token()
        # self.check_status()
        # self.authenticate(self.auth_token)
        # self.check_status()
        