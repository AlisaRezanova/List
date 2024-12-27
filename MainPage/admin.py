from django.contrib import admin
from .models import List, Anime, Movie, Manga, Book


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_title', 'user')
    list_per_page = 10

    def get_title(self, obj):
        return obj.content_object.title
    get_title.short_description = 'Title'


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'season', 'url')
    list_per_page = 500


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating')
    list_per_page = 500


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating')
    list_per_page = 500


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating')
    list_per_page = 500