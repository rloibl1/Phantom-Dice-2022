from game_library import *

# Initialize a New Game
new_game = PhantomDice()

# Variable to Alternate Turns
turn = False

# Game Loop
while True:
    # Print the Board
    new_game.print_board()
    # Roll Die
    roll = new_game.roll_dice()
    print(f"{new_game.player_names[turn]}'s turn | Dice roll: {roll}")
    # Player decides where to place the die
    while True:
        column = input("Where will you place the die (1,2,3): ")
        valid = new_game.update_board(player=int(turn), column=int(column)-1, roll=roll)
        # If the Command Was Valid then Break
        if valid:
            break
    # Update the Score
    new_game.update_score()
    # Endgame Check (True return indicates game has ended)
    if new_game.endgame_check():
        break
    # Switch Turns
    turn = not turn
