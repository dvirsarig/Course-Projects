'''
EX - 12
By Levy Ofek and Dvir Sarig
'''

import Board

DIRECTIONS = {(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)}


class Game:
    """The class game have his board and list of words, it has current word and path
    and keep a list of solutions that found. The game have updates methods, delete, refresh
    and making a restart to all the information."""

    def __init__(self, board: Board, words: set[str]) -> None:
        self.__board = board
        self.__words = words
        self.__score = 0
        self.__solutions = []
        self.__current_word = ""
        self.__current_path = []
        self.__current_keyboard = []

    def update_score(self, n: int) -> None:
        """Update the score of the game with path with size n"""
        self.__score += n ** 2

    def update_solutions(self, word: str) -> None:
        """Update the list of all solutions were found"""
        self.__solutions.append(word)

    def update_word(self, row: int, col: int) -> None:
        """Update the currect word which pressed"""
        letter = self.__board.get_letter(row, col)
        if letter is None:
            raise ValueError("Coordinate not in board")
        self.__current_keyboard.append(letter)
        self.__current_word += letter
        self.__current_path.append((row, col))

    def delete_letter(self) -> bool:
        """Try delete the last letter which pressed and return if action compleated"""
        if len(self.__current_word) == 0:
            return False
        if len(self.__current_path) == 0:
            return False
        letter = self.__current_keyboard.pop()
        self.__current_word = self.__current_word[:-len(letter)]
        self.__current_path.pop()
        return True

    def check_if_solution(self) -> bool:
        """This function checks if the current word which pressed is in the dictionary,
        if it is - we are adding the score to the user, the word to the solutions and restart
        current word"""
        if len(self.__current_word) <= 1:
            return False
        if self.__current_word in self.__words and self.__current_word not in self.__solutions:
            self.__solutions.append(self.__current_word)
            path_length = len(self.__current_path)
            self.update_score(path_length)
            return True
        return False

    def refresh(self) -> None:
        """This function clear the letters were clicked, so the user
        will be able to begin a new path"""
        self.__current_word = ""
        self.__current_path = []

    def new_game(self) -> None:
        """This function restart all the information and get a new board"""
        self.__board.new_board()
        self.__score = 0
        self.__solutions = []
        self.__current_word = ""
        self.__current_path = []

    def check_valid_next_step(self, row: int, col: int) -> bool:
        """This function check if the next coordinate that the user press is valid
        in the game rules"""
        if (row, col) in self.__current_path:
            return False
        if len(self.__current_path) >= 1:
            pre_coordinate = self.__current_path[-1]
            delta = (pre_coordinate[0] - row, pre_coordinate[1] - col)
            if delta not in DIRECTIONS:
                return False

        return True

    def get_game_board(self) -> Board:
        return self.__board.get_board()

    def get_value(self, x, y) -> str:
        return self.__board.get_letter(x, y)

    def get_board_size(self) -> int:
        return self.__board.get_size()

    def get_currect_word(self) -> str:
        return str(self.__current_word)

    def get_path_lentgh(self) -> int:
        return len(self.__current_path)

    def get_score(self) -> int:
        return self.__score

    def get_valid_words(self) -> set[str]:
        return self.__words

    def get_current_keyboard(self) -> str:
        return self.__current_keyboard[-1]

    def update_current_keyboard(self, s: str) -> None:
        self.__current_keyboard.append(s)
