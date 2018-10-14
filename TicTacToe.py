import string
import random


def display_board(board):
    # very simple board display - just the arrays, just to be functional, not pretty
    [print(board[x:x+dimension]) for x in range(1, len(board), dimension)]


def check_player_input(board, player):
    # :returns False, if player picket an invalid marker
    return player not in string.digits


def player_input(board):
    # Let users pick their board markers
    # :returns player markers as tuple

    print(f"Please pick your markers (letters, not numbers)")

    p1 = input("Player 1: ")
    while not check_player_input(board, p1):
        p1 = input("Player 1: ")

    p2 = input("Player 2: ")
    while not check_player_input(board, p2):
        p2 = input("Player 2: ")

    while p2 == p1:
        p2 = input("NO, pick a DIFFERENT marker.")

    return p1.upper(), p2.upper()


def place_marker(board, marker, position):
    # Assign desired position to the board
    board[position] = marker


def win_check(board, mark):
    # :returns True if a game is won

    max_val = len(board) # happens to be the same as numbers on board, since first element is an aligmnent element

    # vertical
    for x in range(1, dimension+1):
        if board[x:max_val:dimension] == [mark]*dimension:
            print(f'WIN! vertical(col {x})')
            return True

    # horizontal
    for c in range(1, max_val, dimension):
        if board[c:c+dimension] == [mark]*dimension:
            print(f'WIN! horizontal(row {int((c+dimension)/dimension)})')
            return True

    # diagonal (left => right)
    if board[1:max_val:dimension+1] == [mark]*dimension:
        print(f'WIN! diagonal left=>right!')
        return True

    # diagonal (right => left)
    if board[dimension:max_val-(dimension-1):dimension-1] == [mark]*dimension:
        print(f'WIN! diagonal right=>left!')
        return True

    return False


def choose_first():
    # random pick the first player to start the game
    # :returns the player to start
    if random.randint(1, 2) == 1:
        return player1
    else:
        return player2


def space_check(board, position):
    # returns True if desired position can be occupied
    return position in range(1,len(board)) and board[position] == str(position)


def full_board_check(board):
    # :returns True if the board is full
    return [x for x in board if x in string.digits] == []


def player_choice(board):
    # ask current player for the next desired position, which will be checked for validity
    pos = 0
    while pos == 0:
        pos = int(input(f'{players_turn}, select valid position: '))
        if not space_check(board, pos):
            # Only allow positions that are available
            pos = 0
    return pos


def replay():
    # ask players to start a new game
    answer = ''
    while answer not in ['yes','y','no','n']:
        answer = input("Do you want to play again? (yes/no): ")

    return answer == 'yes' or answer == 'y'


if __name__ == '__main__':

    print('Welcome to Tic Tac Toe!')

    while True:

        # --- Set up the game

        # Choose the dimension of the board. The larger the board the longer the game
        dimension = int(input('How big should the board be? Give a number for a dimension, e.g 3 for 3x3: '))

        # init the board and display
        game_board = [' ']*((dimension**2)+1)
        game_board[0] = '#'  # adjust the index to fit the cell numbers

        # set indices as cell contents
        for elem in range(1, len(game_board)):
            game_board[elem] = str(elem)

        display_board(game_board)

        # Let players pick their markers
        player1, player2 = player_input(game_board)
        print(f'OK. [Player 1:"{player1.upper()}"], [Player 2:"{player2.upper()}"]. Lets start.')

        # Randomly choose which player goes first
        players_turn = choose_first()

        # --- Game is on
        game_on = True

        # Let players take turns while the game is on
        while game_on:

            # Ask current player for play position
            play_pos = player_choice(game_board)

            # make the turn and display result
            place_marker(game_board, players_turn, play_pos)
            display_board(game_board)

            # current player won - game over
            if win_check(game_board, players_turn):
                print(f'{players_turn} won!')
                break

            # board is full - game over
            if full_board_check(game_board):
                print('No more turns possible. Nobody won.')
                break

            # let the other player do his turn
            if players_turn == player1:
                players_turn = player2
            else:
                players_turn = player1

            print()

        if not replay():
            # we are done, no more games
            break

        print('\n'*100)

    print('--- THE END ---')