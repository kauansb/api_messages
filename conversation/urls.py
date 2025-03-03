from django.urls import path
from .views import ConversationListView, WebhookView, ConversationDetailView


urlpatterns = [
    path("webhook/", WebhookView.as_view(), name="webhook"),
    path("conversations/<uuid:id>/", ConversationDetailView.as_view(), name="get_conversation"),
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
]
