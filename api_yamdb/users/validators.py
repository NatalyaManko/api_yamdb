import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            ('me - недопустимое имя пользователя'),
        )
    if re.search(r'^[\w.@+-]+\Z', value) is None:
        raise ValidationError('Недопустимые символы')
