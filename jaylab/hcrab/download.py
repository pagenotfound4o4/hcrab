#coding=utf-8
import os,sys,datetime,time,subprocess,json
os.environ['DJANGO_SETTINGS_MODULE'] = 'jaylab.settings'
from django.conf import settings
from jaylab.hcrab.models import *

command = '%s -i -c -R 3 --write-info-json --write-srt -o %s -f 18 %s'
vfiles = VideoFile.objects.filter(status='queue').order_by('created_at')[:2]
for f in vfiles:
    f.status = 'downloading'
    f.save()

for f in vfiles:
    fn = f.get_filename()
    vfile_path = os.path.join(settings.SERVER_VIDEO_DIR, fn)
    cmd = command%(settings.YOUTUBE_DL_PATH, vfile_path, f.watch_url)
    r = subprocess.call(cmd, shell=True)
    
    if not os.path.exists(vfile_path):
        f.status = 'failed'
        f.save()
        continue

    srt_file_path = os.path.join(settings.SERVER_VIDEO_DIR, '%s.srt'%f.md5)
    f.has_subtitle = os.path.exists(srt_file_path)
    
    json_file_path = os.path.join(settings.SERVER_VIDEO_DIR, '%s.info.json'%fn)
    info = json.load(open(json_file_path))
    f.title = info.get('title')
    f.desp = info.get('description')
    f.download_url = info.get('url')
    f.duration = int( info.get('duration') )
    f.length = os.path.getsize(vfile_path)
    f.status = 'finished'

    f.save()
    time.sleep(2)
