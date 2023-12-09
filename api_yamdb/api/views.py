import django_filters
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title

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


class UsersViewSet(ModelViewSet):
    """Создание, получение, изменение объектов User администратором.
       Получение и изменение пользователем своего объекта User"""
    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete',)
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Создание, изменение и удаление отзывов"""
    http_method_names = ('get', 'post', 'patch', 'delete',)
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('text', 'author', 'score')
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        title_id = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title_id.reviews_title.filter(title=title_id)

    def perform_create(self, serializer):
        title_id = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    """Создание, изменение и удаление комментариев"""
    http_method_names = ('get', 'post', 'patch', 'delete',)
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('text', 'author',)
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        review_id = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review_id.comments.all()

    def perform_create(self, serializer):
        review_id = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review_id)


class CategoryViewSet(viewsets.ModelViewSet):
    """Создание, изменение и удаление категорий"""
    queryset = Category.objects.all()
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenresViewSet(viewsets.ModelViewSet):
    """Создание, изменение и удаление жанров"""
    queryset = Genre.objects.all()
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='iexact')
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete',)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, )
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    search_fields = ('name', 'year', 'category', 'genre',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleSerializer
