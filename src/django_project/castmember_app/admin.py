from django.contrib import admin

from django_project.castmember_app.models import CastMember as CastMemberModel


class CastMemberAdmin(admin.ModelAdmin): ...


admin.site.register(CastMemberModel, CastMemberAdmin)
