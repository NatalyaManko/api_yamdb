from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    text = models.TextField('Текст')
#    title = models.ForeignKey(
#        Title,
#        on_delete=models.CASCADE,
#        related_name='reviews',
#        verbose_name='Произведение'
#        )
#    author = models.ForeignKey(
#        User,
#        on_delete=models.CASCADE,
#        related_name='reviews',
#        verbose_name='Автор'
#        )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)]
        )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
#        constraints = [
#            models.UniqueConstraint(
#                fields=['title', 'author'],
#                name='unique_title_author'
#            )
#        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text
