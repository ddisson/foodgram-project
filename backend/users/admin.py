from django.contrib import admin

from users.models import User, Subscribe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'is_superuser',
        'is_active', 'date_joined'
    )
    list_filter = ('email', 'username')
    list_display_links = ('username',)
    search_fields = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('Права', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {'fields': (
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2', 'is_staff', 'is_active'
        )}),
    )


@admin.register(Subscribe)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_display_links = ('user',)
    search_fields = ('user',)
