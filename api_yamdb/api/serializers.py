import re
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class MeSerializer(UsersSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254,
                                   required=True)
    username = serializers.CharField(max_length=150,
                                     required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username'
        )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('me - недопустимое'
                                              'имя пользователя')
        if re.search(r'^[\w.@+-]+\Z', data['username']) is None:
            raise serializers.ValidationError('Недопустимые символы')
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
