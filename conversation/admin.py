from django.contrib import admin
from .models import Conversation


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status')
    search_fields = ('status',)
    list_filter = ('created_at',)

admin.site.register(Conversation, ConversationAdmin)