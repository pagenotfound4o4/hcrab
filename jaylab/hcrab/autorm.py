#coding=utf-8
import os, datetime, time
from dateutil.relativedelta import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'jaylab.settings'
from jaylab.hcrab.models import *
from django.settings import EXPIRE_HOURS

qt = datetime.datetime.now() + relativedelta(hours=-EXPIRE_HOURS)
fs = VideoFile.objects.filter(latest_ref__lt=qt).all()
for f in fs:
    try:
        os.remove(f.get_file_path())
        print '%s deleted'%f.md5
        time.sleep(0.1)
    except OSError:
        pass

