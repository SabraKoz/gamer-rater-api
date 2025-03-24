from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from raterapi.views import UserViewSet, CategoryViewSet, GameViewSet, ReviewViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'games', GameViewSet, 'game')
router.register(r'reviews', ReviewViewSet, 'review')

urlpatterns = [
    path('', include(router.urls)),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('admin/', admin.site.urls),
]

