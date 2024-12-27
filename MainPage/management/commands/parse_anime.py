from django.core.management.base import BaseCommand
from MainPage.scripts.parsers import parse_anime_site


class Command(BaseCommand):
    help = "Запуск парсинга аниме из MyAnimeList."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Запуск парсинга..."))

        parse_anime_site()

        self.stdout.write(self.style.SUCCESS("Парсинг успешно завершен!"))