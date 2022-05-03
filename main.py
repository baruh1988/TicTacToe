import math
import random
import time


#############################################################################
class Game():
    def __init__(self):
        self.board = self.generate_board()
        self.winner = None

    def generate_board(self):
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i * 3: (i + 1) * 3] for i in range(3)]:
            print('|' + '|'.join(row) + '|')

    def print_numbered_board(self):
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('|' + '|'.join(row) + '|')

    def check_winner(self, cell, letter):
        i = math.floor(cell / 3)
        row = self.board[i * 3: (i + 1) * 3]
        if row.count(letter) == 3:
            return True
        j = cell % 3
        col = [self.board[j + i * 3] for i in range(3)]
        if col.count(letter) == 3:
            return True
        if cell % 2 == 0:
            diagonal = [self.board[i] for i in [0, 4, 8]]
            if diagonal.count(letter) == 3:
                return True
            diagonal = [self.board[i] for i in [2, 4, 6]]
            if diagonal.count(letter) == 3:
                return True
        return False

    def make_move(self, cell, letter):
        if self.board[cell] == ' ':
            self.board[cell] = letter
            if self.check_winner(cell, letter):
                self.winner = letter
            return True
        return False

    def empty_cells_count(self):
        return self.board.count(' ')

    def has_empty_cells(self):
        return ' ' in self.board

    def available_cells(self):
        # return [i for i in range(9) if self.board[i] == ' ']
        return [i for i, x in enumerate(self.board) if x == ' ']


#############################################################################
class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


#############################################################################
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_cell = False
        cell = None
        while not valid_cell:
            try:
                cell = int(input(self.letter + ' turn. Input square(0 - 8): '))
                if cell not in game.available_cells():
                    raise ValueError
                valid_cell = True
            except ValueError:
                print('Invalid input. Try again!')
        return cell


#############################################################################
class AiPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_cells()) == 9:
            cell = random.choice(game.available_cells())
        else:
            cell = self.minimax(game, self.letter)['cell']
        return cell

    def minimax(self, state, player):
        maximizing_player = self.letter
        other_player = 'O' if player == 'X' else 'X'
        if state.winner == other_player:
            return {'cell': None, 'score': 1 * (state.empty_cells_count() + 1)} if other_player == maximizing_player else {
                'cell': None, 'score': -1 * (state.empty_cells_count() + 1)}
        elif not state.has_empty_cells():
            return {'cell': None, 'score': 0}
        best = {'cell': None, 'score': -math.inf} if player == maximizing_player else {'cell': None, 'score': math.inf}
        for cell in state.available_cells():
            state.make_move(cell, player)
            sim = self.minimax(state, other_player)
            state.board[cell] = ' '
            state.winner = None
            sim['cell'] = cell
            if player == maximizing_player:
                best = sim if best['score'] < sim['score'] else best
            else:
                best = sim if best['score'] > sim['score'] else best
        return best


#############################################################################
def play(game, x_player, o_player):
    game.print_numbered_board()
    letter = 'X'
    while game.has_empty_cells():
        if letter == 'O':
            cell = o_player.get_move(game)
        else:
            cell = x_player.get_move(game)
        if game.make_move(cell, letter):
            print(letter + ' makes a move to {}'.format(cell))
            game.print_board()
            print()
            if game.winner:
                print(letter + ' wins')
                return letter
            letter = 'O' if letter == 'X' else 'X'
        time.sleep(3)
    print('Game ends in a tie')


if __name__ == '__main__':
    while True:
        try:
            choice = input('Choose x/o: ')
            if choice == 'x':
                x_player = HumanPlayer('X')
                o_player = AiPlayer('O')
            elif choice == 'o':
                x_player = AiPlayer('X')
                o_player = HumanPlayer('O')
            else:
                raise ValueError
            game = Game()
            play(game, x_player, o_player)
            choice = input('Play again? y/n: ')
            if choice == 'n':
                break
            elif choice != 'y' and choice != 'n':
                raise ValueError
        except ValueError:
            print('Invalid input! Try again')
