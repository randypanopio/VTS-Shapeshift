import json, secrets, string, asyncio, threading
from m_utils import log as logging
from comms import ws as websocket

class VT_Requests():
    def __init__(self, config_data, new_model_handler = None):
        self.model_id: string = ""
        self.model_data = None
        self.new_model_handler = new_model_handler
        self.connected = False
        self.attempted_first_auth = False
        self.reload_model_attempts = 0

        self.thread = threading.current_thread()
        self.thread.name = self.thread.name + " - VT_Requests_Thread"

        # Prefil from config
        self.plugin_config = config_data["plugin_config"]
        self.auth_token = config_data["cached_auth_token"]
        self.reload_model_on_fail = config_data["plugin_settings"]["reload_model_on_fail"]
        self.update_data_on_new_model = config_data["plugin_settings"]["update_data_on_new_model"]
        base = config_data["plugin_settings"]["ws_base_url"]
        port = config_data["plugin_settings"]["ws_port"]
        self.url = "{0}{1}{2}".format(base, ":" if not base.endswith(":") else "", port)

        # Create and set up a new event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    async def connect_websocket(self):
        logging.ws_logger.info("creating websocket connection")
        self.websocket = websocket.WebSocketConnection(self.url)
        self.loop.create_task(self.websocket.connect())

    # Use me for functionality that modifies model/scene. Rather than creating listeners for model updates,
    # this is a clean way of updating following requests based on changes, or blocking invalid requests.
    async def validate_model(self):
        type = "CurrentModelRequest"
        msg = json.dumps(self._standard_payload(type))
        logging.ws_logger.info("Validating Model Data")
        logging.ws_logger.info("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive()
        logging.ws_logger.info("$$ {} response:\n{}".format(type, response))

        if not response:
            return False
        result = json.loads(response)
        if "data" in result:
            self.model_id == result["data"]["modelID"] # model has not changed
            return True
        else:
            if self.update_data_on_new_model:
                await self.request_model_data()
                self.new_model_event()
                return True
            else:
                self.new_model_event() #trigger anyways, but dont force model reload
        return False

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
        logging.ws_logger.info("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive()
        if response:
            logging.ws_logger.info("$$ {} response:\n{}".format(type, response))
            return json.loads(response)
        else:
            logging.ws_logger.info("Unable to talk to VTS, app likely offline")
            return

    async def _get_auth_token(self):
        type = "AuthenticationTokenRequest"
        msg = json.dumps(self._standard_payload(type))
        logging.ws_logger.info("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive()
        logging.ws_logger.info("$$ {} response:\n{}".format(type, response))

        if not response:
            return
        result = json.loads(response)
        if "data" in result:
            data = result["data"]
            if "authenticationToken" in data:
                self.auth_token = data["authenticationToken"]
            elif "errorID" in result:
                logging.ws_logger.error("Error ID: {}, message: {}".format(data["errorID"], data["message"]))
            else:
                logging.ws_logger.error("Something went terribly wrong during authentication")

    async def authenticate(self):
        status = await self.check_status()
        if not status:
            self.connected = False
            return False
        if "data" in status:
            if status["data"]["currentSessionAuthenticated"] is True:
                self.connected = True
                logging.ws_logger.info("Already Authenticated")
                return True
            else:
                self.connected = False

        if not self.auth_token:
            await self._get_auth_token()
        type = "AuthenticationRequest"
        dict_msg = self._standard_payload(type)
        dict_msg["data"].update({"authenticationToken": self.auth_token })
        msg = json.dumps(dict_msg)
        logging.ws_logger.info("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive()
        logging.ws_logger.info("$$ {} response:\n{}".format(type, response))

        if not response:
            logging.ws_logger.warning("Unnable to authenticate")
            self.auth_token = ""
            self.connected = False
            return False
        result = json.loads(response)
        if "data" in result:
            data = result["data"]
            if data["authenticated"]:
                self.connected = True
                return True
        logging.ws_logger.warning("Failed to authenticate")
        self.auth_token = ""
        self.connected = False
        return False

    async def request_model_data(self):
        type = "CurrentModelRequest"
        msg = json.dumps(self._standard_payload(type))
        logging.ws_logger.info("$$ {} request message:\n{}".format(type, msg))
        await self.websocket.send(msg)
        response = await self.websocket.receive()
        logging.ws_logger.info("$$ {} response:\n{}".format(type, response))

        if not response:
            return None
        result = json.loads(response)
        if "data" in result:
            self.model_data = result["data"]
            self.model_id = result["data"]["modelID"]
        return self.model_data

    # region Live functions - AKA functions used post init
    async def reload_current_model(self):
        # check vts connection status
        if not self.connected:
            await self.authenticate()

        # check if data has not yet been loaded
        if not self.model_id:
            await self.request_model_data()

        # check if model was updated
        if not await self.validate_model():
            pass # model has been updated, no need to use watcher reload since we need to update model data first
        else:
            type = "ModelLoadRequest"
            dict_msg = self._standard_payload(type)
            dict_msg["data"].update({"modelID": self.model_id })
            msg = json.dumps(dict_msg)
            logging.ws_logger.info("$$ {} request message:\n{}".format(type, msg))
            await self.websocket.send(msg)
            response = await self.websocket.receive()
            logging.ws_logger.info("$$ {} response:\n{}".format(type, response))

            if not response:
                return
            result = json.loads(response)
            if "data" in result:
                data_dict = result["data"]
                if "errorID" in data_dict:
                    logging.ws_logger.error("Error ID: {}, message: {}".format(data_dict["errorID"], data_dict["message"]))
                    if data_dict["errorID"] == 153 and self.reload_model_on_fail:
                        if self.reload_model_attempts >= 4:
                            logging.ws_logger.warning("Maxed out auto reload model attempts. Something went wrong")
                        else:
                            # hit 2 second cooldown, wait buffer time before attempting again.
                            await asyncio.sleep(2.5)
                            self.reload_model_attempts += 1
                            await self.reload_current_model()
                else:
                    self.reload_model_attempts = 0
                    logging.ws_logger.info("reload model success")
    # endregion

    # region Events
    def new_model_event(self):
        if self.new_model_handler:
            self.new_model_handler()
    # endregion