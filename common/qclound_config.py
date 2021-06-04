# -*- coding: utf-8 -*-
import os


class QcloudConfig(object):
    cos_appid = os.getenv('COS_APPID')
    secret_id = os.getenv('COS_SECRETID')
    secret_key = os.getenv('COS_SECRETKEY')
    region = os.getenv('COS_REGION')  # cos Region