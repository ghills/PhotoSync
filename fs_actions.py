import logging
import os
import shutil

from log_action import echoDecorator

class dryRunDecorator(object):
    def __init__(self, dry_run=False):
        self._dry_run = dry_run

    def __call__(self, fn):
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
        self.remove = log(dryrun(self.remove), name='remove')
        self.move = log(dryrun(self.move), name='remove')
        self.makedirs = log(dryrun(self.makedirs), name='remove')

    def remove(path):
        os.remove(fpath)

    def move(path):
        shutil.move(fpath, outpath)

    def makedirs(path):
        os.makedirs(path)
