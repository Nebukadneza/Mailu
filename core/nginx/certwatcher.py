#!/usr/bin/python3

import sys
import logging
from os.path import exists, split as path_split
from os import system
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileDeletedEvent, FileCreatedEvent, FileModifiedEvent, FileMovedEvent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('certwatcher')

class ChangeHandler(FileSystemEventHandler):
    @staticmethod
    def reload_nginx():
        if exists("/var/run/nginx.pid"):
            logger.warning("Reloading nginx...")
            system("nginx -s reload")

    def on_any_event(self, event):
        filename = path_split(event.src_path)[-1]
        if isinstance(event, FileMovedEvent):
            filename = path_split(event.dest_path)[-1]

        if filename in ['cert.pem', 'key.pem'] and not event.is_directory:
            if isinstance(event, FileCreatedEvent):
                logger.info("Found that file %s has been created!", filename)
                ChangeHandler.reload_nginx()
            elif isinstance(event, FileModifiedEvent):
                logger.info("Found that file %s has been modified!", filename)
                ChangeHandler.reload_nginx()
            elif isinstance(event, FileMovedEvent):
                logger.info("Found that file %s has been moved to %s!", event.src_path, filename)
                ChangeHandler.reload_nginx()
            else:
                logger.warning("Unhandled event %s", event)
        else:
            logger.debug("Uninteresting event %s", event)

if __name__ == '__main__':
    observer = Observer()
    handler = ChangeHandler()
    observer.schedule(handler, "/certs", recursive=False)
    observer.start()
    while True:
        time.sleep(1)
