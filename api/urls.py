from django.urls import path
from .views import CheckFollowersAPIView

urlpatterns = [
    path('api/check-followers/', CheckFollowersAPIView.as_view(), name='check-followers'),
]
