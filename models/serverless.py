# -*- coding: utf-8 -*-

import json

from common.logger import CustomedLogger

logger = CustomedLogger().get()


class ApiResult(object):

    def __init__(self, body_str, is_base64_encoded=False, status_code=200,
                 headers={"Content-Type": "application/json"}):
        self.body = body_str
        self.is_base64_encoded = is_base64_encoded
        self.status_code = status_code
        self.headers = headers

    def to_dict(self):
        return {
            "isBase64Encoded": self.is_base64_encoded,
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": self.body
        }


class ApiRequest(object):
    '''
    使用api接入时的请求
    '''

    def __init__(self, event, context):
        self.event = event
        self.context = context
        body = event['body']
        self.body = None if body is None else json.loads(body)
        self.query_string = event['queryString']
        logger.info("请求参数信息:{}".format(json.dumps(self.__dict__, ensure_ascii=False)))

    def __str__(self):
        return str(self.__dict__)
