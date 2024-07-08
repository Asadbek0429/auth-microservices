from django.urls import path
from .views import AuthViewSet

urlpatterns = [
    path('login/', AuthViewSet.as_view({'post': 'login'})),
    path('verify/', AuthViewSet.as_view({'post': 'verify'}))
]
