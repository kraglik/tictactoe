import math

from tictactoe.board import Player, Board, Move


def game_loop():

    while True:
        result = '?'

        while result not in ('y', 'n'):
            result = input('Start new game? (y/n)\n> ')

        if result == 'n':
            print('bye!')
            break

        game()


def game():
    current = Player.AI

    board = Board()

    winner = Player.UNKNOWN

    while winner == Player.UNKNOWN:

        if current == Player.HUMAN:
            board = human_turn(board)
            current = Player.AI

        else:
            board = ai_turn(board)
            current = Player.HUMAN

        print('-' * 20)
        print(board)

        winner = board.winner

        if not board.possible_moves(Player.AI) and winner == Player.UNKNOWN:
            winner = None

    if winner == Player.HUMAN:
        print('You won!')
    elif winner == Player.AI:
        print('Yoy lose!')
    else:
        print('It\'s a draw!')


def read_move():
    x, y = None, None

    while x is None and y is None:

        result = input('your move (line column)\n> ')
        result = result.split(' ')

        if len(result) != 2:
            print('wrong number of coordinates!')
            continue

        try:
            x = int(result[0])
            y = int(result[1])

        except Exception:
            print('wrong coordinates format!')
            continue

        if x < 1 or y < 1 or x > 3 or y > 3:
            print('coordinates must be in range [1-3]!')
            x, y = None, None
            continue

        else:
            break

    return x - 1, y - 1


def human_turn(board):
    new_board = None

    while True:
        try:
            y, x = read_move()

            new_board = Board(board, move=Move(x=x, y=y, player=Player.HUMAN))
            break
        except Exception:
            print('impossible move!')
            continue

    return new_board


def toggle_player(player):
    return Player.AI if player == Player.HUMAN else Player.HUMAN


def tree_search(board, player):
    winner = board.winner

    if winner == Player.HUMAN:
        return -1, 1
    elif winner == Player.AI:
        return 1, 1

    wins = 0
    total = 0

    possible_moves = board.possible_moves(toggle_player(player))

    if not possible_moves:
        return board.winner.value, 1

    for move in possible_moves:
        w, t = tree_search(Board(board, move), toggle_player(player))

        wins += w
        total += t

    return wins, total


def ai_turn(board):

    weighted_moves = []

    for move in board.possible_moves(Player.AI):
        w, t = tree_search(Board(board, move), Player.AI)

        weighted_moves.append((move, w / t))

    if len(weighted_moves) == 0:
        return

    best_move, best_weight = weighted_moves[0]

    for move, weight in weighted_moves:
        if weight > best_weight:
            best_move = move
            best_weight = weight

    return Board(board=board, move=best_move)
