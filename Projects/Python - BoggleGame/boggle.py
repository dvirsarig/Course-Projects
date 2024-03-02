'''
EX - 12
By Levy Ofek and Dvir Sarig
'''

import tkinter as tki
from Game import Game
from Board import Board
from datetime import timedelta
import ex11_utils as helper

BOOGLE_DICT_PATH = "boggle_dict.txt"

# Gui
BUTTON_HOVER_COLOR = "slateblue"
REGULER_COLOR = "azure"
BUTTON_ACTIVE_COLOR = "blue"

BUTTON_STYLE = {"font": ("Courier", 30), "borderwidth": 1, "relief": tki.RAISED, "bg": REGULER_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}

COMMAND_BUTTON_STYLE = {"font": ("Courier", 20), "borderwidth": 2, "relief": tki.RAISED, "bg": "purple",
                        "activebackground": "blue"}
TEXT = 'text'


class Boggle:
    """This class make a GUI object that contains all the frames, labels and buttons
    are needed to play the game. It has game object that helps him to display all the information
    and changes in the game.
    """

    def __init__(self, boggle_game: Game) -> None:
        self.__game = boggle_game
        root = tki.Tk()
        root.geometry("700x600")
        root.title("Boggle Game")
        root.resizable(False, False)
        self.__window = root
        self.__buttons = []
        self.__outer_frame = None
        self.__score_and_time_frame = None
        self.__word_frame = None
        self.__timer_label = None
        self.__score_label = None
        self.__word_label = None
        self.__button_frame = None
        self.__solutions_frame = None
        self.__solutions_label = None
        self.__time_left = timedelta(minutes=3)

    def get_max_score(self) -> int:
        '''Return max score poossible in game'''
        return helper.get_score(self.__game.get_game_board(), self.__game.get_valid_words())

    def __make_button(self, button_char: str, row: int, column: int,
                      row_span: int = 1, column_span: int = 1) -> tki.Button:
        """This function helps to create the simple button of the letters in the game"""
        button = tki.Button(self.__button_frame, text=button_char, **BUTTON_STYLE,
                            command=lambda: self.button_chart_pressed(row, column))
        button.grid(row=row, column=column, rowspan=row_span, columnspan=column_span, sticky=tki.NSEW)
        self.__buttons.append(button)  # Adding the button to a list of all letters buttons

        def on_enter(event):  # Changing color while user on the button
            button["background"] = BUTTON_HOVER_COLOR

        def on_leave(event):  # Changing color while user leaves the button
            button["background"] = REGULER_COLOR

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        return button

    def create_special_button(self) -> None:
        """This function create the special buttons in the game, delete, clear,
        new game and refresh buttons."""
        delete_button = tki.Button(self.__button_frame, text="delete",
                                   **COMMAND_BUTTON_STYLE, command=self.delete_last_letter)
        delete_button.grid(row=4, column=0, rowspan=1, columnspan=1, sticky="nsew")
        quit_button = tki.Button(self.__button_frame, text="quit", **COMMAND_BUTTON_STYLE,
                                 command=self.quit_game)
        quit_button.grid(row=4, column=1, rowspan=1, columnspan=1, sticky="nsew")
        clear_button = tki.Button(self.__button_frame, text="clear", **COMMAND_BUTTON_STYLE,
                                  command=self.clear)
        clear_button.grid(row=4, column=2, rowspan=1, columnspan=1, sticky="nsew")
        restart_button = tki.Button(self.__button_frame, text="new game",
                                    **COMMAND_BUTTON_STYLE, command=self.change_game)
        restart_button.grid(row=4, column=3, rowspan=1, columnspan=1, sticky="nsew")

    def create_buttons_in_buttons_frame(self) -> None:
        """This function use the create button function to make all the button letters in
        specific board"""
        boggle_board = self.__game.get_game_board()  # Get the board of the game
        board_size = self.__game.get_board_size()
        for i in range(board_size):
            for j in range(board_size):
                self.__make_button(boggle_board[i][j], i, j)  # Make the button on each letter

    def update_timer(self) -> None:
        """This function update the timer of the game, and checks if the time is over.
        if the game is over we are display the quit window."""
        self.__time_left = self.__time_left - timedelta(seconds=1)  # Update the current time
        self.__timer_label.config(text=str(self.__time_left))
        if self.__time_left <= timedelta(seconds=0):  # Check if the game is over
            self.quit_game()
        else:
            self.__timer_label.after(1000, self.update_timer)  # Calling the function again

    def start_new_game(self) -> None:
        """This function reset the window that displayed and create a window with the boggle
        game with all the information that needs to each label or button"""
        self.reset_window()  # Clear the pre window
        root = self.__window
        self.__buttons = []
        #  Packing the outer frame
        self.__outer_frame = tki.Frame(root, bg="black", highlightbackground="black",
                                       highlightthickness=5)
        self.__outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # In the next lines we fill and pack the score,timer and the current word labels.
        self.__score_and_time_frame = tki.Frame(self.__outer_frame)
        self.__word_frame = tki.Frame(self.__outer_frame)
        self.__score_and_time_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)
        self.__word_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)
        self.__timer_label = tki.Label(self.__score_and_time_frame, font=("Courier", 30), bg="purple",
                                       width=15, height=1, relief="ridge")
        self.__score_label = tki.Label(self.__score_and_time_frame, font=("Courier", 30), bg="purple",
                                       width=20, height=1, relief="ridge", text="0")
        self.__word_label = tki.Label(self.__word_frame, font=("Courier", 30), bg="pink",
                                      width=10, height=2, relief="ridge", text="")
        self.__timer_label.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)
        self.__score_label.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)
        self.__word_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # In the next lines we create the button and solutions frame
        self.__button_frame = tki.Frame(self.__outer_frame)
        self.__button_frame.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)

        self.__solutions_frame = tki.Frame(self.__outer_frame)
        self.__solutions_frame.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)

        self.__solutions_label = tki.Label(self.__solutions_frame, font=("Courier", 30), bg="white",
                                           width=18, height=8, relief="ridge", text="")
        self.__solutions_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self.create_buttons_in_buttons_frame()  # Call the function to create the letters buttons
        self.create_special_button()  # Call the function to create the other buttons.
        self.__time_left = timedelta(minutes=3)  # Start the timer with 3 minutes
        self.update_timer()

    def reset_window(self) -> None:
        """This function clear the window from all widgets"""
        for widget in self.__window.winfo_children():
            widget.destroy()

    def build_finish_screen(self) -> None:
        """This function create a window with the score of the game that finished
        and ask the user if he wants to play a new game"""
        max_score = self.get_max_score()
        score = f"Your score is: {str(self.__game.get_score())}/{max_score}"
        score_label = tki.Label(self.__window, font=("Courier", 30), bg="purple",
                                width=15, height=5, relief="ridge", text=score)
        score_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        new_game_button = tki.Button(self.__window, text="new game",
                                     **COMMAND_BUTTON_STYLE, command=self.start_new_game)
        new_game_button.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)

    def quit_game(self) -> None:
        """This function clear the window and build the quit window
        it also restarts all the information of the game"""
        self.__buttons_clicked_coordinate = set()
        self.reset_window()  # Clear the window
        self.build_finish_screen()  # Build the new widgets
        self.__game.new_game()  # restart the game

    def button_chart_pressed(self, x: int, y: int) -> None:
        """This function get a location that pressed and update the game if it valid.
        it also checks if the current word is a solution, if yes we update the score and
        clear the word and pre path"""
        if self.__game.check_valid_next_step(x, y):  # Checks if the location is valid path
            self.__game.update_word(x, y)
            self.__word_label[TEXT] = self.__game.get_currect_word()  # Update the word
            if self.__game.check_if_solution():  # Checks if solution
                solution = self.__game.get_currect_word()
                self.update_solutions(solution)
                self.add_score()  # Adding a score
                self.clear()  # Clear the pre word and path

    def delete_last_letter(self) -> None:
        """This function delete the last letter that pressed by the user"""
        word = self.__game.get_currect_word()
        letter = self.__game.get_current_keyboard()
        if len(word) < 1:  # Checks if there is letter to delete
            return
        self.__word_label[TEXT] = self.__word_label[TEXT][:-len(letter)]  # Update the current word
        self.__game.delete_letter()

    def clear(self) -> None:
        """This function delete the pre word and path from the game"""
        self.__word_label[TEXT] = ""
        self.__game.refresh()

    def change_game(self) -> None:
        """This function create a new board and update all the button in the game
        and clear the information from the pre gam"""
        self.__game.new_game()  # Restart the game and get a new board
        board_size = self.__game.get_board_size()
        for i in range(board_size):  # A loop that making all the new letters buttons
            for j in range(board_size):
                index = (i * board_size) + j
                new_char = self.__game.get_game_board()[i][j]
                self.__buttons[index].config(text=new_char)
        self.clear()  # Clear all the information that displayed
        self.__solutions_label[TEXT] = ""
        self.__score_label[TEXT] = 0
        self.__time_left = timedelta(minutes=3)  # Return the timer to his start

    def add_score(self) -> None:
        """This function update the score in the score label"""
        self.__score_label[TEXT] = str(self.__game.get_score())

    def update_solutions(self, word: str) -> None:
        """This function add a solution to the solution label"""
        self.__solutions_label.config(text=self.__solutions_label.cget(TEXT) + "\n" + word)

    def start_game_window(self) -> None:
        """This function create the start window which contain some information
         about the game and start game button to start"""

        start_text = "Welcome to the Boggle game" + "\n" + \
                     "try to find all the words you can in" + "\n" + \
                     "3 minutes! Press the button to start"
        start_label = tki.Label(self.__window, font=("Courier", 20), bg="white",
                                width=15, height=5, relief="ridge", text=start_text)
        start_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        start_game_button = tki.Button(self.__window, text="Start Game",
                                       **COMMAND_BUTTON_STYLE, command=self.start_new_game)
        start_game_button.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)

    def run(self) -> None:
        """This function create the start game window and run the loop of the game"""
        self.start_game_window()
        self.__window.mainloop()


if __name__ == "__main__":
    with open(BOOGLE_DICT_PATH, "r") as file:
        words = {line.strip() for line in file}
    board = Board()
    game = Game(board, words)
    boggle_game = Boggle(game)
    boggle_game.run()
