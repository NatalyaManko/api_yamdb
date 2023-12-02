from django.core.management.base import BaseCommand
from django.conf import settings as conf_settings
import csv

from reviews.models import (Genres, Categories,
                            GenreTitles, Titles)


class Command(BaseCommand):
    help = 'Заполняет базу данных из файлов CSV'

    def handle(self, *args, **options):
        with open('static/data/genre.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                _, created = Genres.objects.get_or_create(
                    name=row[1],
                    slug=row[2],)
        with open('static/data/category.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                _, created = Categories.objects.get_or_create(
                    name=row[1],
                    slug=row[2],)
                return
        with open('static/data/titles.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                _, created = Titles.objects.get_or_create(
                    name=row[1],
                    year=int(row[2]),
                    category_id=int(row[3]),
                )

        with open('static/data/genre_title.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                _, created = GenreTitles.objects.get_or_create(
                    genre_id=int(row[1]),
                    tytle_id=int(row[2]),
                )
