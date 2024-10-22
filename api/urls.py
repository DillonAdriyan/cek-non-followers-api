from django.urls import path, include
from .views import CheckFollowersAPIView, InstagramDataView, FacebookProfileView

from .views import save_location

urlpatterns = [
    path('save-location/', save_location, name='save_location'),
    path('api/check-followers/', CheckFollowersAPIView.as_view(), name='check-followers'),
    path('api/instagram-data/', InstagramDataView.as_view(), name='instagram-data'),
    path('api/facebook-data/', FacebookProfileView.as_view(), name='facebook-data'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/facebook/', include('allauth.socialaccount.urls')),  # Facebook login
]
