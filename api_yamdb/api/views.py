from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .mixins import CreateListDestroyMixin, CustomUpdateMixin, RetrieveMixin
from .permissions import AdminPermission, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          GetTokenSerializer,
                          MeSerializer,
                          ReviewSerializer,
                          SignUpSerializer,
                          TitleCreateSerializer,
                          TitleSerializer,
                          UsersSerializer)

User = get_user_model()


class APISignup(APIView):
    """Регистрация и получение кода подтверждения по почте"""

    def send_email(self, username, email, confirmation_code):
        email_body = (
            f'Здравствуйте, {username}.'
            f'\nВаш код доступа: {confirmation_code}'
        )
        email_data = {
            'email_body': email_body,
            'to_email': email,
            'email_subject': 'Код доступа'
        }
        email = EmailMessage(
            subject=email_data['email_subject'],
            body=email_data['email_body'],
            to=[email_data['to_email']]
        )
        email.send()

    def generate_confirmation_code(self, username):
        user = User.objects.get(username=username)
        confirmation_code = default_token_generator.make_token(user)
        return confirmation_code

    def save_confirmation_code(self, username, code):
        user = User.objects.filter(username=username)
        user.update(confirmation_code=code)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        username = user_data['username']
        email = user_data['email']
        if User.objects.filter(username__iexact=username,
                               email__iexact=email).exists():
            confirmation_code = self.generate_confirmation_code(username)
            self.send_email(username=username,
                            email=email,
                            confirmation_code=confirmation_code)
            self.save_confirmation_code(username,
                                        confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.save()
        confirmation_code = self.generate_confirmation_code(username)
        self.send_email(username=username,
                        email=email,
                        confirmation_code=confirmation_code)
        self.save_confirmation_code(username,
                                    confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    """Получение токена"""

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(CustomUpdateMixin,
                   CreateListDestroyMixin,
                   RetrieveMixin):
    """Создание, получение, изменение объектов User администратором.
       Получение и изменение пользователем своего объекта User"""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_me(self, request):
        serializer = MeSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(CustomUpdateMixin,
                    CreateListDestroyMixin,
                    RetrieveMixin):
    """Создание, изменение и удаление отзывов"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('text', 'author', 'score')
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews_title.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(CustomUpdateMixin,
                     CreateListDestroyMixin,
                     RetrieveMixin):
    """Создание, изменение и удаление комментариев"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('text', 'author',)
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyMixin):
    """Создание, изменение и удаление категорий"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenresViewSet(CreateListDestroyMixin):
    """Создание, изменение и удаление жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitlesViewSet(CustomUpdateMixin,
                    CreateListDestroyMixin,
                    RetrieveMixin):
    """Создание, изменение и удаление произведений"""

    queryset = Title.objects.all()
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, )
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    search_fields = ('name', 'year', 'category', 'genre',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleSerializer

    def get_queryset(self):
        if self.request.method in 'GET':
            return Title.objects.prefetch_related(
                'reviews_title__title'
            ).annotate(rating=Avg('reviews_title__score'))
        return Title.objects.all()
