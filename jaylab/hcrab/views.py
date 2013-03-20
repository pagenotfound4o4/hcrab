#coding=utf-8
import re, uuid
from hashlib import md5
from django.conf import settings
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from models import *

youtube_pattern = r'youtube\.com/watch\?v=[0-9, a-z, A-Z, \-, _]+'


def file2md5(url, quality):
    m = md5()
    m.update(url + quality)
    return m.hexdigest()


def index(request):
    sid = request.session.get('session_id', '')

    records = None
    if sid:
        records = DownloadRecord.objects.filter(session_id=sid).order_by('-created_at')
        for r in records:
            if r.status != 'finished':
                r.title = '-'
                r.durl = r.vfile.get_status_display()
            else:
                r.title = ' '.join( r.vfile.title.split()[:6]) + '...'
                r.durl = r.get_download_url()
    else:
        sid = uuid.uuid1().hex
        request.session['session_id'] = sid
        request.session.set_expiry(settings.EXPIRE_TIME)

    params = {}
    params.update(csrf(request))
    params['records'] = records

    return render_to_response('hcrab/index.html', params)


def add(request):
    back_url = reverse(index)

    sid = request.session.get('session_id', '')
    if not sid:
        info = u'请打开浏览器cookie支持。'
        return render_to_response('hcrab/info.html',
                                  {'info': info,
                                   'interval': 3,
                                   'back_url': back_url})

    url = request.POST.get('url', '')
    if not url:
        info = u'请填写视频链接。'
        return render_to_response('hcrab/info.html',
                                  {'info': info,
                                   'interval': 3,
                                   'back_url': back_url})

    r = re.search(youtube_pattern, url)
    if r:
        url = r.group()
    else:
        info ='视频地址不正确.'
        return render_to_response('info.html',
                                  { 'infomation': info,
                                    'interval': 3,
                                    'back_url':back_url,
                                    })

    quality = 'm'

    m5 = file2md5(url, quality)
    y, is_created = VideoFile.objects.get_or_create(md5=m5, watch_url=url, quality=quality)
    DownloadRecord.objects.get_or_create(session_id=sid, vfile=y)
    return redirect(back_url)


