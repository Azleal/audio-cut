# -*- coding: utf-8 -*-
# appid 已在配置中移除,请在参数 Bucket 中带上 appid. Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from os import path

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from urllib3.util import parse_url

from common.config import Config as conf
from common.logger import CustomedLogger
from common.qclound_config import QcloudConfig
from common.util import Util

logger = CustomedLogger().get()
qcloud_config = QcloudConfig()


class CosObject(object):
    def __init__(self, bucket, key):
        assert bucket is not None and len(bucket) > 0, "bucket不能为空"
        assert key is not None and len(key) > 0, "key不能为空"
        self.bucket = bucket
        self.key = key


class AudioCos(object):

    def __init__(self):
        self.secret_id = qcloud_config.secret_id
        self.secret_key = qcloud_config.secret_key
        self.region = qcloud_config.region

        token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Token=token,
                                Scheme=scheme)

    def get_client(self):
        # 获取客户端对象
        # 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py
        return CosS3Client(self.config)

    def object_exists(self, cos_object: CosObject):
        return self.get_client().object_exists(cos_object.bucket, cos_object.key)

    def get_object(self, cos_object: CosObject, local_file=''):
        ext = path.splitext(cos_object.key)[1]
        local_file = local_file if len(local_file) > 0 else (
                conf.LOCAL_FILE_TEMP_PATH_PATTERN.format(Util.get_random_str(len=30)) + ext)
        response = self.get_client().get_object(cos_object.bucket, cos_object.key)
        response['Body'].get_stream_to_file(local_file)
        logger.info(
            u"cos saving bucket:{}, key:{}, to local file{}".format(cos_object.bucket, cos_object.key, local_file))
        return local_file

    def put_object(self, cos_object: CosObject, local_file):
        with open(local_file, 'rb') as fp:
            response = self.get_client().put_object(
                Bucket=cos_object.bucket,
                Body=fp,
                Key=cos_object.key
            )
        logger.info("put local file:{}, to cos bucket:{}, with key:{}, got Etag: {}"
                    .format(local_file, cos_object.bucket, cos_object.key, response['ETag']))


    def url_2_cos_info(self, url) -> CosObject:
        parsed_url = parse_url(url)
        bucket = parsed_url.host.split('.')[0]
        key = parsed_url.request_uri
        return CosObject(bucket, self.normalize_key(key))

    def normalize_key(self, key: str):
        if len(key) > 1 and key.startswith('/'):
            return self.normalize_key(key[1:])
        return key


