# Phantom Dice Game
import pygame
import random
import time
import sys
from game_library import *
from random_action import RandomAgent
from greedy_action import GreedyAgent
from monte_carlo_rollout import MonteCarloAgent
from expectiminimax import MinimaxAgent

# Import keys from keyboard
from pygame.locals import (
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_ESCAPE,
    KEYDOWN
)

# Startup
pygame.init()
new_game = PhantomDice()
pygame.display.set_caption('Phantom Dice')
icon = pygame.image.load("./assets/dice_icon.png")
pygame.display.set_icon(icon)

# Variable to Alternate Turns
turn = False

# Screen Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# Win Banner Constants
BANNER_WIDTH = 400
BANNER_HEIGHT = 200

# Text Fonts
sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(sysfont, 28)
menu_font = pygame.font.Font('./assets/fonts/Orbitron_Medium.ttf', 42)
help_font1 = pygame.font.Font('./assets/fonts/Orbitron_Medium.ttf', 24)
help_font2 = pygame.font.Font('./assets/fonts/Orbitron_Medium.ttf', 16)

# Color Constants
BLACK = (0, 0, 0)
LIGHT_GREY = (224, 224, 224)
DARK_GREEN = (9, 113, 54)

# Location Constants

# Screen Center
center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))

# Board Slots
a1 = (292, 25)
a2 = (292, 100)
a3 = (292, 175)
a4 = (367, 25)
a5 = (367, 100)
a6 = (367, 175)
a7 = (442, 25)
a8 = (442, 100)
a9 = (442, 175)

# Board Slots
b1 = (292, 260)
b2 = (292, 335)
b3 = (292, 410)
b4 = (367, 260)
b5 = (367, 335)
b6 = (367, 410)
b7 = (442, 260)
b8 = (442, 335)
b9 = (442, 410)

# Menu Slots
m1 = (100, 100)
ms1 = (40, 116)
m2 = (100, 175)
ms2 = (30, 191)
m3 = (100, 250)
ms3 = (30, 266)
m4 = (100, 325)
ms4 = (30, 341)
m5 = (100, 400)
ms5 = (30, 416)

# Help Box & Text Locations
h1 = (200, 100)
h2 = (385, 110)
h3 = (210, 150)
h4 = (210, 175)
h5 = (210, 210)
h6 = (210, 245)
h7 = (210, 270)
h8 = (210, 295)

# Dice Roll Locations
c1 = (71, 355)
c2 = (582, 45)
cd1 = (114, 373)
cd2 = (625, 63)

# Score Display Locations
sc0 = (70, 320)
sc1 = (585, 160)

# Sprite Locations
sp0 = (114, 250)
sp1 = (628, 185)

# Win Banner Location
w1 = ((SCREEN_WIDTH / 2) - (BANNER_WIDTH / 2), (SCREEN_HEIGHT / 2) - (BANNER_HEIGHT / 2))

# Size Constants
s1 = (65, 65)
s2 = (150, 100)
s3 = (400, 200)
s4 = (200, 400)
s5 = (525, 365)

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Load Images
bg = pygame.image.load("./assets/mosaic_background.jpg")
title_img = pygame.image.load("./assets/title_dice.png")
d1 = pygame.image.load("./assets/dice_1.png")
d2 = pygame.image.load("./assets/dice_2.png")
d3 = pygame.image.load("./assets/dice_3.png")
d4 = pygame.image.load("./assets/dice_4.png")
d5 = pygame.image.load("./assets/dice_5.png")
d6 = pygame.image.load("./assets/dice_6.png")
p_sprite1 = pygame.image.load("assets/astro.png")
p_sprite2 = pygame.image.load("assets/woman.png")
p_sprite3 = pygame.image.load("assets/man.png")
a_sprite1 = pygame.image.load("assets/randy_random.png")
a_sprite2 = pygame.image.load("assets/bernard_bear.png")
a_sprite3 = pygame.image.load("./assets/lil_phantom.png")
a_sprite4 = pygame.image.load("assets/danny_phantom.png")
a_sprite5 = pygame.image.load("assets/dice_demon.png")


# Maps die roll to die image and screen location
def roll_mapper(_roll, _turn):
    roll_map = f"d{_roll}"
    # Opponent Turn
    if _turn:
        # Programmatically select the correct die image
        screen.blit(globals()[roll_map], cd2)
    # Player Turn
    else:
        # Programmatically select the correct die image
        screen.blit(globals()[roll_map], cd1)


# Maps board state to correct die images and screen locations
def display_mapper(names, scores, board):
    # Display Board
    # Loop Through the Entire Board
    for player in range(board.shape[0]):
        for col in range(board.shape[1]):
            for row in range(board.shape[2]):
                # If the board slot is empty don't display a dice image
                if board[player, row, col] != 0:
                    # Map to the correct dice image
                    roll_map = f'd{board[player, row, col]}'
                    # Map to the correct location on the screen
                    slot_map = (col * 3) + (row + 1)
                    # Adjust the location based on the player
                    if player == 0:
                        loc_map = f'b{slot_map}'
                    else:
                        loc_map = f'a{slot_map}'
                    # Write the dice to the specified location
                    screen.blit(globals()[roll_map], globals()[loc_map])

    # Display Scores
    # Player
    player_score_text = f"{names[0]}'s score: {scores[0]}"
    img0 = font.render(player_score_text, True, LIGHT_GREY)
    screen.blit(img0, sc0)
    # Opponent
    opponent_score_text = f"{names[1]}'s score: {scores[1]}"
    img1 = font.render(opponent_score_text, True, LIGHT_GREY)
    screen.blit(img1, sc1)


# Centers the within another reference box
def center_text(text_box, reference_box):
    # Calculate Coordinates
    x = reference_box.centerx - (text_box.get_width() / 2)
    y = reference_box.centery - (text_box.get_height() / 2)

    # Keep Coordinates on the Screen
    # Width
    if x < 0:
        x = 0
    elif x + text_box.get_width() > SCREEN_WIDTH:
        x = SCREEN_WIDTH - text_box.get_width()
    # Height
    if y < 0:
        y = 0
    elif x + text_box.get_width() > SCREEN_WIDTH:
        x = SCREEN_WIDTH - text_box.get_width()
    return x, y


# Place the die based on user input
def keystroke():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_1:
                return 0
            elif event.type == KEYDOWN and event.key == K_2:
                return 1
            elif event.type == KEYDOWN and event.key == K_3:
                return 2
            elif event.type == KEYDOWN and event.key == K_4:
                return 3
            elif event.type == KEYDOWN and event.key == K_5:
                return 4
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return -1
            elif event.type == pygame.QUIT:
                return -1


def menu():
    # ===============
    # Draw the Screen
    # ===============

    # Background
    screen.blit(bg, (0, 0))

    # Game Title & Picture
    title_text = menu_font.render('Phantom Dice', True, DARK_GREEN)
    screen.blit(title_text, ((SCREEN_WIDTH / 2) - (title_text.get_width() / 2) + 32, 25))
    screen.blit(title_img, ((SCREEN_WIDTH / 2) - (title_text.get_width() / 2) - 42, 5))

    # Help Box
    pygame.draw.rect(screen, BLACK, h1 + s5)
    help_str1 = "How to Play"
    help_str2 = "Press 1-3 to select your character"
    help_str3 = "Press 1-5 to select your opponent"
    help_str4 = "Gameplay:"
    help_str5 = "Press 1-3 to place dice - max 3 dice/column"
    help_str6 = "Bonus: Place two or three of the same dice in a column"
    help_str7 = "Eliminate opponent's dice with same dice in your column"

    help_text1 = help_font1.render(help_str1, True, LIGHT_GREY)
    screen.blit(help_text1, h2)
    help_text2 = help_font2.render(help_str2, True, LIGHT_GREY)
    screen.blit(help_text2, h3)
    help_text3 = help_font2.render(help_str3, True, LIGHT_GREY)
    screen.blit(help_text3, h4)
    help_text4 = help_font2.render(help_str4, True, LIGHT_GREY)
    screen.blit(help_text4, h5)
    help_text5 = help_font2.render(help_str5, True, LIGHT_GREY)
    screen.blit(help_text5, h6)
    help_text6 = help_font2.render(help_str6, True, LIGHT_GREY)
    screen.blit(help_text6, h7)
    help_text7 = help_font2.render(help_str7, True, LIGHT_GREY)
    screen.blit(help_text7, h8)

    # Character Backings
    pygame.draw.rect(screen, BLACK, m1 + s1)
    select_one = menu_font.render('1', True, LIGHT_GREY)
    screen.blit(select_one, ms1)
    pygame.draw.rect(screen, BLACK, m2 + s1)
    select_two = menu_font.render('2', True, LIGHT_GREY)
    screen.blit(select_two, ms2)
    pygame.draw.rect(screen, BLACK, m3 + s1)
    select_three = menu_font.render('3', True, LIGHT_GREY)
    screen.blit(select_three, ms3)
    pygame.draw.rect(screen, BLACK, m4 + s1)
    select_four = menu_font.render('4', True, LIGHT_GREY)
    screen.blit(select_four, ms4)
    pygame.draw.rect(screen, BLACK, m5 + s1)
    select_five = menu_font.render('5', True, LIGHT_GREY)
    screen.blit(select_five, ms5)

    # Character Sprites
    screen.blit(p_sprite1, m1 + s1)
    screen.blit(p_sprite2, m2 + s1)
    screen.blit(p_sprite3, m3 + s1)

    # Flip the display
    pygame.display.flip()

    # ======================
    # User Selects Character
    # ======================

    # Clear Events
    pygame.event.clear()
    # Get the set of keys pressed and check for user input (Loop until valid input from player)
    while True:
        # Wait for Player to Select a Column
        user_input = keystroke()

        if user_input == 0:
            player_sprite = p_sprite1
            break
        elif user_input == 1:
            player_sprite = p_sprite2
            break
        elif user_input == 2:
            player_sprite = p_sprite3
            break
        elif user_input == -1:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        else:
            # Refresh the loop
            pass

    # ==================
    # User Selects Agent
    # ==================

    # Background
    screen.blit(bg, (0, 0))

    # Game Title & Picture
    title_text = menu_font.render('Phantom Dice', True, DARK_GREEN)
    screen.blit(title_text, ((SCREEN_WIDTH / 2) - (title_text.get_width() / 2) + 32, 25))
    screen.blit(title_img, ((SCREEN_WIDTH / 2) - (title_text.get_width() / 2) - 42, 5))

    # Help Box
    pygame.draw.rect(screen, BLACK, h1 + s5)
    help_str1 = "How to Play"
    help_str2 = "Press 1-3 to select your character"
    help_str3 = "Press 1-5 to select your opponent"
    help_str4 = "Gameplay:"
    help_str5 = "Press 1-3 to place dice - max 3 dice/column"
    help_str6 = "Bonus: Place two or three of the same dice in a column"
    help_str7 = "Eliminate opponent's dice with same dice in your column"

    help_text1 = help_font1.render(help_str1, True, LIGHT_GREY)
    screen.blit(help_text1, h2)
    help_text2 = help_font2.render(help_str2, True, LIGHT_GREY)
    screen.blit(help_text2, h3)
    help_text3 = help_font2.render(help_str3, True, LIGHT_GREY)
    screen.blit(help_text3, h4)
    help_text4 = help_font2.render(help_str4, True, LIGHT_GREY)
    screen.blit(help_text4, h5)
    help_text5 = help_font2.render(help_str5, True, LIGHT_GREY)
    screen.blit(help_text5, h6)
    help_text6 = help_font2.render(help_str6, True, LIGHT_GREY)
    screen.blit(help_text6, h7)
    help_text7 = help_font2.render(help_str7, True, LIGHT_GREY)
    screen.blit(help_text7, h8)

    # Character Backings
    pygame.draw.rect(screen, BLACK, m1 + s1)
    select_one = menu_font.render('1', True, LIGHT_GREY)
    screen.blit(select_one, ms1)
    pygame.draw.rect(screen, BLACK, m2 + s1)
    select_two = menu_font.render('2', True, LIGHT_GREY)
    screen.blit(select_two, ms2)
    pygame.draw.rect(screen, BLACK, m3 + s1)
    select_three = menu_font.render('3', True, LIGHT_GREY)
    screen.blit(select_three, ms3)
    pygame.draw.rect(screen, BLACK, m4 + s1)
    select_four = menu_font.render('4', True, LIGHT_GREY)
    screen.blit(select_four, ms4)
    pygame.draw.rect(screen, BLACK, m5 + s1)
    select_five = menu_font.render('5', True, LIGHT_GREY)
    screen.blit(select_five, ms5)

    # Agent Sprites
    screen.blit(a_sprite1, m1 + s1)
    screen.blit(a_sprite2, m2 + s1)
    screen.blit(a_sprite3, m3 + s1)
    screen.blit(a_sprite4, m4 + s1)
    screen.blit(a_sprite5, m5 + s1)

    # Flip the display
    pygame.display.flip()

    # Clear Events
    pygame.event.clear()
    # Get the set of keys pressed and check for user input (Loop until valid input from player)
    while True:
        # Wait for Player to Select a Column
        user_input = keystroke()

        if user_input == 0:
            agent_sprite = a_sprite1
            selected_agent = RandomAgent(agent=1)
            break
        elif user_input == 1:
            agent_sprite = a_sprite2
            selected_agent = GreedyAgent(agent=1)
            break
        elif user_input == 2:
            agent_sprite = a_sprite3
            selected_agent = MonteCarloAgent(agent=1, trials=50)
            break
        elif user_input == 3:
            agent_sprite = a_sprite4
            selected_agent = MinimaxAgent(eval_agent=1, max_depth=3)
            break
        elif user_input == 4:
            agent_sprite = a_sprite5
            selected_agent = MonteCarloAgent(agent=1, trials=250)
            break
        elif user_input == -1:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        else:
            # Refresh the loop
            pass
    return player_sprite, agent_sprite, selected_agent


# Clear Events
pygame.event.clear()

# Menu
player_sprite, agent_sprite, selected_agent = menu()

# Main Game
running = True
while running:
    # ===============
    # Draw the Screen
    # ===============

    # Background
    screen.blit(bg, (0, 0))

    # Dice Boxes
    pygame.draw.rect(screen, BLACK, a1 + s1)
    pygame.draw.rect(screen, BLACK, a2 + s1)
    pygame.draw.rect(screen, BLACK, a3 + s1)
    pygame.draw.rect(screen, BLACK, a4 + s1)
    pygame.draw.rect(screen, BLACK, a5 + s1)
    pygame.draw.rect(screen, BLACK, a6 + s1)
    pygame.draw.rect(screen, BLACK, a7 + s1)
    pygame.draw.rect(screen, BLACK, a8 + s1)
    pygame.draw.rect(screen, BLACK, a9 + s1)

    pygame.draw.rect(screen, BLACK, b1 + s1)
    pygame.draw.rect(screen, BLACK, b2 + s1)
    pygame.draw.rect(screen, BLACK, b3 + s1)
    pygame.draw.rect(screen, BLACK, b4 + s1)
    pygame.draw.rect(screen, BLACK, b5 + s1)
    pygame.draw.rect(screen, BLACK, b6 + s1)
    pygame.draw.rect(screen, BLACK, b7 + s1)
    pygame.draw.rect(screen, BLACK, b8 + s1)
    pygame.draw.rect(screen, BLACK, b9 + s1)

    # Roll Boxes
    pygame.draw.rect(screen, BLACK, c1 + s2)
    pygame.draw.rect(screen, BLACK, c2 + s2)

    # Character Sprites
    screen.blit(player_sprite, sp0)
    screen.blit(agent_sprite, sp1)

    # Display Current Board State
    display_mapper(names=new_game.player_names, scores=new_game.player_score, board=new_game.board_state)

    # Flip the display
    pygame.display.flip()

    # ===================
    # Run the Actual Game
    # ===================

    # Roll Die
    roll = new_game.roll_dice()
    # Display Die
    roll_mapper(_roll=roll, _turn=turn)
    time.sleep(1)
    pygame.display.flip()
    # Player's Turn
    if not turn:
        # Clear Events
        pygame.event.clear()
        # Get the set of keys pressed and check for user input (Loop until valid input from player)
        while True:
            # Wait for Player to Select a Column
            user_input = keystroke()
            # Check if Escape was Hit (-1 return)
            if user_input == -1:
                running = False
                break
            # Try to Update the Board
            else:
                if new_game.update_board(player=int(turn), column=user_input, roll=roll):
                    break
    # Agent's Turn
    else:
        # Get an action from the agent
        action = selected_agent.take_action(board_state=new_game.board_state, roll=roll)
        new_game.update_board(player=int(turn), column=action, roll=roll)
        # Brief pause
        time.sleep(random.uniform(.5, 1.5))
    # Exit Check (break game loop if ESC was pressed)
    if not running:
        break
    # Calculate Score
    new_game.update_score()
    # Endgame Check
    if new_game.endgame_check():
        # Display Win Banner
        # Background Box
        win_box = pygame.draw.rect(screen, BLACK, w1 + s3)
        # Win Text
        # Print the Winner of the Game
        winner = np.argmax(new_game.player_score)
        win_text = f"***{new_game.player_names[winner]} has won with a score of {new_game.player_score[winner]}***"
        img = font.render(win_text, True, LIGHT_GREY)
        # Get coordinates to center the text in the win box
        text_x, text_y = center_text(img, win_box)
        screen.blit(img, (text_x, text_y))
        pygame.display.flip()
        # Pause then Exit
        time.sleep(5)
        break
    # Update Display
    display_mapper(names=new_game.player_names, scores=new_game.player_score, board=new_game.board_state)
    pygame.display.flip()
    # Switch Turns
    turn = not turn

# Done! Time to quit.
pygame.quit()
