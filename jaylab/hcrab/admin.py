#coding=utf-8
from django.contrib import admin
from models import *


class VideoFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_length_display')


class DownloadRecordAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'vfile', 'status')

admin.site.register(VideoFile, VideoFileAdmin)
admin.site.register(DownloadRecord, DownloadRecordAdmin)