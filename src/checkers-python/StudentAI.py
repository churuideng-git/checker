from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        best_move = moves[0][0]
        best_util = self.get_util(move)

        for i in range(3):
            index = randint(0,len(moves)-1)
            inner_index =  randint(0,len(moves[index])-1)
            move = moves[index][inner_index]
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
        util: int = 0
        util += self.util_num_captures(move)
        util += self.util_back_row(move)
        util += self.util_king(move)
        util += self.util_towards_center(move)
        util += self.util_enemy_capture(move)
        return util

    def util_num_captures(self, move: Move) -> int:
        l: int = len(move)
        return l * 3 if l > 2 else 0

    def util_back_row(self, move: Move) -> int:
        if len(move) == 0:
            return 0
        return -5 if move[0][1] == 0 else 0

    def util_king(self, move: Move) -> int:
        if len(move) == 0:
            return 0
        return 5 if move[-1][1] == self.row - 1 else 0

    def util_towards_center(self, move: Move) -> int:
        if len(move) == 0:
            return 0
        final_x: int = move[-1][0]
        if 0 == final_x or final_x == self.col - 1:
            return -2 * self.col
        return 0
        # center: int = (self.col - 1) / 2
        # distance_from_center: int = abs(center - final_x)
        # return -5 * distance_from_center

    def util_enemy_capture(self, move: Move):
        if len(move) == 0:
            return 0
        pos_x = move[-1][0]
        pos_y = move[-1][1]

        if self.board.is_in_board(pos_x-1, pos_y+1):
            left = self.board.board[pos_x-1][pos_y+1]
            if left.get_color().lower() == "w":
                return -100
        if self.board.is_in_board(pos_x+1, pos_y+1):
            right = self.board.board[pos_x+1][pos_y+1]
            if right.get_color().lower() == "w":
                return -100
        return 0