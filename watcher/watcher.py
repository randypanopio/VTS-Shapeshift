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
        self.observer.schedule(self.scheduler_event_handler, self.dir, recursive=True)
        self.observer.name = "Watchdog_Thread"

        self.is_enabled = False
        self.thread = threading.Thread(target=self.run)
        self.thread.name = "Watcher_Thread"
        self.should_stop = threading.Event()
        self.thread.start()

    def run(self):
        self.observer.start()
        try:
            while self.should_stop.is_set():
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()

    def enable_watcher(self):
        if not self.is_enabled:
            self.is_enabled = True
            print("Enabled observer")

    def disable_watcher(self):
        if self.is_enabled:
            self.is_enabled = False
            print("Disabled observer")

    def update_directory(self, directory):
        if not self.is_enabled:
            self.dir = os.path.abspath(directory)
            print("Directory updated to:", self.dir)

    def kill_thread(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            print("killed watchdog")
        self.should_stop.set()
        print("killed watcher thread")

    def trigger_event(self, event):
        if self.is_enabled:
            self.event_handler(event)
