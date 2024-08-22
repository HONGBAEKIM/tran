import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.conf import settings
import requests

class ChatConsumer(AsyncWebsocketConsumer):
    # This method is called when a WebSocket connection is established.
    async def connect(self): 
        self.room_group_name = 'chatroom'

        # consumer (client) is joining the group where messages will be broadcasted.
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accepts the WebSocket connection, allowing communication to proceed.
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # seceive function send message 
    # and chat_message check client who triggered the chat_message event?

    async def receive(self, text_data):
        try:
            # Parses the incoming message from JSON format.
            text_data_json = json.loads(text_data)
            # Get the message from the parsed JSON data
            message = text_data_json['message']

            # Send message to channel_layer group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except KeyError:
            # Handle the case where 'message' key is missing
            await self.send(text_data=json.dumps({
                'error': 'No message key in WebSocket data'
            }))
        except json.JSONDecodeError:
            # Handle invalid JSON
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON data received'
            }))
    
    # Why chat_message is Necessary
    # it handles that the message is sent to multiple clients (or users) who are part of that group
    async def chat_message(self, event):
        # Receives an event dictionary containing the message (event['message']).
        message = event['message']

        # Sends the message back to the client who triggered the chat_message event.
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))



class PingpongConsumer(AsyncWebsocketConsumer):
    # A set keeps track of currently connected players.
    connected_players = set()
    # identifying which player is controlling which paddle
    player_roles = {}  
    game_started = False

    ball = {'x': 300, 'y': 200, 'dx': 8, 'dy': 8}
    player1 = {'y': 200, 'dy': 0, 'score': 0}  
    player2 = {'y': 200, 'dy': 0, 'score': 0}  

    async def connect(self):
        self.room_group_name = 'pingpong'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.fetch_initial_data()

        # Assign player roles
        if len(self.connected_players) % 2 == 0:
            self.player_roles[self.channel_name] = 'player1'
        elif len(self.connected_players) % 2 == 1:
            self.player_roles[self.channel_name] = 'player2'

        # Track connected players
        self.connected_players.add(self.channel_name)

        # Broadcasting Update to Group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'players_update',
                'players': len(self.connected_players)
            }
        )

        # Ensure only two players can connect
        if len(self.connected_players) > 10:
            await self.close()

    async def disconnect(self, close_code):
        # Remove player from connected players
        self.connected_players.discard(self.channel_name)
        try:
            del self.player_roles[self.channel_name]
        except KeyError:
            pass  # Handle the case where self.channel_name does not exist

        # Broadcasting Update to Group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'players_update',
                'players': len(self.connected_players)
            }
        )

        # Reset game if all players disconnect
        if len(self.connected_players) == 0:
            self.game_started = False
            # await self.reset_game_state() 
            # await self.reset_game_state() 
                        # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state()             # await self.reset_game_state() 
            # await self.reset_game_state() 
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def reset_game_state(self):
        # Reset all game state variables
        self.ball = {'x': 300, 'y': 200, 'dx': 8, 'dy': 8}
        self.player1 = {'y': 200, 'dy': 0, 'score': 0}
        self.player2 = {'y': 200, 'dy': 0, 'score': 0}

        # Broadcast the updated game state to all connected players
        await self.broadcast_game_state()

    async def fetch_initial_data(self):
        url = 'https://10.15.203.3:8443/api/players/'
        try:
            response = await sync_to_async(requests.get)(url, verify=False)  # Disable SSL verification
            data = response.json()
            # Handle the data as needed
        except SSLError as e:
            print(f"SSL Error: {str(e)}")
            # Handle SSL error accordingly
        except Exception as e:
            print(f"Error fetching initial data: {str(e)}")


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type', '')
            data = data.get('data', {})

            if message_type == 'initiate_remote_play':
                role = 'A' if len(self.connected_players) % 2 == 1 else 'B'

                # Send a message to the group indicating remote play initiation
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'remote_play_initiated',
                        'role': role
                    }
                )

                # Start the game if both players are ready
                if len(self.connected_players) % 2 == 0 and not self.game_started:
                    await self.start_game()
            
            elif message_type == 'player_action':
                await self.handle_player_action(data)

            else:
                await self.send(text_data=json.dumps({
                    'error': f'Unsupported message type: {message_type}'
                }))
        
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON data received'
            }))


    async def remote_play_initiated(self, event):
        role = event['role']
        await self.send(text_data=json.dumps({
            'type': 'remote_play_initiated',
            'role': role
        }))

    async def handle_player_action(self, data):
        try:
            # Determines which player ('player1' or 'player2') the current WebSocket client 
            player = self.player_roles[self.channel_name]
            
            # how much the player's paddle moves up or down 
            dy = data.get('dy')

            if player == 'player1':
                self.player1['dy'] = dy
            elif player == 'player2':
                self.player2['dy'] = dy

            await self.broadcast_game_state()
        except KeyError:
            print(f"KeyError: Could not find player role for channel {self.channel_name}")
        except Exception as e:
            print(f"Exception in handle_player_action: {str(e)}")
    
    
    async def players_update(self, event):
        try:
            # send msg to the client over the websocket
            # before moving on to the next line
            await self.send(text_data=json.dumps({
                'type': 'players_update',
                'players': event['players']
            }))
        except Exception as e:
            # Log the exception or handle it appropriately
            print(f"Error sending message: {str(e)}")


    async def start_game(self):
        if not self.game_started:
            # Perform game start operations here
            self.game_started = True
            

            # Send a 'game_start' message to the channel layer group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_start',
                }
            )
            # Broadcast the initial game state to all clients
            await self.broadcast_game_state()
            # Start a task to update the game state continuously
            asyncio.create_task(self.update_game_state())

    # sending a WebSocket message back to the client
    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_start',
        }))


    async def update_game_state(self):
        while self.game_started:
            self.update_ball()
            self.update_paddles()
            await self.broadcast_game_state()
            await asyncio.sleep(0.03)  # Update game state every 30ms   
    
    # checking for collisions, updating positions, and handling scoring.
    def update_ball(self):
        self.ball['x'] += self.ball['dx']
        self.ball['y'] += self.ball['dy']

        # Check collision with top and bottom walls
        if self.ball['y'] <= 0 or self.ball['y'] >= 400:
            self.ball['dy'] *= -1

        # Check collision with paddles
        if (self.ball['x'] <= 60 and self.player1['y'] < self.ball['y'] < self.player1['y'] + 50 and self.ball['dx'] < 0) or \
           (self.ball['x'] >= 530 and self.player2['y'] < self.ball['y'] < self.player2['y'] + 50 and self.ball['dx'] > 0):
            self.ball['dx'] *= -1

        # Check if ball goes out of bounds
        if self.ball['x'] <= 0:
            # Player 2 scores
            self.player2['score'] += 1
            if self.player2['score'] >= 10:
                asyncio.create_task(self.end_game()) 
            else:
                self.ball = {'x': 300, 'y': 200, 'dx': 8, 'dy': 8}  # Reset ball position
        elif self.ball['x'] >= 600:
            # Player 1 scores
            self.player1['score'] += 1
            if self.player1['score'] >= 10:
                asyncio.create_task(self.end_game()) 
            else:
                self.ball = {'x': 300, 'y': 200, 'dx': 8, 'dy': 8} 

        self.broadcast_game_state()

    def update_paddles(self):
        self.player1['y'] += self.player1['dy']
        self.player2['y'] += self.player2['dy']

        # Ensure paddles stay within the bounds of the game area
        self.player1['y'] = max(0, min(self.player1['y'], 400))
        self.player2['y'] = max(0, min(self.player2['y'], 400))

    # Continuously sending the updated game state to connected players ensures that
    # all players see the same game state and can interact with it correctly.
    async def broadcast_game_state(self):
        # current state of player1, player2, ball
        game_state = {
            'player1': self.player1,
            'player2': self.player2,
            'ball': self.ball,
        }
        
        # Sending the Game State to the Group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_state_update',
                'data': game_state
            }
        )
    # Updating Each Client
    async def game_state_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_state_update',
            'data': event['data']
        }))

 

    async def end_game(self):
        self.game_started = False
        # Optionally, perform any end-of-game logic, e.g., announcing winner
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_end',
                'winner': 'player1' if self.player1['score'] >= 10 else 'player2'
            }
        )
    
    async def game_end(self, event):
        winner = event['winner']
        await self.send(text_data=json.dumps({
            'type': 'game_end',
            'winner': winner
        }))
