import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from recipes.serializers import SubscribeRecipeSerializer
from .models import User, Subscribe


class BaseUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        return Subscribe.objects.filter(author=obj, user=request_user).exists()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class UserReadSerializer(BaseUserSerializer):
    pass


class UserWriteSerializer(BaseUserSerializer):
    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return super().validate(data)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('password',)
        extra_kwargs = {'password': {'write_only': True}}


class SubscribeListSerializer(BaseUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes.count', read_only=True
    )

    def get_recipes(self, obj):
        request = self.context['request']
        limit = request.GET.get('recipes_limit', 10)
        try:
            limit = int(limit)
        except ValueError:
            limit = 10
        recipes = obj.recipes.all()[:limit]
        serializer = SubscribeRecipeSerializer(
            recipes,
            many=True,
            context={'request': request}
        )
        return serializer.data

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('recipes', 'recipes_count')


class SubscribeCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all()
    )

    def validate(self, data):
        user = data['user']
        author = data['author']
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return data

    class Meta:
        model = Subscribe
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на данного автора'
            )
        ]
