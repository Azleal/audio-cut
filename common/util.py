# -*- coding: utf-8 -*-

import random
from datetime import time


class Util(object):

    @classmethod
    def ms_to_time(cls, time_in_ms):
        ms = (time_in_ms % 1000) * 1000
        second = (time_in_ms // 1000) % 60
        minute = (time_in_ms // (1000 * 60)) % 60
        hour = (time_in_ms // (1000 * 60 * 60)) % 60
        return time(hour, minute, second, ms)

    @classmethod
    def ms_to_srt_time_str(cls, time_in_ms):
        return cls.ms_to_time(time_in_ms).isoformat(timespec='microseconds')[:-3]

    @classmethod
    def get_random_str(cls, len=12):
        alphabet = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        sa = []
        for i in range(len):
            sa.append(random.choice(alphabet))
        return ''.join(sa)
