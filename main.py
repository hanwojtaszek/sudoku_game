import numpy as np
import copy


def print_welcome_message():
    """
            Print welcome message with initial sudoku board.

            Parameters: N/A
            Returns: N/A
    """
    print("====== WELCOME TO SUDOKU GAME! ======\n")
    print("Here is your sudoku board:")
    print_board(board)


def print_rules():
    """
            Print game rules.

            Parameters: N/A
            Returns: N/A
    """
    print("\nSudoku game rules:")
    print("- Fill in the numbers 1-9 exactly once in every row, column, and 3x3 region.")
    print("- You can insert a number in selected position by giving its row and column index.")
    print("- Indexes are printed on the left (row index) and on the bottom (column index) of the game board.")
    print("- You can overwrite iserted numbers or remove them from the board.")
    print("- You cannot remove numbers that are placed initially in the board.\n")


def print_board(board, row=None, column=None):
    """
            Display game board.

            Parameters: board (list) : game board
                        row (int) : row number
                        column (int) : column number
            Returns: N/A
    """
    display = copy.deepcopy(board)
    for x in enumerate(display):
        for y in enumerate(display):
            if y[0] == 2 or y[0] == 5:
                display[x[0]][y[0]] = str(display[x[0]][y[0]]) + " |"
            else:
                display[x[0]][y[0]] = str(display[x[0]][y[0]]) + " "

            if display[x[0]][y[0]] == "0 ":
                display[x[0]][y[0]] = "  "
            elif display[x[0]][y[0]] == "0 |":
                display[x[0]][y[0]] = "  |"

    # Add "*" when user inserts new number
    if row is not None and column is not None:
        display[row][column] = display[row][column].replace(" ", "*")

    # Board displaying
    print("\nrow:")
    for x in enumerate(display):
        print(x[0] + 1, "   ", " ".join(display[x[0]]))
        if x[0] == 2 or x[0] == 5:
            print("     ", "-" * 7, "+", "-" * 7, "+", "-" * 8)
    print("\ncol:  1  2  3   4  5  6   7  8  9\n\n")


def get_start_indexes(board):
    """
            Get board indexes which are initially filled by numbers.

            Parameters: board (list) : game board
            Returns: start_indexes (list) : list of board positions filled by numbers
    """
    start_indexes = []
    for start_row_index, row in enumerate(board):
        for start_column_index, number in enumerate(row):
            if number != 0:
                start_indexes.append([start_column_index, start_row_index])
    return start_indexes


def choose_option():
    """
            Display available game options and allow user to select one.

            Parameters: N/A
            Returns: option (str) : Option chosen by user
    """
    print("What do you want to do?")
    print("1) Insert or replace number in the board,\n2) Remove existing number from the board,")
    print("3) Reset board,\n4) Show game rules.")
    option = input("Choose option (1 - 4): ")
    option = validate_option(option)
    return option


def validate_option(option):
    """
            Verify if option entered by user is correct.

            Parameters: option (str) : Option chosen by user
            Returns: option (str) : Option chosen by user after validation
    """
    options = ["1", "2", "3", "4"]
    valid_option = False
    while not valid_option:
        if option in options:
            valid_option = True
        else:
            print("Wrong option. Try again!")
            option = input("Choose option (1 - 4): ")
    return option


def play_game(option, board):
    """
            Play game based on chosen option.

            Parameters: option (str) : Option chosen by user
                        board (list) : Game board
            Returns: victory (bool) : Boolean value indicating if user won the game
    """
    if option == "1":
        insert_number(board)
    elif option == "2":
        remove_number(board)
    elif option == "3":
        board = reset_board()
    elif option == "4":
        print_rules()
    victory = check_if_winner(board)
    return victory


def reset_board():
    """
            Reset board.

            Parameters: N/A
            Returns: board (list) : Game board after reset
    """
    print("\nResetting board...")
    board = start_board
    print_board(board)
    return board


def insert_number(board):
    """
            Insert number in the board.

            Parameters: board (list) : Game board
            Returns: board (list) : Game board after inserting number
    """
    print("Which number to add?")
    number = input("Choose number (1-9): ")
    number = int(validate_number(number))

    add_column_index = input("Column (1-9): ")
    add_row_index = input("Row (1-9): ")
    add_column_index, add_row_index = validate_index(add_column_index, add_row_index)
    board[add_row_index - 1][add_column_index - 1] = number

    print_board(board, add_row_index - 1, add_column_index - 1)
    return board


def remove_number(board):
    """
            Remove number from the board.

            Parameters: board (list) : Game board
            Returns: board (list) : Game board after removing number
    """
    print("Which number to remove?")
    remove_column_index = input("Column (1-9): ")
    remove_row_index = input("Row (1-9): ")
    remove_column_index, remove_row_index = validate_index(remove_column_index, remove_row_index)
    board[remove_row_index - 1][remove_column_index - 1] = 0

    print_board(board)
    return board


def validate_number(number):
    """
            Validate number inserted in the board by user.

            Parameters: number (str) : Number given by user
            Returns: number (str) : Number after validation
    """
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    valid_number = False

    while not valid_number:
        if number in numbers:
            valid_number = True
        else:
            print("Incorrect number. Try again!")
            number = input("Choose number (1-9): ")
    return number


def validate_index(column_index, row_index):
    """
            Validate index to add/ remove number given by user.

            Parameters: column_index (str) : Column number given by user
                        row_index (str) : Row number given by user
            Returns: column_index (str) : Column number after validation
                        row_index (str) : Row number after validation
    """
    indexes = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    valid_index = False

    while not valid_index:
        if column_index not in indexes or row_index not in indexes:
            print("Incorrect column and/or row number. Try again!")
            column_index = input("Column (1-9): ")
            row_index = input("Row (1-9): ")
        else:
            validated_index = [int(column_index) - 1, int(row_index) - 1]
            if validated_index in start_indexes:
                print("This field cannot be overwritten. Try again!")
                column_index = input("Column (1-9): ")
                row_index = input("Row (1-9): ")
            else:
                valid_index = True
    return int(column_index), int(row_index)


def check_if_winner(board):
    """
            Check if winning conditions are met (sum of numbers in each row and column = 45)

            Parameters: board (list) : Game board
            Returns: victory (bool) : Boolean value defining if user won the game.
    """
    rows_result = [1 if sum(board[i]) == 45 else 0 for i in range(0, board_length)]
    board_transp = np.array(board).T.tolist()
    columns_result = [1 if sum(board_transp[i]) == 45 else 0 for i in range(0, board_length)]

    if sum(rows_result) + sum(columns_result) == 18:
        print("====== VICTORY :) ! ======")
        victory = True
    else:
        victory = False
    return victory


board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]

# For testing purposes only!
board2 = [[5, 3, 4, 6, 7, 8, 9, 1, 0],
          [6, 7, 2, 1, 9, 5, 3, 4, 8],
          [1, 9, 8, 3, 4, 2, 5, 6, 7],
          [8, 5, 9, 7, 6, 1, 4, 2, 3],
          [4, 2, 6, 8, 5, 3, 7, 9, 1],
          [7, 1, 3, 9, 2, 4, 8, 5, 6],
          [9, 6, 1, 5, 3, 7, 2, 8, 4],
          [2, 8, 7, 4, 1, 9, 6, 3, 5],
          [3, 4, 5, 2, 8, 6, 1, 7, 9]]

# For testing purposes only!
# Uncomment the line below to test "check_if_winner" function. Add number 2 in missing place to complete the board.
# board = board2

start_board = copy.deepcopy(board)
start_indexes = get_start_indexes(board)
board_length = len(board)
victory = False

print_welcome_message()
while not victory:
    option = choose_option()
    victory = play_game(option, board)
