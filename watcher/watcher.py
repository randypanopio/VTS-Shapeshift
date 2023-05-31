import os, shutil, sys, time, string, threading
from watchdog.observers import Observer
from m_utils import log as logging
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler


class Watcher(threading.Thread):
    """
        create a backup for current session. on new sess, check if backup exists, if not create backup
        if backup folder exists, compare if backup matches latest files, if not matching, create new backup?
    """
    current_backup_dir_name = ".current_watcher_backup"
    previous_session_backup_name = ".previous_watcher_backup"

    def __init__(self, config_data, event_handler = None, trigger_on_delete = True, trigger_on_move = True, trigger_on_create = True):
        super().__init__()
        if config_data["plugin_settings"]["model_directory"]:
            self.dir = os.path.abspath(config_data["plugin_settings"]["model_directory"])
        else:
            self.dir: string = ""
        self.trigger_on_delete = trigger_on_delete
        self.trigger_on_move = trigger_on_move
        self.trigger_on_create = trigger_on_create
        self.event_handler = event_handler
        self.observer = Observer()
        self.enabled = False
        self.initialized = False
        self._stop_event = threading.Event()
        self.observer_thread = None

    def run(self):
        patterns = ["*"]
        event_handler = PatternMatchingEventHandler(patterns, None, False, True)
        event_handler.on_modified = self.trigger_event
        if self.trigger_on_delete:
            event_handler.on_deleted = self.trigger_event
        if self.trigger_on_move:
            event_handler.on_moved = self.trigger_event
        if self.trigger_on_create:
            event_handler.on_created = self.trigger_event
        self.observer.schedule(event_handler, self.dir, recursive=True)

        try:
            while not self._stop_event.is_set():
                time.sleep(1)
        except:
            self.observer.stop()

    def trigger_event(self, event):
        if self.event_handler:
            self.event_handler(event)

    # This gets called by main thread when I want to turn on the watchdog events
    def enable_watcher(self):
        if not self.dir:
            print("Directory has not yet been set up")
            return
        if not self.enabled and self.observer_thread is None:
            self.observer_thread = threading.Thread(target=self.run)
            self.observer_thread.start()
            self.enabled = True
            print("Enabled observer")

    # This gets called by main thread when I want to turn off the watchdog events, i should be able to turn on and off at will
    def disable_watcher(self):
        if self.enabled and self.observer_thread is not None:
            self._stop_event.set()
            self.observer_thread.join()
            self.observer_thread = None
            self.enabled = False
            print("Disabled observer")

    def update_directory(self, directory):
        self.dir = os.path.abspath(directory)
        self.disable_watcher()
        self.enable_watcher()

    def kill_watcher(self):
        self.disable_watcher()
        self._stop_event.set()
        self.observer.stop()
        self.enabled = False
        self.disable_watcher()
        if self.observer_thread is not None:
            self.observer_thread.join()

    def create_backup(self):
        backup_dir = os.path.join(self.dir, self.current_backup_dir_name)

        if not os.path.exists(backup_dir):
            try:
                print("trying to creating backup of directory: " + self.dir)
                shutil.copytree(self.dir, backup_dir)
            except Exception as e:
                print("unable to create a backup of: " + self.dir)
                print(e)
        else:
            # TODO add condition for reverting after session. as well as if we are to update the backup at the end of session
            print("backup exists at: " + backup_dir)
