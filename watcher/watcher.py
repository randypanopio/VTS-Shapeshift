import os, time, string, threading
from watchdog.observers import Observer
from m_utils import log as logging
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler

"""
NOTE I dunno how to properly handle the observer thread.
I could go the nasty route and just have a permanent watcher subprocess in the background
And instead of disabling the thread, just ignore trigger callbacks
- not very performant :( - maybe a TODO revisit later way down the road
"""
class Watcher(threading.Thread):
    def __init__(
            self, config_data,
            event_handler,
            trigger_on_delete = True,
            trigger_on_move = True,
            trigger_on_create = True
            ):
        super().__init__()
        if config_data["plugin_settings"]["model_directory"]:
            self.dir = os.path.abspath(config_data["plugin_settings"]["model_directory"])
        else:
            self.dir: string = ""

        self.observer = Observer()
        patterns = ["*"]
        self.event_handler = event_handler
        self.scheduler_event_handler = PatternMatchingEventHandler(patterns, None, False, True)
        self.scheduler_event_handler.on_modified = self.trigger_event
        if trigger_on_delete: self.scheduler_event_handler.on_deleted = self.trigger_event
        if trigger_on_move: self.scheduler_event_handler.on_moved = self.trigger_event
        if trigger_on_create: self.scheduler_event_handler.on_created = self.trigger_event
        self.observer.name = self.observer.name + " - Watchdog_Thread"

        self.is_enabled = False
        self.has_started = False

        self.thread = threading.Thread(target=self.run)
        self.thread.name = self.thread.name + " - Watcher_Thread"
        self.allow_event_trigger = True
        self.should_stop = threading.Event()

        # this buffer is how often events can get trigd. its to allow some file/io buffer time between completion of complete filestreming in that directory to roughly time files are ready to be reloaded in VTS.
        self.event_cooldown = 2

    def start_watcher(self):
        if not self.has_started:
            self.observer.schedule(self.scheduler_event_handler, self.dir, recursive=True)
            self.observer.start()
            logging.ws_logger.info("enabled {} thread".format(self.observer.name))
            if not self.thread.is_alive():
                self.thread.start()
                logging.ws_logger.info("enabled {} thread".format(self.thread.name))
            self.has_started = True

    def run(self):
        try:
            while self.should_stop.is_set():
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()

    def enable_watcher(self):
        if not self.dir:
            return
        if not self.is_enabled:
            self.is_enabled = True
            logging.ws_logger.info("Enabled observer, watching: " + self.dir)
        if not self.has_started:
            self.start_watcher()

    def disable_watcher(self):
        if self.is_enabled:
            self.is_enabled = False
            logging.ws_logger.info("Disabled observer")

    def update_directory(self, directory):
        if not self.is_enabled:
            self.dir =  os.path.abspath(directory)
            self.observer.unschedule_all()
            self.observer.schedule(self.scheduler_event_handler, self.dir, recursive=True)
            logging.ws_logger.info("Directory updated to:", self.dir)

    def kill_thread(self):
        if self.observer is not None and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            logging.ws_logger.info("killed watchdog")
        self.should_stop.set()
        if self.thread.is_alive(): self.thread.join()
        logging.ws_logger.info("killed watcher thread")

    def trigger_event(self, event):
        if self.is_enabled:
            if self.allow_event_trigger:
                logging.ws_logger.info("correct event")
                self.event_handler(event)
                self.allow_event_trigger = False
                self.start_cooldown()
            else:
                logging.ws_logger.info("rejected event")

    def start_cooldown(self):
        # technically all the events' thread are cleaned up by the interpreter.
        # But could also create a new single thread and handle itself or smn
        threading.Thread(target=self.reset_event).start()

    def reset_event(self):
        time.sleep(self.event_cooldown)
        self.allow_event_trigger = True
