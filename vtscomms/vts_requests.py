

import os, sys, json, secrets, string, asyncio
from log import ws_logger as logging
from vtscomms import ws as websocket

# TODO convert logging
# TODO maybe allow for catching auth instead of first auth. Allow each function to auto auth.
class VTSRequests:
    def __init__(self):
        self.auth_token: string = ""
        self.model_id: string = ""
        self.url = "ws://localhost:8001"        
        self.websocket = websocket.WebSocketConnection(self.url)
        self.attempted_first_auth = False
        self.reload_model_on_fail = False
        self.reload_model_attempts = 0

        self.plugin_config = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "pluginName": "VTS-Shapeshift",
                "pluginDeveloper": "Randy Panopio"}

        # TODO update me when releasing, do not use debug config
        config_filename = "VTS-Shapeshift/files/images/debug_config.json"
        # config_filename = "VTS-Shapeshift/files/images/plugin_config.json"
        if os.path.isfile(config_filename):
            with open(config_filename) as file_handler:
                try:
                    json_dict = json.loads(file_handler.read())
                    if json_dict["plugin_config"]:
                        self.plugin_config = json_dict["plugin_config"]
                    if json_dict["cached_auth_token"]:
                        self.auth_token = json_dict["cached_auth_token"]
                    if json_dict["plugin_settings"]:
                        self.reload_model_on_fail = json_dict["plugin_settings"]["reload_model_on_fail"]
                except Exception as e:
                    print(e)
    
    def _standard_payload(self, req_type: str, req_id: str = secrets.token_hex(32)):
        request_payload = {
            "apiName": self.plugin_config["apiName"],
            "apiVersion": self.plugin_config["apiVersion"],
            "requestID": req_id,
            "messageType": req_type,
            "data": {
                "pluginName": self.plugin_config["pluginName"],
                "pluginDeveloper": self.plugin_config["pluginDeveloper"]
            }
        }
        return request_payload

    async def check_status(self):
        type = "APIStateRequest"
        msg = json.dumps(self._standard_payload(type))
        print("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive() 
        print("$$ {} response:\n{}".format(type, response))
        return json.loads(response)  

    async def _get_auth_token(self):
        type = "AuthenticationTokenRequest"
        msg = json.dumps(self._standard_payload(type))
        print("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive() 
        print("$$ {} response:\n{}".format(type, response))

        if not result:
            return
        result = json.loads(response)
        if "data" in result:
            data = result["data"]
            if "authenticationToken" in data:
                self.auth_token = data["authenticationToken"]
            elif "errorID" in result:
                print("Error ID: {}, message: {}".format(data["errorID"], data["message"]))
            else:
                print("Something went terribly wrong during authentication")

    async def authenticate(self):
        status = await self.check_status()
        if "data" in status:
            if status["data"]["currentSessionAuthenticated"] is True:
                print("Current session is already authenticated")
                return
        if not self.auth_token:
            await self._get_auth_token()
        type = "AuthenticationRequest"
        dict_msg = self._standard_payload(type)
        dict_msg["data"].update({"authenticationToken": self.auth_token })
        msg = json.dumps(dict_msg)
        print("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive() 
        print("$$ {} response:\n{}".format(type, response))

        if not result:
            return
        result = json.loads(response)
        if "data" in result:
            data = result["data"]
            if data["authenticated"] is False:
                logging.warning("Failed to authenticate")
            else:
                logging.info("Authenticated session")

    async def get_current_model_id(self):
        type = "CurrentModelRequest"
        msg = json.dumps(self._standard_payload(type))
        print("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive() 
        print("$$ {} response:\n{}".format(type, response))

        if not result:
            return
        result = json.loads(response)
        if "data" in result:
            data = result["data"]
            self.model_id = data["modelID"]
        return self.model_id
    
    async def reload_current_model(self):
        if not self.model_id:
            await self.get_current_model_id()

        type = "ModelLoadRequest"
        dict_msg = self._standard_payload(type)
        dict_msg["data"].update({"modelID": self.model_id })
        msg = json.dumps(dict_msg)
        print("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive() 
        print("$$ {} response:\n{}".format(type, response))

        if not result:
            return
        result = json.loads(response)
        if "data" in result:
            data_dict = result["data"]
            if "errorID" in data_dict:
                print("Error ID: {}, message: {}".format(data_dict["errorID"], data_dict["message"]))
                if data_dict["errorID"] == 153 and self.reload_model_on_fail:
                    print("watta")
                    if self.reload_model_attempts >= 4:
                        print("Maxed out auto reload model attempts. Something went wrong")
                    else:                            
                        # hit 2 second cooldown, wait buffer time before attempting again.
                        await asyncio.sleep(2.5)
                        self.reload_model_attempts += 1
                        await self.reload_current_model()
            else:
                self.reload_model_attempts = 0

