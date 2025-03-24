from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from raterapi.models import Game, Review

class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context['request'].user == obj.user

    class Meta:
        model = Review
        fields = ['id', 'game', 'user', 'content', 'rating', 'is_owner']
        read_only_fields = ['user']

class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        rating = request.data.get('rating')
        content = request.data.get('content')
        game = request.data.get('game')

        game_instance = Game.objects.get(pk=game)
        review = Review.objects.create(
            user=request.user,
            game=game_instance,
            rating=rating,
            content=content,
        )

        try:
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Game.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            self.check_object_permissions(request, review)
            if review.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            review.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    