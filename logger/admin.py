from django.contrib import admin

from logger.models import EmailSenderLogger


class EmailSenderLoggerAdmin(admin.ModelAdmin):
    readonly_fields = ('datetime_end',)
    list_display = ('datetime_end', 'status',)
    list_filter = ('status',)

admin.site.register(EmailSenderLogger, EmailSenderLoggerAdmin)
