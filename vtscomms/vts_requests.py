

import os, sys, json, secrets, string
from log import ws_logger as logging
from vtscomms import ws as websocket

# TODO convert logging
class VTSRequests:
    def __init__(self):
        self.auth_token: string = ""
        self.url = "ws://localhost:8001"        
        self.websocket = websocket.WebSocketConnection(self.url)

        # websocket.enableTrace(True)
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


    def _base_payload(self, req_type: str, req_id: str = secrets.token_hex(32)):
        request_payload = {
            "apiName": self.plugin_config["apiName"],
            "apiVersion": self.plugin_config["apiVersion"],
            "requestID": req_id,
            "messageType": req_type,
            "data": {}
        }
        return request_payload
    
    def _standard_payload(self, req_type: str, req_id: str = secrets.token_hex(32)):
        request_payload = self._base_payload(req_type, req_id)
        request_payload["data"].update({
            "pluginName": self.plugin_config["pluginName"],
            "pluginDeveloper": self.plugin_config["pluginDeveloper"]
        })
        return request_payload

    async def check_status(self):
        type = "APIStateRequest"
        msg = json.dumps(self._standard_payload(type))
        print("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive() 
        print("$$ {} response:\n{}".format(type, response))        


    async def _get_auth_token(self):
        type = "AuthenticationTokenRequest"
        msg = json.dumps(self._standard_payload(type))
        print("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive() 
        print("$$ {} response:\n{}".format(type, response))

        result = json.loads(response)
        if "data" in result:
            data = result["data"]
            if "authenticationToken" in data:
                self.auth_token = data["authenticationToken"]
            elif "errorID" in result:
                print("Error ID: {}, message: {}".format(data["errorID"], data["message"]))
            else:
                print("Something went terribly wrong during authentication")

    # TODO check if valid auth and existing authtoken before generating a new token
    async def authenticate(self):
        if not self.auth_token:
            await self._get_auth_token()
        else:
            return
        type = "AuthenticationRequest"
        dict_msg = self._standard_payload(type)
        dict_msg["data"].update({"authenticationToken": self.auth_token })
        msg = json.dumps(dict_msg)
        print("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive() 
        print("$$ {} response:\n{}".format(type, response))

        result = json.loads(response)
        if "data" in result:
            data = result["data"]
            if data["authenticated"] is False:
                logging.warning("Failed to authenticate")
            else:
                logging.info("Authenticated session")

    def get_current_model(self):
        msg = self._standard_payload("CurrentModelRequest")
        print("$$ CurrentModelRequest request message: \n" + json.dumps(msg))
        ws = self.get_ws()
        ws.send(json.dumps(msg))
        result = ws.recv()
        print("$$ CurrentModelRequest respone: \n" + result)
        response = json.loads(result)
        if "data" in response:
            data = response["data"]
        else:
            print("No data found during CurrentModelRequest")
        ws.close()

##  SHIIITT THIS WONT WORK, I NEED A KEEPALIVE WEBSOCKET CONNECTIO NRAAAGHH
