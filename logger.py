""" logger sets formatter and handlers settings to logger"""
import os

import logging
import config as c


__author__ = 'Danila Lapko'

formatter = logging.Formatter(u'[%(filename)-12s%(lineno)4d%(funcName)30s()]# %(levelname)-8s   %(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
fileHandler = logging.FileHandler(os.path.join(c.log_path, 'log.txt'))
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(streamHandler)
log.addHandler(fileHandler)
log.setLevel(logging.DEBUG)