# -*- coding:utf-8 -*-
import sys
import time
import datetime
import hashlib
import random
import requests
import re
import functools
import datetime
import collections

from ExceptionBox import *

reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(1000000)

#def output()

def methodName(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print '[%s] call=>>  %s()' % (nowtime, func.__name__)
        return func(*args, **kw)

    return wrapper