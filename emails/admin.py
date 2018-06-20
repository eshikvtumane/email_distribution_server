from django.contrib import admin

from emails.submodels.email import Email
from emails.submodels.group_email import GroupEmail


class GroupEmailAdmin(admin.ModelAdmin):
    pass


class EmailAdmin(admin.ModelAdmin):
    pass


admin.site.register(GroupEmail, GroupEmailAdmin)
admin.site.register(Email, EmailAdmin)
