from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import csv

from reviews.models import (Genres, Categories, Titles)

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных из файлов CSV'

    def handle(self, *args, **options):
        with open('static/data/genre.csv', newline='') as csvfile:

            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first = True
            for row in reader:
                if not first:
                    _, created = Genres.objects.get_or_create(
                        name=row[1],
                        slug=row[2],)
                first = False
        with open('static/data/category.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first = True
            for row in reader:
                if not first:
                    _, created = Categories.objects.get_or_create(
                        name=row[1],
                        slug=row[2],)
                first = False
        with open('static/data/titles.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            first = True
            for row in reader:
                if not first:
                    _, created = Titles.objects.get_or_create(
                        name=row[1],
                        year=int(row[2]),
                        category_id=int(row[3]),
                    )
                first = False
        return
        with open('static/data/genre_title.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            first = True
            for row in reader:
                if not first:
                    _, created = GenreTitles.objects.get_or_create(
                        genre_id=int(row[1]),
                        title_id=int(row[2]),
                    )
                first = False

        with open('static/data/users.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first = True
            for row in reader:
                if not first:
                    _, created = User.objects.get_or_create(
                        username=int(row[1]),
                        email=int(row[2]),
                        role=int(row[3]),
                    )
                first = False
