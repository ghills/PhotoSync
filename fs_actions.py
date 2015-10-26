import logging
import os
import shutil

from functools import wraps
from log_action import echoDecorator

class dryRunDecorator(object):
    def __init__(self, dry_run=False):
        self._dry_run = dry_run

    def __call__(self, fn):
        @wraps(fn)
        def wrapped(*v, **k):
            if not self._dry_run:
                return fn(*v, **k)
            else:
                return None
        return wrapped

class FSActionContext(object):
    def __init__(self, dry_run=False):
        log = echoDecorator(logger=logging.info)
        dryrun = dryRunDecorator(dry_run=dry_run)
        self.remove = log(dryrun(self.remove))
        self.move = log(dryrun(self.move))
        self.makedirs = log(dryrun(self.makedirs))

    def remove(self, path):
        os.remove(path)

    def move(self, fpath, outpath):
        shutil.move(fpath, outpath)

    def makedirs(self, path):
        os.makedirs(path)
