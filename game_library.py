import numpy as np


class PhantomDice:
    def __init__(self):
        self.board_state = np.zeros(shape=(2, 3, 3), dtype=np.int8)
        self.turn_count = 0
        self.player_turn = 0
        self.player_score = np.zeros(shape=(2,), dtype=np.int8)
        self.player_names = ['Human', 'BOT']
        self.game_ended = False
        self.winner = None

    # ========================
    # Real-Time Game Functions
    # ========================

    # Displays the Board State in the Terminal
    def print_board(self):
        print(f"Turn {self.turn_count}")
        print("=========")
        if self.player_turn == 1:
            print('|', ' '.join(map(str, self.board_state[1, 0, :])), '| *', self.player_names[1], self.player_score[1])
        else:
            print('|', ' '.join(map(str, self.board_state[1, 0, :])), '| ', self.player_names[1], self.player_score[1])
        print('|', ' '.join(map(str, self.board_state[1, 1, :])), '|')
        print('|', ' '.join(map(str, self.board_state[1, 2, :])), '|')
        print("=========")
        if self.player_turn == 0:
            print('|', ' '.join(map(str, self.board_state[0, 0, :])), '| *', self.player_names[0], self.player_score[0])
        else:
            print('|', ' '.join(map(str, self.board_state[0, 0, :])), '| ', self.player_names[0], self.player_score[0])
        print('|', ' '.join(map(str, self.board_state[0, 1, :])), '|')
        print('|', ' '.join(map(str, self.board_state[0, 2, :])), '|')
        print("=========")

    # Determines if the Game has ended
    def endgame_check(self):
        for j in range(self.board_state.shape[1]):
            for k in range(self.board_state.shape[2]):
                if self.board_state[self.player_turn, j, k] == 0:
                    # Update Tracker to Reflect Next Players Turn
                    self.player_turn = int(not bool(self.player_turn))
                    self.game_ended = False
                    return False
        self.game_ended = True
        # Print the Winner of the Game (-1 for tie)
        if self.player_score[0] == self.player_score[1]:
            self.winner = -1
        else:
            self.winner = np.argmax(self.player_score)
        return True

    # Calculates the Score for Each Player
    def update_score(self):
        # Calc score for both players
        for player in range(self.board_state.shape[0]):
            # Reset Score Since it Will be Fully Recalculated
            self.player_score[player] = 0
            # Calculate Score for Each Column
            for col in range(self.board_state.shape[1]):
                single_list, double_list, triple_list = ([] for i in range(3))
                for row in range(self.board_state.shape[2]):
                    value = self.board_state[player, row, col]
                    if value in single_list:
                        double_list.append(value)
                        single_list.remove(value)
                    elif value in double_list:
                        triple_list.append(value)
                        double_list.remove(value)
                    else:
                        single_list.append(value)
                # Calculate Score Using Single, Double, Triple Lists
                self.player_score[player] += np.sum(single_list) + (np.sum(double_list) * 4) + (np.sum(triple_list) * 9)

    # Updates Board State with Move
    def update_board(self, player, column, roll):
        # Player Picks Column and the Die is added to the First Available Spot
        # Determine Row for the Die and then Place the Die (Lowest Row First)
        for row in range(self.board_state.shape[2]):
            if self.board_state[player, -(row+1), column] == 0:
                # Place the Die for Player
                self.board_state[player, -(row+1), column] = roll
                # Remove Opponents Dice if they are the Same
                self.dice_removal(column=column, roll=roll, player=int(not bool(player)))
                # Update the Move Counter and Return that the Move Was Valid
                self.turn_count += 1
                return True
        # Return that the Move was Invalid (Column was Full)
        return False

    # Removes Matching Dice from Opponent
    def dice_removal(self, column, roll, player):
        # Keep Track of Dice Remaining
        remaining_dice = list()
        removal = False
        for row in range(self.board_state.shape[2]):
            if self.board_state[player, row, column] == roll:
                # Remove Die From Opponent
                self.board_state[player, row, column] = 0
                removal = True
            else:
                # Add to Tracking List
                remaining_dice.append(self.board_state[player, row, column])
        # Re-Arrange Dice
        if removal:
            for i in range(self.board_state.shape[2]):
                try:
                    self.board_state[player, -(i+1), column] = remaining_dice.pop()
                except IndexError:
                    self.board_state[player, -(i+1), column] = 0

    # Rolls a random Die 1-6
    def roll_dice(self):
        return np.random.randint(6) + 1
