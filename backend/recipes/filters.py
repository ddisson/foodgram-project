from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from .models import Recipe, User


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_by_user_relation(self, queryset, name, relation_name):
        if self.request.user.is_authenticated:
            return queryset.filter(
                **{f"{relation_name}__user": self.request.user}
            )
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return self.filter_by_user_relation(
                queryset,
                name,
                "favorites_recipe"
            )
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return self.filter_by_user_relation(queryset, name, "carts")
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']


class IngredientFilter(SearchFilter):
    search_param = 'name'
