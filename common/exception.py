# -*- coding: utf-8 -*-
class AudioCutException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)