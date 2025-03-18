from django.urls import path, include
from rest_framework.routers import DefaultRouter
from assistant.views import AssistantViewSet

# Crear el router
router = DefaultRouter()

# Registrar el ViewSet
router.register(r'', AssistantViewSet, basename='assistant')

# Definir los patrones de URL
urlpatterns = [
    path('', include(router.urls)),
]