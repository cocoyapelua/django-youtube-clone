from django.contrib import admin
from .models import Video, Comment, Interaction, History


# Register your models here.


class LikeInline(admin.TabularInline):
    model = Interaction
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class VideoAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
        LikeInline,
    ]
    list_display = ('title', 'user', 'date')


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'date')


admin.site.register(Video, VideoAdmin)
admin.site.register(Comment)
admin.site.register(History, HistoryAdmin)
