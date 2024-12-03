from django.urls import path
from .views import *

urlpatterns = [
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', CookieTokenLogoutView.as_view(), name='token_logout'),
    path('current/', CookieTokenObtainCurrentUserView.as_view(), name='current_user'),
    path('register/', RegisterView.as_view(), name='register'),

]
