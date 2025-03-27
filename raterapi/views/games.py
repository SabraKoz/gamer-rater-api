from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game, Category
from .categories import CategorySerializer

class GameSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all(), write_only=True)

    category_details = CategorySerializer(many=True, read_only=True, source='categories')

    def get_is_owner(self, obj):
        return self.context['request'].user == obj.user
    
    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'designer', 'year_released', 'num_players', 'estimated_playtime', 'age_recommendation', 'is_owner', 'categories', 'category_details']

class GameViewSet(viewsets.ViewSet):

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        designer = request.data.get('designer')
        year_released = request.data.get('year_released')
        num_players = request.data.get('num_players')
        estimated_playtime = request.data.get('estimated_playtime')
        age_recommendation = request.data.get('age_recommendation')

        game = Game.objects.create(
            user=request.user,
            title=title,
            description=description,
            designer=designer,
            year_released=year_released,
            num_players=num_players,
            estimated_playtime=estimated_playtime,
            age_recommendation=age_recommendation
        )

        category_ids = request.data.get('categories', [])
        game.categories.set(category_ids)

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)

            if game.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = GameSerializer(game, data=request.data, partial=True, context={'request': request})

            if serializer.is_valid():
                serializer.save()

                category_ids = request.data.get('categories', [])
                game.categories.set(category_ids)

                return Response(None, status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            self.check_object_permissions(request, game)

            if game.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            game.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
