import secrets
import string
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import AdminPermission
from api.serializers import (GetTokenSerializer, MeSerializer,
                             SignUpSerializer, UsersSerializer)

User = get_user_model()


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def send_email(email_data):
        email = EmailMessage(
            subject=email_data['email_subject'],
            body=email_data['email_body'],
            to=email_data['to_email']
        )
        email.send()

    def generate_confirmation_code():
        letters_and_digits = string.ascii_letters + string.digits
        confirmation_code = ''.join(secrets.choice(
            letters_and_digits) for i in range(8))
        return confirmation_code

    def save_confirmation_code(username, code):
        user = User.objects.filter(username=username)
        user.confirmation_code = code
        user.save(update_fields=['confirmation_code'])

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        confirmation_code = self.generate_confirmation_code()
        email_body = (
            f'Здравствуйте, {user_data["username"]}.'
            f'\nВаш код доступа: {confirmation_code}'
        )
        email_data = {
            'email_body': email_body,
            'to_email': user_data['email'],
            'email_subject': 'Код доступа'
        }
        self.send_email(email_data)
        if User.objects.filter(username=user_data['username']).exists():
            self.save_confirmation_code(user_data['username'],
                                        confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.save()
        self.save_confirmation_code(user_data['username'],
                                    confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
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
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminPermission,)
    lookup_field = 'username'


class MeViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = MeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user
