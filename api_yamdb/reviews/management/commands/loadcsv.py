from datetime import datetime
import sqlite3
import csv

from django.core.management.base import BaseCommand

from reviews.models import (Genre, Category,
                            Title, Comment,
                            Review,)
from users.models import User


class Command(BaseCommand):
    help = 'Заполняет базу данных из файлов CSV'

    def handle(self, *args, **options):
        with open('static/data/genre.csv', newline='') as csvfile:

            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first = True
            for row in reader:
                if not first:
                    _, created = Genre.objects.get_or_create(
                        id=int(row[0]),
                        name=row[1],
                        slug=row[2],)
                first = False
        with open('static/data/category.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first = True
            for row in reader:
                if not first:
                    _, created = Category.objects.get_or_create(
                        id=int(row[0]),
                        name=row[1],
                        slug=row[2],)
                first = False

        with open('static/data/titles.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            first = True
            for row in reader:
                if not first:
                    _, created = Title.objects.get_or_create(
                        id=int(row[0]),
                        name=row[1],
                        year=int(row[2]),
                        category_id=int(row[3]),
                    )
                first = False

        with open('static/data/users.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first = True
            for row in reader:
                if not first:
                    _, created = User.objects.get_or_create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                    )
                first = False

        with open('static/data/review.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            first = True
            for row in reader:
                if not first:
                    _, created = Review.objects.get_or_create(
                        id=int(row[0]),
                        title_id=int(row[1]),
                        text=row[2],
                        author_id=int(row[3]),
                        score=int(row[4]),
                        pub_date=datetime.strptime(row[5], '%Y-%m-%dT%H:%M:%S.%fZ')
                    )
                first = False

        with open('static/data/comments.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            first = True
            for row in reader:
                if not first:
                    _, created = Comment.objects.get_or_create(
                        id=int(row[0]),
                        review_id=int(row[1]),
                        text=row[2],
                        author_id=int(row[3]),
                        pub_date=datetime.strptime(row[4], '%Y-%m-%dT%H:%M:%S.%fZ')
                    )
                first = False

        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        reviews_genres = []
        with open('static/data/genre_title.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            first = True
            for row in reader:
                if not first:
                    reviews_genres.append((int(row[0]), int(row[1]), int(row[2])))
                first = False

        cur.executemany('INSERT INTO reviews_title_genres VALUES (?, ?, ?);', reviews_genres)
        con.commit()
        con.close()
