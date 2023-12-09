from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для действий с
       использованием прав администратора"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class MeSerializer(UsersSerializer):
    """Сериализатор пользователя для действий с
       использованием прав администратора"""

    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

        def new_validators(field):
            new_validators = filter(
                lambda validator: not isinstance(validator,
                                                 validators.UniqueValidator),
                self.fields[field].validators
            )
            self.fields[field].validators = new_validators

        new_validators(field="email")
        new_validators(field="username")

    class Meta:
        model = User
        fields = (
            'email',
            'username'
        )

    def validate(self, data):
        username = data["username"]
        email = data["email"]
        if User.objects.filter(username__iexact=username,
                               email__iexact=email).exists():
            return data
        if (
            User.objects.filter(Q(email__iexact=email)
                                | Q(username__iexact=username)
                                ).exists()
        ):
            raise serializers.ValidationError()
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена"""

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        new_validators = filter(
            lambda validator: not isinstance(validator,
                                             validators.UniqueValidator),
            self.fields["username"].validators
        )
        self.fields["username"].validators = new_validators

    class Meta:
        model = User
        fields = (
            'confirmation_code',
            'username'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Отзывов"""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.context.get('request').user
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    f'Вы уже оценили произведение: {title}!')
            return data
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категорий"""

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров"""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Чтение данных произведений"""

    genre = GenreSerializer(many=True,
                            read_only=False)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор Произведений"""

    genre = serializers.SlugRelatedField(slug_field='slug',
                                         many=True,
                                         read_only=False,
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(read_only=False,
                                            required=True,
                                            slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category')
