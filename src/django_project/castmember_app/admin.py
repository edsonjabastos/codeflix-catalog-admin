from django.contrib import admin

from django_project.castmember_app.models import CastMember as CastMemberORM


class CastMemberAdmin(admin.ModelAdmin): ...


admin.site.register(CastMemberORM, CastMemberAdmin)
