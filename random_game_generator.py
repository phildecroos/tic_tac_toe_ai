import os
import random

clear = lambda: os.system('cls')
clear()
print("Starting...")

data = open("random_games.txt", "w+")
games = 10

def placed(game_state, check, val):
  return (game_state.find(val) != -1 and game_state.find(val) % 2 == check)

def game_over(game_state):
  if len(game_state) == 10:
    return True
  
  check = (len(game_state) - 1) % 2

  if placed(game_state, check, "0") and placed(game_state, check, "1") and placed(game_state, check, "2"):
      return True
  if placed(game_state, check, "0") and placed(game_state, check, "3") and placed(game_state, check, "6"):
      return True
  if placed(game_state, check, "0") and placed(game_state, check, "4") and placed(game_state, check, "8"):
      return True
  if placed(game_state, check, "1") and placed(game_state, check, "4") and placed(game_state, check, "7"):
      return True
  if placed(game_state, check, "2") and placed(game_state, check, "4") and placed(game_state, check, "6"):
      return True
  if placed(game_state, check, "2") and placed(game_state, check, "5") and placed(game_state, check, "8"):
      return True
  if placed(game_state, check, "3") and placed(game_state, check, "4") and placed(game_state, check, "5"):
      return True
  if placed(game_state, check, "6") and placed(game_state, check, "7") and placed(game_state, check, "8"):
      return True
  
  return False

for i in range(games):
  curr_game = ""
  free_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]

  first_player = random.randint(0, 1)
  if first_player:
    curr_game += "x"
  else:
    curr_game += "o"
    
  while not game_over(curr_game):
    new_move = random.randint(0, 8)
    while not new_move in free_moves:
      new_move = random.randint(0, 8)
    free_moves.remove(new_move)
    curr_game += str(new_move)
  
  data.write(curr_game + "\n")

  unit = 25
  if ((i + 1) % (games/unit) == 0):
    clear()
    print("Progress: ", end = "")
    completed = int((i + 1) / (games/unit))
    for j in range(completed):
      print("#", end = "")
    for k in range(unit - completed - 1):
      print("-", end = "")
    if unit - completed > 0:
      print("-")
    else:
      print("\nDone")

data.close()