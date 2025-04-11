from django.contrib import admin

from django_project.video_app.models import Video, AudioVideoMedia, ImageMedia


class VideoAdmin(admin.ModelAdmin): ...


class AudioVideoMediaAdmin(admin.ModelAdmin): ...


class ImageMediaAdmin(admin.ModelAdmin): ...


admin.site.register(Video, VideoAdmin)

admin.site.register(AudioVideoMedia, AudioVideoMediaAdmin)

admin.site.register(ImageMedia, ImageMediaAdmin)
