import os

FN_LIMIT = 38
FN_LIMIT_HALVED = int(FN_LIMIT / 2)
SUPPORTED_FORMATS = ['mp3', 'wav', 'ogg']
TABLEFMT = 'plain'
FFMPEG_PATH = 'ffmpeg'

os.environ['PATH'] += f';{os.getcwd()}\\{FFMPEG_PATH}'
