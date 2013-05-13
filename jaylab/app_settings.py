#coding=utf-8
#global setting for installed app
import os
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

#setting for app hcrab
HOST = 'http://d.jaylab.org'
SERVER_VIDEO_DIR = '/home/jay/websites/d.jaylab.org/yt'
#SERVER_VIDEO_DIR = '/Users/jay/temp/yt'
VIDEO_URL = '/yt'
EXPIRE_TIME = 86400
YOUTUBE_DL_PATH = '/home/jay/Envs/jaylab/bin/youtube-dl'
N_PER_MINUTE = 2 #每分钟处理多少下载记录
MAX_DOWNLOAD_TIMES = 3

#for dropbox
ENABLE_DROPBOX = True
if ENABLE_DROPBOX:
    from dropbox_settings import *
