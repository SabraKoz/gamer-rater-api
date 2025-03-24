from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game
from .categories import CategorySerializer

class GameSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)

    def get_is_owner(self, obj):
        return self.context['request'].user == obj.user
    
    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'designer', 'year_released', 'num_players', 'estimated_playtime', 'age_recommendation', 'is_owner', 'categories']

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

            self.check_object_permissions(request, game)

            serializer = GameSerializer(data=request.data)

            if serializer.is_valid():
                game.title = serializer.validated_data['title']
                game.description = serializer.validated_data['description']
                game.designer = serializer.validated_data['designer']
                game.year_released = serializer.validated_data['year_released']
                game.num_players = serializer.validated_data['num_players']
                game.estimated_playtime = serializer.validated_data['estimated_playtime']
                game.age_recommendation = serializer.validated_data['age_recommendation']
                game.save()

                category_ids = request.data.get('categories', [])
                game.categories.set(category_ids)

                serializer = GameSerializer(game, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            self.check_object_permissions(request, game)
            game.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
