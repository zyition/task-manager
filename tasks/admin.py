from django.contrib import admin

from .models import Member, Iteration


class MemberAdmin(admin.ModelAdmin):
    pass


class IterationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Member, MemberAdmin)
admin.site.register(Iteration, IterationAdmin)
