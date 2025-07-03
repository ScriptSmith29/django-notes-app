from django.shortcuts import HttpResponseRedirect
from django.contrib import admin
from .models import Note, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect("/admin/home/tag/")

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_important', 'created', 'updated')
    list_filter = ('is_important', 'created')
    search_fields = ('title', 'content')
