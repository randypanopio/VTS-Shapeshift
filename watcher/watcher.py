import os, shutil, sys, time, string, threading, logging
from watchdog.observers import Observer
# from m_utils import log as logging
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler


class Watcher(threading.Thread):
    """
        create a backup for current session. on new sess, check if backup exists, if not create backup
        if backup folder exists, compare if backup matches latest files, if not matching, create new backup?
    """
    current_backup_dir_name = ".current_watcher_backup"
    previous_session_backup_name = ".previous_watcher_backup"

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

        self.is_enabled = False


    def run(self):
        self.is_enabled = True
        self.observer.start()
        try:
            while self.is_enabled:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.is_enabled = False
        self.observer.stop()
        self.observer.join()

    def enable_watcher(self):
        if not self.is_enabled:
            self.start()
            print("Enabled observer")

    def disable_watcher(self):
        if self.is_enabled:
            self.stop()
            print("Disabled observer")

    def update_directory(self, directory):
        self.dir = os.path.abspath(directory)
        self.observer.unschedule_all()
        self.observer.schedule(self.event_handler, self.dir, recursive=True)
        print("Directory updated to:", self.dir)

    def kill_thread(self):
        self.disable_watcher()
        self.join()

    def trigger_event(self, event):
        self.event_handler(event)

    # TODO move backup logic to a new class
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
