import sys

from functools import wraps
from itertools import chain

class echoDecorator(object):
    def __init__(self, logger=sys.stdout.write):
        self._logger = logger

    def __call__(self, fn):
        @wraps(fn)
        def wrapped(*v, **k):
            pos_vars = map(repr, v)
            kw_vars = ( '{}={}'.format(k, repr(v)) for k, v in k.items() )
            args = ", ".join(chain(pos_vars, kw_vars))
            self._logger('{}({})'.format(fn.__name__, args))
            return fn(*v, **k)
        return wrapped
