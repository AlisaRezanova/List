from django.core.management.base import BaseCommand
from MainPage.scripts.parsers import parse_book


class Command(BaseCommand):
    help = "Запуск парсинга книг."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Запуск парсинга..."))

        parse_book()

        self.stdout.write(self.style.SUCCESS("Парсинг успешно завершен!"))