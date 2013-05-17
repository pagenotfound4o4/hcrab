#coding=utf-8
import os, datetime, time
from dateutil.relativedelta import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'jaylab.settings'
from jaylab.hcrab.models import *
from django.conf import settings

qt = datetime.datetime.now() + relativedelta(hours=-settings.EXPIRE_HOURS)
today = datetime.date.today()
today2 = datetime.datetime(today.year, today.month, today.day, 0 , 0)
fs = VideoFile.objects.filter(latest_ref__lt=qt).filter(latest_ref__gt=today2).all()
print '%i files is about to delete'%len(fs)
for f in fs:
    if not f.is_downloaded():continue
    try:
        os.remove(f.get_file_path())
        print ('%s deleted'%f.title).encode('u8')
        print f.latest_ref
        time.sleep(0.1)
    except OSError:
        pass

