# -*- coding: utf-8 -*-

import os
import subprocess
from os import path

import ffmpeg

from common.exception import AudioCutException
from common.logger import CustomedLogger
from common.util import Util
from common.config import Config as confs

# 最终存在的位置,这里才是可执行的
FFMPEG_PATH = confs.FFMPEG_PATH

# 通过层管理的ffmpeg可执行文件在/opt/usr/bin/ffmpeg
# 原始文件下载地址 https://raw.githubusercontent.com/tencentyun/serverless-demo/master/Python3.6-VideoToRTMP/src/ffmpeg
# 该文件必须存在
LOCAL_FFMPEG_PATHS = confs.LOCAL_FFMPEG_PATHS

logger = CustomedLogger().get()


class Ffmpeg(object):

    def __init__(self):
        self.__prepare_ffmpeg_env()

    def __prepare_ffmpeg_env(self):
        if path.exists(FFMPEG_PATH) and os.access(FFMPEG_PATH, os.X_OK):
            # 当前的FFMPEG_PATH 可以访问,且有执行权限, 则什么都不做
            return
        for executable in LOCAL_FFMPEG_PATHS:
            if path.exists(executable):
                subprocess.run('cp {} {} && chmod 755 {}'.format(executable, FFMPEG_PATH, FFMPEG_PATH), shell=True)
                return

        raise AudioCutException("ffmpeg doesn't exist")

    def __check_ffmpeg_env(self):
        logger.info("ffmpeg path:{}".format(path.exists(FFMPEG_PATH)))

    '''
        裁切音频, 本地地址, 起始时间 时长
    '''

    def cut_audio(self, input_file_path, start, duration, trimmed_key='', trimmed_local_path=''):
        audio_random_name = trimmed_key if len(trimmed_key) > 0 else Util.get_random_str(
            30) + "." + confs.DEFAULT_AUDIO_FORMAT
        trimmed_mp3_file_path = trimmed_local_path if len(trimmed_local_path) > 0 else path.join(
            path.dirname(input_file_path), audio_random_name)
        ffmpeg_cmd = (
            ffmpeg
                .input(input_file_path, ss=start, t=duration)
                .output(trimmed_mp3_file_path, acodec='copy')
                .overwrite_output()
        )
        logger.info(ffmpeg_cmd.compile(cmd=FFMPEG_PATH))
        ffmpeg_cmd.run(cmd=FFMPEG_PATH)
        return audio_random_name, trimmed_mp3_file_path
