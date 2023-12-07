import csv
import sqlite3
from datetime import datetime

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Заполняет базу данных из файлов CSV'

    def handle(self, *args, ** options):    # noqa: C901

        paths = {
            'genre': 'static/data/genre.csv',
            'category': 'static/data/category.csv',
            'title': 'static/data/titles.csv',
            'user': 'static/data/users.csv',
            'review': 'static/data/review.csv',
            'comment': 'static/data/comments.csv',
            'title_genre': 'static/data/genre_title.csv',
        }

        for name, path in paths.items():
            with (open(path, newline='', encoding='utf-8') as csvfile):
                reviews_title_genre = []
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                first = True
                for row in reader:
                    if not first:
                        if name == 'genre':
                            _, created = Genre.objects.get_or_create(
                                id=int(row[0]),
                                name=row[1],
                                slug=row[2],)

                        elif name == 'category':
                            _, created = Category.objects.get_or_create(
                                id=int(row[0]),
                                name=row[1],
                                slug=row[2],)

                        elif name == 'title':
                            _, created = Title.objects.get_or_create(
                                id=int(row[0]),
                                name=row[1],
                                year=int(row[2]),
                                category_id=int(row[3]),)

                        elif name == 'user':
                            _, created = User.objects.get_or_create(
                                id=row[0],
                                username=row[1],
                                email=row[2],
                                role=row[3],
                            )

                        elif name == 'review':
                            _, created = Review.objects.get_or_create(
                                id=int(row[0]),
                                title_id=int(row[1]),
                                text=row[2],
                                author_id=int(row[3]),
                                score=int(row[4]),
                                pub_date=datetime.strptime(
                                    row[5],
                                    '%Y-%m-%dT%H:%M:%S.%fZ'))

                        elif name == 'comment':
                            _, created = Comment.objects.get_or_create(
                                id=int(row[0]),
                                review_id=int(row[1]),
                                text=row[2],
                                author_id=int(row[3]),
                                pub_date=datetime.strptime(
                                    row[4], '%Y-%m-%dT%H:%M:%S.%fZ'))
                        elif name == 'title_genre':
                            reviews_title_genre.append((int(row[0]),
                                                        int(row[1]),
                                                        int(row[2])))
                    first = False

        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        cur.executemany(
            'INSERT INTO reviews_titlegenre VALUES (?, ?, ?);',
            reviews_title_genre)
        con.commit()
        con.close()
