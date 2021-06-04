# -*- coding: utf-8 -*-
import logging  # 引入logging模块
import sys

class CustomedLogger(object):

    def __init__(self, _logging=logging, level=logging.INFO, datefmt="%Y%m%d%H%M", stream=sys.stdout, format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"):
        self._logging = _logging
        self.level = level
        self.datefmt = datefmt
        self.stream = stream
        self.format = format

    def get(self):
        logging.basicConfig(level=self.level, datefmt=self.datefmt,  stream=self.stream, format=self.format)
        return logging.getLogger()
