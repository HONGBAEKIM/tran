# from django.shortcuts import render
# from django.http import HttpResponse

# def play_pong(request):
#     return render(request, 'Pong.html')

# # Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import RegisterForm
import json
import uuid

# to check remote user CSRF token before access the remote game 
#from django.middleware.csrf import get_token

#rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


# Helper functions to generate game_id and session_token
def generate_game_id():
    return str(uuid.uuid4())

def generate_session_token():
    return str(uuid.uuid4())

# ---------------------------------------------------------------
def home(request):
    return render(request, "main/home.html")

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/pong')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/sign_up.html', {"form": form})
# ---------------------------------------------------------------


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        # Your authentication logic to verify credentials and get user
        user = authenticate(username=request.data['username'], password=request.data['password'])

        if user:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            # Return tokens as JSON response
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@login_required
def play_pong(request):
    context = {
        'is_logged_in': request.user.is_authenticated
    }
    return render(request, 'main/pong.html', context)


@csrf_exempt
@require_POST
@login_required
def start_remote_game(request):
    data = json.loads(request.body.decode('utf-8'))
    player1_name = data.get('player1Name', '')
    player2_name = data.get('player2Name', '')
    
    # Start the remote game session (your logic here)
    game_mode = 'remoteuser-vs-remoteuser'
    game_id = generate_game_id()  # You need to implement this function
    session_token = generate_session_token()  # You need to implement this function
    
    game_data = {
        'player1Name': player1_name,
        'player2Name': player2_name,
        'gameMode': game_mode,
        'gameId': game_id,
        'sessionToken': session_token
    }

    return JsonResponse({'success': True, **game_data})


@csrf_exempt
@require_POST
@login_required
def join_remote_game(request):
    data = json.loads(request.body.decode('utf-8'))
    game_id = data.get('gameId', '')
    session_token = data.get('sessionToken', '')

    if valid_game_session(game_id, session_token):
        game_session = get_game_session_by_id(game_id)
        game_session['remotePlayer'] = 'Remote Player'

        update_game_session(game_session)

        return JsonResponse({
            'success': True,
            'message': 'Remote player joined successfully',
            'gameState': game_session
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid game ID or session token'
        }, status=400)

def get_csrf_token(request):
    csrf_token = request.META.get('CSRF_COOKIE', '')
    return JsonResponse({'csrfToken': csrf_token})



