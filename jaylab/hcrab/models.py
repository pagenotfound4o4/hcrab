#coding=utf-8
from django.conf import settings
from django.db import models

status_choices = (
    ('queue', u'排队中'),
    ('downloading', u'下载中'),
    ('finished', u'完成'),
    ('failed', u'下载失败'),
)
quality_choices = (
    ('l', u'低'),
    ('m', u'中'),
    ('h', u'高'),
)


class DropboxUser(models.Model):
    class Meta:
        verbose_name = u'Dropbox用户'
        verbose_name_plural = verbose_name

    uid = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=400, blank=True, default='')
    country = models.CharField(max_length=50, blank=True, default='')
    name = models.CharField(max_length=400, blank=True, default='')
    quota_info = models.CharField(max_length=400, blank=True, default='')
    referral_link = models.CharField(max_length=400, blank=True, default='')

    access_key = models.CharField(max_length=50, blank=True, default='')
    access_secret = models.CharField(max_length=50, blank=True, default='')

    is_valid = models.BooleanField(default='True')

    def __unicode__(self):
        return self.name


class VideoFile(models.Model):
    class Meta:
        verbose_name = u'视频文件'
        verbose_name_plural = verbose_name

    title = models.CharField(max_length=400, blank=True, default='')

    watch_url = models.CharField(max_length=500)
    md5 = models.CharField(max_length=50, unique=True)
    download_url = models.CharField(max_length=500, blank=True, default='')
    duration = models.IntegerField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True, verbose_name=u'文件大小(byte)')
    desp = models.TextField(blank=True, default='')
    ext = models.CharField(max_length=50, default='mp4')
    quality = models.CharField(max_length=20, default=u'm', choices=quality_choices)
    has_subtitle = models.BooleanField(default=False)
    website = models.CharField(max_length=20, default=u'youtube')

    status = models.CharField(max_length=50, choices=status_choices, default='queue')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_filename(self):
        return self.md5 + '.' + self.ext

    def get_srt_filename(self):
        '''字幕文件的名字'''
        return self.md5 + '.srt'

    def get_length_display(self):
        if self.length:
            return '%i MB' % (self.length/1024.0/1024.0)
        return ''


class DownloadRecord(models.Model):
    class Meta:
        verbose_name = u'下载记录'
        verbose_name_plural = verbose_name

    session_id = models.CharField(max_length=50, blank=True, default='')
    dropbox_user = models.ForeignKey(DropboxUser, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    vfile = models.ForeignKey(VideoFile)

    def get_download_url(self):
        if self.vfile.status != 'finished':
            return ''
        return settings.HOST + settings.VIDEO_URL + '/' + self.vfile.get_filename()

    def get_srt_url(self):
        if self.vfile.has_subtitle:
            return settings.HOST + settings.VIDEO_URL + '/' + self.vfile.get_srt_filename()
        return ''

    def get_status(self):
        return self.vfile.status
    status = property(fget=get_status)

    def __unicode__(self):
        return 'Download_record_%i' % self.id


