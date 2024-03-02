from typing import List, Tuple, Iterable, Optional

import boggle_board_randomizer


class Board:
    """This is an object of boggle board that contains letters in 2D
    list. You can get an information about every coordinate in it and randomize
    a new board"""

    def __init__(self) -> None:
        self.__board = boggle_board_randomizer.randomize_board()

    def cell_set(self) -> set[tuple]:
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        set_of_coordinates = {(i, j) for i in range(len(self.__board))
                              for j in range(len(self.__board[i]))}
        return set_of_coordinates

    def get_letter(self, x: int, y: int) -> Optional[str]:
        """This function return the letter that locate in given coordinate"""
        if (x, y) in self.cell_set():
            return self.__board[x][y]

    def new_board(self) -> None:
        """This function make a new board"""
        new_board = boggle_board_randomizer.randomize_board()
        self.__board = new_board

    def get_board(self) -> list[list[str]]:
        return self.__board

    def get_size(self) -> int:
        return len(self.__board)
