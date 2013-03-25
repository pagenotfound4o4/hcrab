#coding=utf-8
import os, time, subprocess, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'jaylab.settings'
from django.conf import settings
from jaylab.hcrab.models import *

command = '%s -i -c -R 3 --write-info-json --write-srt -o %s -f 18 %s'

to_download = DownloadRecord.objects.filter(status='queue').\
                  order_by('created_at')[:settings.N_PER_MINUTE]

print len(to_download)
for r in to_download:
    print 'process download record: %i .' % r.id
    vfile = r.vfile
    if not vfile.is_downloaded():
        vfile.status = 'downloading'
        vfile.save()
        print 'has not download. start to download.'
        cmd = command % (settings.YOUTUBE_DL_PATH, vfile.get_file_path(), vfile.watch_url)
        subprocess.call(cmd, shell=True)
        if not vfile.is_downloaded():
            vfile.status = 'download_failed'
            vfile.save()
            print 'downloaded failed.'
            continue
        print 'downloaded.'
        vfile.has_subtitle = os.path.exists(vfile.get_srt_file_path())
        json_file_path = os.path.join(settings.SERVER_VIDEO_DIR,
                                      '%s.info.json' % vfile.get_filename())
        info = json.load(open(json_file_path))
        vfile.title = info.get('title')
        vfile.desp = info.get('description')
        vfile.download_url = info.get('url')
        duration = info.get('duration')
        if duration:
            vfile.duration = int(duration)
        vfile.length = os.path.getsize(vfile.get_file_path())
        vfile.save()
    else:
        print 'downloaded before.'
    dropbox_user = r.dropbox_user
    if dropbox_user:
        print 'pushing dropbox.'
        r.status = 'dropbox_pushing'
        r.save()
        c = dropbox_user.get_client()
        title = vfile.title
        #https://www.dropbox.com/help/145/en
        incompatible_characters = ['/', '\\', '<', '>', ':', '"', '|', '?', '*']
        for char in incompatible_characters:
            title = title.replace(char, '')
        #print title
        resp = c.put_file('/%s.%s' % (title, vfile.ext), open(vfile.get_file_path()))
        #需要错误处理
        #...
    print 'finished'
    r.status = 'finished'
    r.save()

    time.sleep(0.1)
