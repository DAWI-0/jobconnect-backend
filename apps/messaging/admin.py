from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("created_at",)
    autocomplete_fields = ("sender",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "recruiter", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("candidate__user__email", "recruiter__user__email")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("candidate", "recruiter")
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "sender", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("sender__email", "content")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("conversation", "sender")