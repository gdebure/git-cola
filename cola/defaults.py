#!/usr/bin/env python

import os
from PyQt4.QtCore import QEvent
from cola import version
VERSION = version.VERSION
DIRECTORY = os.getcwd()

WIDTH = 780
HEIGHT = 600

X = 262
Y = 254

INOTIFY_EVENT = QEvent.User + 0