from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

from backend.constants import (
    USER_MAIL_MAX_LENGTH, USER_NAME_MAX_LENGTH
)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        blank=False,
        unique=True,
        max_length=USER_MAIL_MAX_LENGTH,
        error_messages={
            'unique': 'Такой адрес электронной почты уже зарегистрирован.'
        },
    )
    username = models.CharField(
        verbose_name='логин',
        max_length=USER_NAME_MAX_LENGTH,
        unique=True,
        help_text='Не более 150 символов.',
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с таким именем уже зарегистрирован.'
        },
    )
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if self.username == 'me':
            return ValidationError('Username не может быть "me".')
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.is_superuser

    def get_short_name(self):
        return f'{self.username[:15]}'

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='Пользователь не может быть назван me!',
            )
        ]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='Нельзя подписаться на самого себя!',
            )
        ]
