""" logger sets formatter and handlers settings to logger"""
import os

import logging
import config as c

__author__ = 'Danila Lapko'

formatter = logging.Formatter(u'[%(filename)-12s%(lineno)4d%(funcName)30s()]# %(levelname)-8s   %(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)

file_path = os.path.join(c.log_path, 'log.txt')
if os.path.exists(file_path):
    file_mode = 'a'  # append if already exists
else:
    file_mode = 'w'  # make a new file if not

fileHandler = logging.FileHandler(file_path, file_mode)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(streamHandler)
log.addHandler(fileHandler)
log.setLevel(logging.DEBUG)
