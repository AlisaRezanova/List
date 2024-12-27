from django.core.management.base import BaseCommand
from MainPage.scripts.parsers import parse_lord_film


class Command(BaseCommand):
    help = "Запуск парсинга аниме из Кинопоиск."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Запуск парсинга..."))

        parse_lord_film()

        self.stdout.write(self.style.SUCCESS("Парсинг успешно завершен!"))