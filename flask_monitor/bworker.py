#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import logging.handlers
from bworker_app import app


###################### Run Flask server ######################
if len(sys.argv) < 2:
    port = 25139  # BEAt WorkeR (25139)
else:
    port = sys.argv[1]
if len(sys.argv) < 3:
    log_path = None
else:
    log_path = sys.argv[2]

###################### Configure log ######################
# configure log
log_path = log_path if log_path else os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
log_file = os.path.join(log_path, 'bworker.log')
if not os.path.exists(log_path):
    os.makedirs(log_path)

# add file handler (if not added)
app.logger.setLevel(logging.DEBUG)
if len([handler for handler in app.logger.handlers if (type(handler) == logging.handlers.RotatingFileHandler)]) == 0:
    rot_handler = logging.handlers.RotatingFileHandler(log_file, mode='a', maxBytes=10*1024*1024, backupCount=5)
    rot_handler.setLevel(logging.DEBUG)
    rot_handler.setFormatter(logging.Formatter('%(asctime)15s: <%(filename)s, %(lineno)s> %(message)s', '%Y-%m-%d %H:%M:%S'))
    app.logger.addHandler(rot_handler)

# stdout log
if len([handler for handler in app.logger.handlers if (type(handler) == logging.StreamHandler)]) == 0:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter('%(asctime)15s: %(message)s', '%Y-%m-%d %H:%M:%S'))
    app.logger.addHandler(stream_handler)

app.run(debug=False, host='0.0.0.0', port=port)
