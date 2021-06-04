# -*- coding: utf-8 -*-

from os import path

class Config(object):

    # 本地临时文件文件夹
    LOCAL_FILE_TEMP_BASE_DIR = "/tmp/"

    # 本地临时文件保存地址pattern
    LOCAL_FILE_TEMP_PATH_PATTERN = path.join(LOCAL_FILE_TEMP_BASE_DIR, "{}")

    # 默认的音频格式
    DEFAULT_AUDIO_FORMAT = "mp3"

    # 最终存在的位置,这里才是可执行的
    FFMPEG_PATH = "/tmp/ffmpeg"

    # 通过层管理的ffmpeg可执行文件在/opt/usr/bin/ffmpeg
    # 原始文件下载地址 https://raw.githubusercontent.com/tencentyun/serverless-demo/master/Python3.6-VideoToRTMP/src/ffmpeg
    # 该文件必须存在
    LOCAL_FFMPEG_PATHS = ["/opt/usr/bin/ffmpeg", '/usr/local/bin/ffmpeg']
