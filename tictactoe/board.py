from enum import IntEnum


class Player(IntEnum):
    HUMAN = -1
    UNKNOWN = 0
    AI = 1


class Cell:
    def __init__(self, y, x, player):
        self.x = x
        self.y = y
        self.player = player

    def __str__(self):
        return 'x' if self.player.value == Player.HUMAN.value else (
            'o' if self.player.value == Player.AI.value else ' '
        )

    def __repr__(self):
        return str(self)


class Line:
    def __init__(self, cells):
        self.cells = cells

    @property
    def winner(self):
        players = list({c.player for c in self.cells})

        if len(players) != 1 or players[0].value == Player.UNKNOWN.value:
            return Player.UNKNOWN

        return players[0]

    def __str__(self):
        return '#' + '#'.join(str(c) for c in self.cells) + '#'

    def __repr__(self):
        return str(self)


class Move:
    def __init__(self, y, x, player):
        self.y = y
        self.x = x

        assert player.value != Player.UNKNOWN.value, "impossible move"

        self.player = player

    def __str__(self):
        return f"({self.y}, {self.x}) [{self.player}]"


class Board:
    def __init__(self, board=None, move=None):
        self.data = [
            [
                Cell(y, x, Player.UNKNOWN) if board is None else board[y, x]
                for x in range(3)
            ]
            for y in range(3)
        ]

        if move is not None:
            assert self[move.y, move.x].player.value == Player.UNKNOWN.value, "Impossible move"
            self[move.y, move.x] = Cell(move.y, move.x, move.player)

    def __getitem__(self, pos):
        y, x = pos
        return self.data[y][x]

    def __setitem__(self, key, value):
        y, x = key
        self.data[y][x] = value

    @property
    def horizontal_lines(self):
        return [
            Line([self[x, y] for y in range(3)])
            for x in range(3)
        ]

    @property
    def vertical_lines(self):
        return [
            Line([self[x, y] for x in range(3)])
            for y in range(3)
        ]

    @property
    def diagonal_lines(self):
        return [
            Line([self[0, 0], self[1, 1], self[2, 2]]),
            Line([self[0, 2], self[1, 1], self[2, 0]])
        ]

    @property
    def lines(self):
        return [*self.horizontal_lines, *self.vertical_lines, *self.diagonal_lines]

    def possible_moves(self, player):
        moves = []

        for y in range(3):
            for x in range(3):
                if self[y, x].player == Player.UNKNOWN:
                    moves.append(Move(x=x, y=y, player=player))

        return moves

    @property
    def winner(self):
        winners = [line.winner for line in self.lines]
        winners = [w for w in winners if w.value != Player.UNKNOWN.value]

        return winners[0] if len(winners) > 0 else Player.UNKNOWN

    def __str__(self):
        divider = '#' * 7 + '\n'

        result = divider

        for line in self.horizontal_lines:
            result += str(line) + '\n' + divider

        return result

    def __repr__(self):
        return str(self)
