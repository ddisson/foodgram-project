from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Tag, Recipe, Favorite, ShoppingCart, IngredientRecipe
from .permissions import IsAuthenticatedOwnerOrReadOnly
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer, FollowRecipeSerializer
from .utils import download_pdf


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _handle_favorite_shopping(self, request, pk, model, errors):
        if request.method == 'POST':
            if model.objects.filter(user=request.user, recipe__id=pk).exists():
                return Response(errors['recipe_in'], status=status.HTTP_400_BAD_REQUEST)

            recipe = get_object_or_404(Recipe, id=pk)
            model.objects.create(user=request.user, recipe=recipe)
            serializer = FollowRecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        recipe = model.objects.filter(user=request.user, recipe__id=pk)
        if recipe.exists():
            recipe.delete()
            return Response({'msg': 'Успешно удалено'}, status=status.HTTP_204_NO_CONTENT)

        return Response(errors['recipe_not_in'], status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', 'DELETE'], detail=True, permission_classes=[AllowAny])
    def favorite(self, request, pk):
        errors = {
            'recipe_in': {'errors': 'Рецепт уже в избранном'},
            'recipe_not_in': {'error': 'Рецепта нет в избранном'}
        }
        return self._handle_favorite_shopping(request, pk, Favorite, errors)

    @action(methods=['POST', 'DELETE'], detail=True, permission_classes=[AllowAny])
    def shopping_cart(self, request, pk):
        errors = {
            'recipe_in': {'errors': 'Рецепт уже в списке покупок'},
            'recipe_not_in': {'error': 'Рецепта нет в спике покупок'}
        }
        return self._handle_favorite_shopping(request, pk, ShoppingCart, errors)

    @action(methods=['GET'], detail=False, permission_classes=[AllowAny])
    def download_shopping_cart(self, request):
        ingredients_data = (
            IngredientRecipe.objects.filter(recipe__carts__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(sum_amount=Sum('amount'))
        )
        ingredients = {
            item['ingredient__name'].capitalize(): [item['sum_amount'], item['ingredient__measurement_unit']]
            for item in ingredients_data
        }
        ingredients_list = [
            f"{str(ind).zfill(2)}. {name} - {values[0]} {values[1]}"
            for ind, (name, values) in enumerate(ingredients.items(), 1)
        ]
        return download_pdf(ingredients_list)
