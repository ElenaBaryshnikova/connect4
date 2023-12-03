from __future__ import annotations

import numpy as np

from settings import Settings


class Connect4:
    def __init__(self):
        self.board: list = [
            ['*' for i in range(Settings.COL_COUNT)] for j in range(Settings.ROW_COUNT)
        ]
        self.player: str = Settings.PLAYER1_POINT

    def print_board(self) -> None:
        print('\n'.join(' '.join(map(str, sl)) for sl in self.board))

    @staticmethod
    def is_column_correct(column_number: int) -> bool:
        if column_number > Settings.COL_COUNT:
            print('Column number should be less when Settings.COL_COUNT')
            return False
        elif column_number <= 0:
            print('Column number should be positive')
            return False
        # todo column is full
        return True

    def select_column(self) -> int:
        valid = False
        while not valid:
            try:
                column_number = int(
                    input(f'Player {self.player} choose column number '),
                )
                valid = Connect4.is_column_correct(column_number)
            except:
                print('Value is not a number')
        return int(column_number)

    def drop(self, column_number: int) -> bool:
        try:
            row_num = Settings.ROW_COUNT - 1
            while self.board[row_num][column_number - 1] != '*':
                row_num -= 1
            self.board[row_num][column_number - 1] = self.player
            return True
        except:
            print('Wrong point, choose another')

    @staticmethod
    def check_if_winner() -> bool:
        return False

    def change_player(self):
        if self.player == Settings.PLAYER1_POINT:
            self.player = Settings.PLAYER2_POINT
        else:
            self.player = Settings.PLAYER1_POINT

    @staticmethod
    def find_winner_in_array(nums: np.ndarray, k: int) -> str | bool:
        for i in range(len(nums)-k+1):
            if len(set(nums[i:(k+i)])) == 1:
                winner = nums[i]
                if winner != '*':
                    return winner
        return False

    def find_winner(self):
        array_board = np.array(self.board)
        for row in self.board:
            if winner := Connect4.find_winner_in_array(row, Settings.POINTS_IN_A_ROW):
                return winner
        for column in array_board.transpose():
            if winner := Connect4.find_winner_in_array(column, Settings.POINTS_IN_A_ROW):
                return winner
        diagonals_1 = [
            np.diag(array_board, k=i)
            for i in range(-Settings.ROW_COUNT + 1, Settings.ROW_COUNT)
        ]
        good_dia_1 = [
            i for i in diagonals_1 if len(
                i,
            ) >= Settings.POINTS_IN_A_ROW
        ]

        array_board = np.flipud(array_board)
        diagonals_2 = [
            np.diag(array_board, k=i)
            for i in range(-Settings.ROW_COUNT + 1, Settings.ROW_COUNT)
        ]
        good_dia_2 = [
            i for i in diagonals_2 if len(
                i,
            ) >= Settings.POINTS_IN_A_ROW
        ]
        good_dia = good_dia_1 + good_dia_2
        for diag in good_dia:
            if winner := Connect4.find_winner_in_array(diag, Settings.POINTS_IN_A_ROW):
                return winner
        return False


if __name__ == '__main__':
    connect4 = Connect4()
    connect4.print_board()
    while not connect4.find_winner():
        chosen_column = connect4.select_column()
        connect4.drop(chosen_column)
        connect4.print_board()
        connect4.change_player()
    print(f'Congratulations player {connect4.find_winner()}, you win')
