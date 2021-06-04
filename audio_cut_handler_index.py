# -*- coding: utf-8 -*-

import json
import multiprocessing
from os import path

from common.config import Config as conf
from common.cos import AudioCos, CosObject
from common.exception import AudioCutException
from common.ffmpeg_client import Ffmpeg
from common.logger import CustomedLogger
from common.util import Util
from models.audio_cut_param import AudioCutParam
from models.serverless import ApiResult, ApiRequest

logger = CustomedLogger().get()
audio_cos = AudioCos()
ffmpeg = Ffmpeg()
SUCCESS = "success"

"""
音频裁切接口. 响应两种动作:
1. 裁切(cut). 指定bucket, key, start, duration, 进行音频裁切. 裁剪好的音频放置到指定bucket下
2. 查询(query). 指定bucket, key, 查询文件是否存在
"""


def main_handler(event, context):
    result = get_result(None, None, SUCCESS)
    try:
        api_request = ApiRequest(event, context)
        param = AudioCutParam.from_api_request(api_request)

        if param.action == param.CUT_ACTION:
            result = cut_action_handler(param)
        else:
            result = query_action_handler(param)
    except AudioCutException as e:
        result["message"] = e.message
    except AssertionError as ae:
        result["message"] = str(ae)

    return ApiResult(json.dumps(result)).to_dict()


def cut_action_handler(cut_param: AudioCutParam):
    '''
    音频裁剪handler
    :param cut_param: bucket, key, start, duration
    :return: bucket, key, status
    '''
    original_cos_object = cut_param.cos_object
    if not audio_cos.object_exists(original_cos_object):
        raise AudioCutException("文件[bucket={}, key={}]不存在".format(original_cos_object.bucket, original_cos_object.key))
    ext = path.splitext(original_cos_object.key)[1]
    # 原始(待裁切)文件的本地保存位置
    original_local_path = conf.LOCAL_FILE_TEMP_PATH_PATTERN.format(Util.get_random_str(len=30)) + ext

    # 提前生成待上传的文件key
    random_key = Util.get_random_str(30) + "." + conf.DEFAULT_AUDIO_FORMAT
    while audio_cos.object_exists(CosObject(original_cos_object.bucket, random_key)):
        random_key = Util.get_random_str(30) + "." + conf.DEFAULT_AUDIO_FORMAT
    to_upload_cos_object = CosObject(original_cos_object.bucket, random_key)

    # 提前生成待上传的本地文件地址
    trimmed_mp3_file_path = path.join(path.dirname(original_local_path), random_key)

    p = multiprocessing.Process(target=async_cut_audio,
                                args=(original_cos_object, cut_param.start, cut_param.duration,
                                      original_local_path, to_upload_cos_object, trimmed_mp3_file_path))
    p.start()
    return get_result(to_upload_cos_object.bucket, to_upload_cos_object.key, SUCCESS)


def query_action_handler(query_param: AudioCutParam):
    if audio_cos.object_exists(query_param.cos_object):
        return get_result(query_param.cos_object.bucket, query_param.cos_object.key, SUCCESS)
    return get_result(None, None, "fail")

def async_cut_audio(original_cos_object: CosObject, start, duration, original_local_path, trimmed_cos_object: CosObject,
                    trimmed_local_path):
    local_file = audio_cos.get_object(original_cos_object, local_file=original_local_path)
    trimmed_key, local_trimmed_file = ffmpeg.cut_audio(local_file, start, duration, trimmed_key=trimmed_cos_object.key,
                                                       trimmed_local_path=trimmed_local_path)
    audio_cos.put_object(trimmed_cos_object, local_trimmed_file)
    return trimmed_cos_object

def get_result(bucket, key, msg):
    return {"bucket": bucket, "key": key, "message": msg}
