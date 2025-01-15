from django.contrib import admin

from django_project.genre_app.models import Genre as GenreORM


class GenreAdmin(admin.ModelAdmin): ...


admin.site.register(GenreORM, GenreAdmin)
