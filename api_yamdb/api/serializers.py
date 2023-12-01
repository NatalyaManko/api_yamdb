from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    #author = SlugRelatedField(
#        read_only=True,
 #       slug_field='username',
  #      default=serializers.CurrentUserDefault()
   # )
    title = serializers.HiddenField(default='auto_replace_me')

    class Meta:
        model = Review
        fields = '__all__'
       # read_only_fields = ('title',)
        validators = (
            UniqueTogetherValidator(
               queryset=Review.objects.all(),
               fields=('title', 'author'),
               message=('Вы уже оценили произведение!')
            ),
        )
