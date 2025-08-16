from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, UserViewSet

routers = DefaultRouter()
routers.register(r"groups", GroupViewSet)
routers.register(r"users", UserViewSet)

urlpatterns = routers.urls
