class TextDoc:
    def __init__(self):
        self.__caret = (0, 0)
        self.__text = [[]]

    def move_caret(self, row: int, col: int) -> None:
        """A ValueError exception is triggered if row,col are not legal"""
        if row >= len(self.__text):
            raise ValueError
        else:
            if col > len(self.__text[row]):
                raise ValueError
        self.__caret = (row, col)

    def type_in(self, character: str) -> None:
        if character == "\n":
            self.__text.append([])
            self.__caret = (self.__caret[0] + 1, 0)
        else:
            row = self.__caret[0]
            col = self.__caret[1]
            self.__text[row].insert(col, character)
            self.__caret = (row, col + 1)

    def get_current_line(self) -> str:
        row = self.__caret[0]
        line = ""
        for char in self.__text[row]:
            line += str(char)
        return line




