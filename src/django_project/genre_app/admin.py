from django.contrib import admin

from django_project.genre_app.models import Genre as GenreModel


class GenreAdmin(admin.ModelAdmin): ...


admin.site.register(GenreModel, GenreAdmin)
