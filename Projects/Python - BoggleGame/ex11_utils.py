'''
EX - 12
By Levy Ofek and Dvir Sarig
'''

from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]
DIRECTIONS = {(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)}


def coordinate_outside_of_board(row: int, col: int, board: Board) -> bool:
    '''Return if row, col not in board borders'''
    if (row < 0) or (row >= len(board)):
        return True
    if (col < 0) or (col >= len(board[0])):
        return True
    return False


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    '''Return if the path in board is valid'''
    if len(path) == 0:
        return None
    visited_posions = set()

    prev = path[0]
    if coordinate_outside_of_board(prev[0], prev[1], board):
        return None
    visited_posions.add(prev)

    word = board[prev[0]][prev[1]]
    for i in range(1, len(path)):
        coordinate = path[i]

        if coordinate_outside_of_board(coordinate[0], coordinate[1], board):
            return None
        if coordinate in visited_posions:
            return None
        delta = (coordinate[0] - prev[0], coordinate[1] - prev[1])  # Calcalaute the change in position between points
        if delta not in DIRECTIONS:  # Check if the chnge in position is legal
            return None

        word += board[coordinate[0]][coordinate[1]]
        prev = coordinate
        visited_posions.add(coordinate)

    if word not in words:
        return None
    return word


def parts_of_string(s):
    '''Return the part of the string like this if s = 'DOG' : {'DOG', 'DO', 'D'}'''
    parts = set()
    for j in range(1, len(s) + 1):
        parts.add(s[0:j])
    return parts


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    '''Return a list that contains all the valid path at n size in board'''
    # Get all the parts of all words in one set
    words = set(words)
    partial_words = set()
    for word in words:
        for part in parts_of_string(word):
            partial_words.add(part)

    # A list of all the valid paths in board
    moves_list = []

    # Run for any starting point in board
    for start_row in range(len(board)):
        for start_col in range(len(board[0])):
            path = [(start_row, start_col)]  # Add the first cell to the path
            path_set = {(start_row, start_col)}  # Use this set to speed up the code
            # For any starting point add all paths
            _find_length_n_paths(n - 1, board, path, path_set, start_row, start_col, partial_words, moves_list, words,
                                 '')

    return moves_list


def _find_length_n_paths(n: int, board: Board, path: Path, path_set: set[Tuple[int, int]], row: int, col: int,
                         partial_words: set[str],
                         moves_list: List[Path], words: set[str], word: str) -> None:
    '''An helper function that insert to moves_list all the valid path in starting location'''
    if coordinate_outside_of_board(row, col, board):
        return
    word += board[row][col]  # update word
    if n == 0:  # if we finish the path
        if word in words:  # if final word in valid words
            moves_list.append(path.copy())  # add final path to moves_list
        return
    if word not in partial_words:  # if word isn't possible to complete finish
        return

    n -= 1  # counter
    for direction in DIRECTIONS:  # check for any direction
        # update coordinates
        new_row = row + direction[0]
        new_col = col + direction[1]
        coordinate = (new_row, new_col)

        # Thw path can't repeat itself
        if coordinate not in path_set:
            path.append(coordinate)
            path_set.add(coordinate)

            # Move in direction
            _find_length_n_paths(n, board, path, path_set, new_row, new_col, partial_words, moves_list, words,
                                 word)

            # reset for next direction
            path.pop()
            path_set.remove(coordinate)


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    '''Return a list that contains all the valid path that contains
    words at n size in board'''
    # Get all the parts of all words in one set
    words = words
    partial_words = set()
    new_words = set()
    for word in words:
        if len(word) == n:  # We want only n size words
            new_words.add(word)
            for part in parts_of_string(word):
                partial_words.add(part)
    if len(new_words) == 0:
        return []

    # A list of all the valid paths in board
    moves_list = []

    # Run for any starting point in board
    for start_row in range(len(board)):
        for start_col in range(len(board[0])):
            path = [(start_row, start_col)]  # Add the first cell to the path
            path_set = {(start_row, start_col)}  # Use this set to speed up the code
            # For any starting point add all paths
            _find_length_n_words(n, board, path, path_set, start_row, start_col, partial_words, moves_list,
                                 new_words,
                                 '')

    return moves_list


def _find_length_n_words(n: int, board: Board, path: Path, path_set: set[Tuple[int, int]], row: int, col: int,
                         partial_words: set[str],
                         moves_list: List[Path], words: set[str], word: str) -> None:
    '''An helper function that insert to moves_list all the valid path in starting location'''
    if coordinate_outside_of_board(row, col, board):
        return
    word += board[row][col]  # update word
    if n == len(word):  # if we finish the path
        if word in words:  # if final word in valid words
            moves_list.append(path.copy())  # add final path to moves_list
        return
    if word not in partial_words:  # if word isn't possible to complete finish
        return

    for direction in DIRECTIONS:  # check for any direction
        # update coordinates
        new_row = row + direction[0]
        new_col = col + direction[1]

        coordinate = (new_row, new_col)
        # Thw path can't repeat itself
        if coordinate not in path_set:
            path.append(coordinate)
            path_set.add(coordinate)

            # Move in direction
            _find_length_n_words(n, board, path, path_set, new_row, new_col, partial_words, moves_list, words,
                                 word)

            # reset for next direction
            path.pop()
            path_set.remove(coordinate)


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    '''Return a list that contains path that all of them together is the best solution for game'''
    # Get all the parts of all words in one set
    words = set(words)
    partial_words = set()
    for word in words:
        for part in parts_of_string(word):
            partial_words.add(part)
    taken_words = set()
    size = len(board) ** 2
    moves_list = []

    for n in range(size, 0, -1):
        _get_path_in_n_size_at_board(n, board, words, partial_words, taken_words, moves_list)

    return moves_list


def _get_path_in_n_size_at_board(n: int, board: Board, words: set[str], partial_words: set[str],
                                 taken_words: set[str], moves_list: List[Path]) -> None:
    '''Helper function to max_score_paths that return a list
    that contains all the valid path at n size in board'''

    # Run for any starting point in board
    for start_row in range(len(board)):
        for start_col in range(len(board[0])):
            path = [(start_row, start_col)]  # Add the first cell to the path
            path_set = {(start_row, start_col)}  # Use this set to speed up the code
            # For any starting point add all paths
            _helper_get_path_in_n_size_at_board(n - 1, board, path, path_set, start_row, start_col, partial_words,
                                                moves_list, words,
                                                '', taken_words)


def _helper_get_path_in_n_size_at_board(n: int, board: Board, path: Path, path_set: set[Tuple[int, int]], row: int,
                                        col: int,
                                        partial_words: set[str],
                                        moves_list: List[Path], words: set[str], word: str,
                                        taken_words: set[str]) -> None:
    '''An helper function that insert to moves_list all the valid path in starting location'''
    if coordinate_outside_of_board(row, col, board):
        return
    word += board[row][col]  # update word
    if n == 0:  # if we finish the path
        if word not in taken_words:
            if word in words:  # if final word in valid words
                moves_list.append(path.copy())  # add final path to moves_list
                taken_words.add(word)
        return
    if word not in partial_words:  # if word isn't possible to complete finish
        return

    n -= 1  # counter
    for direction in DIRECTIONS:  # check for any direction
        # update coordinates
        new_row = row + direction[0]
        new_col = col + direction[1]
        coordinate = (new_row, new_col)

        # Thw path can't repeat itself
        if coordinate not in path_set:
            coordinate = (new_row, new_col)
            path.append(coordinate)
            path_set.add(coordinate)

            # Move in direction
            _helper_get_path_in_n_size_at_board(n, board, path, path_set, new_row, new_col, partial_words, moves_list,
                                                words,
                                                word, taken_words)

            # reset for next direction
            path.pop()
            path_set.remove(coordinate)


def get_score1(board: Board, words: Iterable[str]) -> int:
    '''Return max score for game mid-speed option'''
    # Get all the parts of all words in one set
    words = set(words)
    partial_words = set()
    for word in words:
        for part in parts_of_string(word):
            partial_words.add(part)
    taken_words = set()
    size = len(board) ** 2
    score = 0

    for n in range(size, 0, -1):
        score += _get_score_in_n_size_at_board1(n, board, words, partial_words, taken_words)

    return score


def _get_score_in_n_size_at_board1(n: int, board: Board, words: set[str], partial_words: set[str],
                                   taken_words: set[str]) -> int:
    '''Helper function to get_score that return the score for n size paths'''
    score = 0
    # Run for any starting point in board
    for start_row in range(len(board)):
        for start_col in range(len(board[0])):
            path_set = {(start_row, start_col)}  # Use this set to speed up the code
            # For any starting point add all paths
            score += _helper_get_score_in_n_size_at_board1(n - 1, board, path_set, start_row, start_col, partial_words,
                                                           words,
                                                           '', taken_words, 1)
    return score


def _helper_get_score_in_n_size_at_board1(n: int, board: Board, path_set: set[Tuple[int, int]], row: int,
                                          col: int,
                                          partial_words: set[str],
                                          words: set[str], word: str,
                                          taken_words: set[str], score: int) -> int:
    '''An helper function that insert to moves_list all the valid path in starting location'''
    if coordinate_outside_of_board(row, col, board):
        return 0
    word += board[row][col]  # update word
    if n == 0:  # if we finish the path
        if word not in taken_words:
            if word in words:  # if final word in valid words
                taken_words.add(word)
                return score ** 2
        return 0
    if word not in partial_words:  # if word isn't possible to complete finish
        return 0

    score += 1
    sum = 0
    n -= 1  # counter
    for direction in DIRECTIONS:  # check for any direction
        # update coordinates
        new_row = row + direction[0]
        new_col = col + direction[1]
        coordinate = (new_row, new_col)

        # Thw path can't repeat itself
        if coordinate not in path_set:
            coordinate = (new_row, new_col)
            path_set.add(coordinate)

            # Move in direction
            sum += _helper_get_score_in_n_size_at_board1(n, board, path_set, new_row, new_col, partial_words, words,
                                                         word,
                                                         taken_words, score)

            # reset for next direction
            path_set.remove(coordinate)
    return sum


def get_score2(board, words):
    '''Return max score in board slow option'''
    paths = max_score_paths(board, words)
    score = 0
    for path in paths:
        score += len(path) ** 2
    return score


def get_score(board: Board, words: Iterable[str]) -> int:
    '''Return max score for game - fast option'''
    # Get all the parts of all words in one set
    words = set(words)
    partial_words = set()
    for word in words:
        for part in parts_of_string(word):
            partial_words.add(part)
    taken_words = set()
    size = len(board) ** 2
    score = 0

    for n in range(size, 0, -1):
        factor = n ** 2
        score += (_get_score_in_n_size_at_board(n, board, words, partial_words, taken_words) * factor)

    return score


def _get_score_in_n_size_at_board(n: int, board: Board, words: set[str], partial_words: set[str],
                                  taken_words: set[str]) -> int:
    '''Helper function to get_score that return how many paths at n size in board'''
    score = 0
    # Run for any starting point in board
    for start_row in range(len(board)):
        for start_col in range(len(board[0])):
            path_set = {(start_row, start_col)}  # Use this set to speed up the code
            # For any starting point add all paths
            score += _helper_get_score_in_n_size_at_board(n - 1, board, path_set, start_row, start_col, partial_words,
                                                          words,
                                                          '', taken_words)
    return score


def _helper_get_score_in_n_size_at_board(n: int, board: Board, path_set: set[Tuple[int, int]], row: int,
                                         col: int,
                                         partial_words: set[str],
                                         words: set[str], word: str,
                                         taken_words: set[str]) -> int:
    '''Helper function to get_score that return how many paths at n size in board starting from row, col'''
    if coordinate_outside_of_board(row, col, board):
        return 0
    word += board[row][col]  # update word
    if n == 0:  # if we finish the path
        if word not in taken_words:
            if word in words:  # if final word in valid words
                taken_words.add(word)
                return 1
        return 0
    if word not in partial_words:  # if word isn't possible to complete finish
        return 0

    sum = 0
    n -= 1  # counter
    for direction in DIRECTIONS:  # check for any direction
        # update coordinates
        new_row = row + direction[0]
        new_col = col + direction[1]
        coordinate = (new_row, new_col)

        # Thw path can't repeat itself
        if coordinate not in path_set:
            coordinate = (new_row, new_col)
            path_set.add(coordinate)

            # Move in direction
            sum += _helper_get_score_in_n_size_at_board(n, board, path_set, new_row, new_col, partial_words, words,
                                                        word,
                                                        taken_words)

            # reset for next direction
            path_set.remove(coordinate)
    return sum
