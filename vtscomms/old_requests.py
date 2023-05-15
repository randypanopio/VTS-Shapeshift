# # TODO delete me, single use ws does not work

# import os, sys, json, secrets, websocket, string
# from log import ws_logger as logging

# # TODO cleanup, maybe refactor to be async? - websocket seems like does not mesh well with this, and websocket already seems slow :( sadge
# # TODO centralize websocket connection, maybe one separate for startup, and a keepalive during main session
# # - turns out I need to learn a lot about websockets if I want to do this. Keeping the dirty way for now
# """
#     Steps:
#     - get websocket client running
#     - get ws client to connect to vts
# """

# class VTSRequests:
#     def __init__(self):
#         self.auth_token: string = ""
#         self.url = "ws://localhost:8001"

#         # websocket.enableTrace(True)
#         config_filename = "VTS-Shapeshift/files/images/plugin_config.json"
#         if os.path.isfile(config_filename):
#             with open(config_filename) as file_handler:
#                 raw_config = file_handler.read()
#                 try:
#                     self.plugin_config = json.loads(raw_config)
#                 except:
#                     self.plugin_config = self._default_plugin_config()
#         else:
#             self.plugin_config = self._default_plugin_config()
        
#     def _default_plugin_config(self):
#         return {
#                     "apiName": "VTubeStudioPublicAPI",
#                     "apiVersion": "1.0",
#                     "pluginName": "VTS-Shapeshift",
#                     "pluginDeveloper": "Randy"}

#     def get_ws(self):
#         ws = websocket.WebSocket()
#         ws.connect(self.url)
#         return ws

#     def check_status(self):
#         msg = self._standard_payload("APIStateRequest")
#         print("$$ APIStateRequest request message: \n" + json.dumps(msg))
#         ws = self.get_ws()
#         ws.send(json.dumps(msg))
#         result = ws.recv()
#         print("$$ APIStateRequest response: \n" + result)
#         ws.close()

#     # TODO check if authtoken exists and check if current sess is validated before trying to get a new token
#     def _get_auth_token(self):
#         msg = self._standard_payload("AuthenticationTokenRequest")
#         print("$$ AuthenticationTokenRequest request message: \n" + json.dumps(msg))
#         ws = self.get_ws()
#         ws.send(json.dumps(msg))
#         result = ws.recv()
#         print("$$ AuthenticationTokenRequest response: \n" + result)
#         response = json.loads(result)
#         if "data" in response:
#             data = response["data"]
#             if "authenticationToken" in data:
#                 self.auth_token = data["authenticationToken"]
#             elif "errorID" in response:
#                 print("Error ID: {}, message: {}".format(data["errorID"], data["message"]))
#             else:
#                 print("Something went terribly wrong during authentication")
#         else:
#             print("No data found during get auth token request")
#         ws.close()

#     def authenticate(self):
#         self._get_auth_token()
#         msg = self._standard_payload("AuthenticationRequest")
#         msg["data"].update({"authenticationToken": self.auth_token })
#         print("$$ AuthenticationRequest request message: \n" + json.dumps(msg))
#         ws = self.get_ws()
#         ws.send(json.dumps(msg))
#         result = ws.recv()
#         print("$$ AuthenticationRequest respone: \n" + result)
#         response = json.loads(result)
#         if "data" in response:
#             data = response["data"]
#             if data["authenticated"] is False:
#                 logging.warning("Failed to authenticate")
#             else:
#                 logging.info("Authenticated session")
#         else:
#             print("No data found during AuthenticationRequest")
#         ws.close()

#     def get_current_model(self):
#         msg = self._standard_payload("CurrentModelRequest")
#         print("$$ CurrentModelRequest request message: \n" + json.dumps(msg))
#         ws = self.get_ws()
#         ws.send(json.dumps(msg))
#         result = ws.recv()
#         print("$$ CurrentModelRequest respone: \n" + result)
#         response = json.loads(result)
#         if "data" in response:
#             data = response["data"]
#         else:
#             print("No data found during CurrentModelRequest")
#         ws.close()        


#     def _base_payload(self, req_type: str, req_id: str = secrets.token_hex(32)):
#         request_payload = {
#             "apiName": self.plugin_config["apiName"],
#             "apiVersion": self.plugin_config["apiVersion"],
#             "requestID": req_id,
#             "messageType": req_type,
#             "data": {}
#         }
#         return request_payload
    
#     def _standard_payload(self, req_type: str, req_id: str = secrets.token_hex(32)):
#         request_payload = self._base_payload(req_type, req_id)
#         request_payload["data"].update({
#             "pluginName": self.plugin_config["pluginName"],
#             "pluginDeveloper": self.plugin_config["pluginDeveloper"]
#         })
#         if self.auth_token:
#             request_payload["data"].update({"authenticationToken": self.auth_token })
#         return request_payload

# ##  SHIIITT THIS WONT WORK, I NEED A KEEPALIVE WEBSOCKET CONNECTIO NRAAAGHH
