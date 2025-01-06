from django.urls import path
from user.views import LoginAPIView, RegisterUserView, CustomRefreshTokenView, LogoutApiView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    # path('refresh/', CustomRefreshTokenView.as_view(), name='refresh'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
]
