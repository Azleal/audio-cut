# -*- coding: utf-8 -*-
from common.cos import CosObject
from models.serverless import ApiRequest
from common.exception import AudioCutException


class AudioCutParam(object):
    CUT_ACTION = 'cut'
    QUERY_ACTION = 'query'
    allowed_actions = [CUT_ACTION, QUERY_ACTION]

    def __init__(self, action, bucket, key, start, duration):
        self.action = action
        if self.action not in AudioCutParam.allowed_actions:
            raise AudioCutException("action=[{}] now allowed".format(self.action))

        self.cos_object = CosObject(bucket, key)
        self.start = start
        self.duration = duration

        assert self.cos_object is not None, "文件信息[bucket, key]必须存在"
        if self.action == AudioCutParam.CUT_ACTION:
            assert self.start is not None, "截取起始时间[start]必须存在"
            assert self.start >= 0, "截取起始时间[start]必须大于等于0"
            assert self.duration is not None, "截取持续时间[duration]必须存在"
            assert self.duration > 0, "截取持续时间[duration]必须大于0"

    @classmethod
    def from_api_request(cls, api_request: ApiRequest):
        action, bucket, key, start, duration = None, None, None, None, None
        try:
            action = api_request.query_string['action']
            bucket = api_request.body['bucket']
            key = api_request.body['key']
            start = api_request.body['start']
            duration = api_request.body['duration']
        except Exception as e:
            pass
        return AudioCutParam(action, bucket, key, start, duration)
