#coding=utf-8
import os, datetime
from dateutil.relativedelta import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'jaylab.settings'
from jaylab.hcrab.models import *

qt = datetime.datetime.today() + relativedelta(days=-2)
fs = VideoFile.objects.filter(latest_ref__lt=qt).all()
for f in fs:
    try:
        os.remove(f.get_file_path())
    except OSError:
        pass
