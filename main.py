import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
from model import game

cred = credentials.Certificate("backend-assignment-cf21c-firebase-adminsdk-1uh9p-08a66d14be.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://backend-assignment-cf21c-default-rtdb.firebaseio.com/"
})
ref=db.reference('/')
games_ref=ref.child('games')

def initialize_grid():
    grid = [['?' for _ in range(5)] for _ in range(5)]
    return grid

# Function to print the grid
def print_grid(grid):
    for row in grid:
        print(" ".join(row))

# Function to randomly place mines and gems on the grid
def place_mines():
    mine_x, mine_y = random.randint(1, 5), random.randint(1, 5)
   # print(f"{mine_x} {mine_y}")
    return mine_x,mine_y
  
# Function to play the game
def play_game():
    grid = initialize_grid()
    mine_x,mine_y = place_mines()
    print("Welcome to Mines game!")
    print_grid(grid)
    

    player1_name = input("Enter Player 1's name: ")
    while True:
        player2_name = input("Enter Player 2's name: ")
        if(player1_name==player2_name):
            print("Name already taken \n Enter another name ")
        else:
            break
    
    game1=game.Game(id='',result='yet to be declared',winner='yet not decided',player1_name=player1_name,mine_x=mine_x,mine_y=mine_y,player2_name=player2_name,states=[grid])
    doc=games_ref.push(game1.to_json())
    games_ref.child(doc.key).update({"id":doc.key})

    # Track the number of opened tiles for each player
    player1_tiles_opened = 0
    player2_tiles_opened = 0

    # Game loop
    while True:

        # Player 1 turn
       
        print(f"\n{player1_name}'s turn:")
        while True:
                try:
                     x, y = map(int, input("Enter the coordinates to open (e.g., 1 2): ").split())
                     
                except ValueError:
                     print("Invalid input! Please enter integers separated by space.")
                else:
                    if (x<1 or x>5)or(y<1 or y>5):
                        print("Enter values between 1 and 5")
                    elif grid[x-1][y-1]=='*':
                        print("Entered cell is already open")
                    else:
                        break
        if x==mine_x and y==mine_y:
            grid[x-1][y-1]='$'
            print_grid(grid)
            print("Boom! Mine hit! Game Over!")
            print(f"{player2_name} wins!")
            game1.states.append(grid)
            games_ref.child(doc.key).update({
                "states":game1.states,
                "winner": player2_name,
                "result": "win"
            })
            break    
        else:
            grid[x-1][y-1] = '*'
            print_grid(grid)
            game1.states.append(grid)
            games_ref.child(doc.key).update({
                "states":game1.states
            })
            player1_tiles_opened += 1

        # Player 2 turn
        print(f"\n{player2_name}'s turn:")
        while True:
                try:
                     x, y = map(int, input("Enter the coordinates to open (e.g., 1 2): ").split())
                     
                except ValueError:
                     print("Invalid input! Please enter integers separated by space.")
                else:
                    if (x<1 and x>5)or(y<1 and y>5):
                        print("Enter values between 1 and 5")
                    elif grid[x-1][y-1]=='*':
                        print("Entered cell is already open")
                    else:
                        break
        if x==mine_x and y==mine_y:
            grid[x-1][y-1]='$'
            print_grid(grid)
            print("Boom! Mine hit! Game Over!")
            print(f"{player1_name} wins!")
            game1.states.append(grid)
            games_ref.child(doc.key).update({
                "states":game1.states,
                "winner": player1_name,
                "result": "win"
            })
            break
        else:
            grid[x-1][y-1] = '*'
            print_grid(grid)
            game1.states.append(grid)
            player2_tiles_opened += 1
            games_ref.child(doc.key).update({
                "states":game1.states
            })

        # Check for draw condition
        if player1_tiles_opened == 12 and player2_tiles_opened == 12:
            print("It's a draw! Both players opened 12 tiles without hitting a mine.")
            ref.push({
                "result": "draw",
                "winner":"none"
            })
            break

# Main function to start the game
if __name__ == "__main__":
    play_game()