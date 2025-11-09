from random import randint
from BoardClasses import Move
from BoardClasses import Board

# constants
BLACK = 1
WHITE = 2

OPPONENT = {BLACK: WHITE, WHITE: BLACK}
PIECE_CHAR = {BLACK: "B", WHITE: "W"}

FORWARD_DIR = {BLACK: 1, WHITE: -1}

BACK_ROW_LEAVE_PENALTY_PER_ROW = 2
KING_PROMOTION_REWARD_PER_ROW = 1
CENTER_DISTANCE_WEIGHT = 1
SUPPORT_BONUS = 5
ENEMY_AHEAD_THREAT_PENALTY = 10

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI:

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = OPPONENT
        self.color = WHITE
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = BLACK
        moves = self.board.get_all_possible_moves(self.color)

        best_move = moves[0][0]
        best_util = self.get_util(best_move)

        # pick 3
        # for i in range(3):
        #     index = randint(0,len(moves)-1)
        #     inner_index =  randint(0,len(moves[index])-1)
        #     move = moves[index][inner_index]
        #     if move == best_move:
        #         continue
        #     util = self.get_util(move)
        #     if util > best_util:
        #         best_move = move
        #         best_util = util

        # analyze all
        for piece in moves:
            for move in piece:
                if move == best_move:
                    continue
                util = self.get_util(move)
                if util > best_util:
                    best_move = move
                    best_util = util

        self.board.make_move(best_move,self.color)
        return best_move

    class Node:
        def __init__(self):
            self.w = 0
            self.s = 0

    def get_util(self, move: Move) -> int:
        if len(move) == 0:
            return 0

        util: int = 0
        util += self.util_back_row(move)
        util += self.util_king(move)
        util += self.util_towards_center(move)
        util += self.util_enemy_capture(move)
        return util

    def util_back_row(self, move: Move) -> int:
        back_row = 0 if self.color == BLACK else self.row - 1
        start_row = move[0][0]
        return -BACK_ROW_LEAVE_PENALTY_PER_ROW * self.row if start_row == back_row else 0

    def util_king(self, move: Move) -> int:
        king_row = self.row - 1 if self.color == BLACK else 0
        final_row: int = move[-1][0]
        final_col: int = move[-1][1]
        return KING_PROMOTION_REWARD_PER_ROW * self.row if final_row == king_row and not self.board.board[final_row][final_col].is_king else 0

    def util_towards_center(self, move: Move) -> int:
        final_col: int = move[-1][1]
        center: int = (self.col - 1) / 2
        distance_from_center: int = center - final_col
        return -CENTER_DISTANCE_WEIGHT * distance_from_center * distance_from_center

    def util_enemy_capture(self, move: Move):
        own_color = PIECE_CHAR[self.color]
        opp_color = PIECE_CHAR[self.opponent[self.color]]

        row = move[-1][0]
        col = move[-1][1]
        front = row + FORWARD_DIR[self.color]

        left = self.board.board[front][col-1].get_color() if self.board.is_in_board(front, col-1) else ""
        right = self.board.board[front][col+1].get_color() if self.board.is_in_board(front, col+1) else ""

        util = 0
        if left == own_color or right == own_color:
            util += SUPPORT_BONUS
        if left == opp_color or right == opp_color:
            util += -ENEMY_AHEAD_THREAT_PENALTY
        return util
