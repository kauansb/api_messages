from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'timestamp')
    search_fields = ('content',)
    list_filter = ('timestamp',)

admin.site.register(Message, MessageAdmin)