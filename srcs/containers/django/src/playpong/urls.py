from django.urls import path
# from . import views
from .views import home, sign_up, UserLoginView, play_pong, start_remote_game, join_remote_game, get_csrf_token


urlpatterns = [
    path('', home, name='home'), # Publicly accessible
    path('pong/', play_pong, name='play_pong'),
    path('sign_up/', sign_up, name='sign_up'),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/game/start-remote/', start_remote_game, name='start_remote_game'),
    path('api/game/join-remote/', join_remote_game, name='join_remote_game'),
    path('api/csrf-token/', get_csrf_token, name='get_csrf_token'),
    # Add other paths as needed
]