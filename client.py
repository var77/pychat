from termcolor import colored
from socketIO_client import SocketIO
import threading
import uuid
import os

ID = uuid.uuid4().hex
DEF_ROOM = 'general'
DEF_NAME = 'Anonym'
ROOM = None
NAME = None
socketIO = None

def print_header():
  print(colored('##################################################', 'blue'))
  print(colored('############', 'blue'), colored('Welcome To PyChat', 'red'), colored('###################', 'blue'))
  print(colored('##################################################', 'blue'))
  print('\n\nType', colored('/channel_name', 'green'), 'to connect to a channel\n')

def connect_to_channel(socketIO):
  global ROOM, NAME
  ROOM = input('(' + DEF_ROOM  + ')' + ' Channel name: ') or DEF_ROOM
  NAME = input('(' +  DEF_NAME  + ')' + 'Your name: ') or DEF_NAME
  socketIO.emit('join_room', ROOM)
  welcome_to_channel()

def welcome_to_channel():
  print(colored('##################################################', 'blue'))
  print(colored('########', 'blue'), colored('Welcome To Channel', 'red'), colored(ROOM, 'yellow') , colored('###############', 'blue'))
  print(colored('##################################################', 'blue'))
  print('\n\nType', colored('/channel', 'green'), 'to change channel\n')

def process_input(input):
  print("\033[A                             \033[A")
  if input == '/channel':
    connect_to_channel(socketIO)
  elif input == '/exit':
    os._exit(status=True)
  else:
    send_message(input)

def send_message(message):
  socketIO.emit('new_message', {"room": ROOM, 'message': str(message), 'name': NAME, 'id': ID})

def get_message(data):
  name = colored('You:', 'green') if data['id'] == ID else colored(data['name'] + ':', 'red')
  message = data['message'] if data['id'] == ID else colored(data['message'], 'green')

  print(name, message)


def add_listeners(socket):
  socket.off('get_message')
  socket.on('get_message', get_message)


print_header()
socketIO = SocketIO('localhost', 8888)
add_listeners(socketIO)
connect_to_channel(socketIO)

threading.Thread(target=socketIO.wait).start()


while(True):  
  process_input(input())
