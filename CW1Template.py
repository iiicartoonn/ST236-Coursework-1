import csv
from copy import deepcopy

groupNumber = 6
groupName = {'Matthew Thorpe' : 'u2272464',\
             'Pedro Ramos Cervero' : 'u5593619',\
             'Person 3 name' : 'Person 3 Username',\
             'Person 4 name' : 'Person 4 Username',\
             'Person 5 name' : 'Person 5 Username'}


###############################################################################
# Task 1

def newGame(p1: str, p2: str) -> dict:
    """
    Create and return a new game state dictionary.

    The returned dict has keys:
      - 'Player 1': player 1 name (str)
      - 'Player 2': player 2 name (str)
      - 'Who': whose turn it is next (1 or 2); starts at 1
      - 'Board': 3D list [level][row][col] with values in {'x', 0, 1, 2}

    Blocked cells are at rows c,d; columns C,D; levels 1,2.

    :param p1: Player 1 name.
    :type p1: str
    :param p2: Player 2 name.
    :type p2: str
    :return: A new game dictionary.
    :rtype: dict
    """

    # catch invalid inputs
    if not isinstance(p1, str) or not isinstance(p2, str):
        raise TypeError("Player names must be strings.")
    
    if p1.strip() == "" or p2.strip() == "":
        raise ValueError("Player names cannot be empty.")
    
    if p1 == p2:
        raise ValueError("Player names must be different.")
    

    # initialise the 3D 6 x 6 x 5 board with all 0s
    board = [[[0 for _ in range(6)] for _ in range(6)] for _ in range(5)]

    # set the blocked cells according to th instruction
    for level in (0, 1):
        for row in (2, 3):
            for col in (2, 3):
                board[level][row][col] = 'x'
    
    return {'Player 1': p1,
            'Player 2': p2,
            'Who': 1,
            'Board': board                                                
            }
    
    


###############################################################################

###############################################################################
# Task 2
def printBoard(board: list) -> str:
    """
    The board is a 3D list [level][row][col].
    The function returns a nicely formatted string representation of the game board.
    Empty cells (0) are shown as spaces, blocked cells are shown as 'x',
    and player moves are shown as digits (1,2).

    :param board: The 3D board list [level][row][col]
    :type board: list
    :return: A formatted string representation of the board
    :rtype: str
    """
    # Defensive check for invalid boards
    if not isinstance(board, list) or len(board) != 5:
        raise ValueError("board must be a 3D list with 5 layers.")

    def cell_to_char(v) -> str:
        # Show empty as blank; keep numbers and 'x'
        return " " if v == 0 else str(v)

    # Build lines for each layer, then stitch layers together line-by-line
    layers_lines = []
    for k in range(5):
        layer = board[k]
        if not isinstance(layer, list) or len(layer) != 6:
            raise ValueError("Each layer must be a 6x6 grid.")

        lines = []
        lines.append(f"   Layer {k+1}   ")
        lines.append(" |A|B|C|D|E|F")
        lines.append("-+-+-+-+-+-+-")

        for r in range(6):
            row_label = chr(ord("a") + r)
            row_vals = [cell_to_char(layer[r][c]) for c in range(6)]

            lines.append(row_label + "|" + "|".join(row_vals))

        layers_lines.append(lines)

    # Join corresponding lines across layers with " | "
    out_lines = []
    for line_idx in range(9):  # 9 lines per layer
        out_lines.append(" | ".join([layers_lines[layer_idx][line_idx] for layer_idx in range(5)]))

    return "\n".join(out_lines)


###############################################################################

###############################################################################
# Task 3

class ColumnFullError(Exception):
    """Raised when a valid column has no empty (0) slot."""
    pass

class InvalidColumnFormat(Exception):
    """Raised when the column string is not exactly one A-F and one a-f."""
    pass

def posToIndex(col: str, board: list) -> list:
    """
    Converts a column string (e.g., 'Aa', 'aA') to a 3D board index [k, j, i].
    k: level (0-indexed from bottom)
    j: row index (0-indexed 'a' through 'f')
    i: column index (0-indexed 'A' through 'F')

    The function finds the first empty slot (value 0) in the specified column.

    :param col: A string representing the column, e.g., 'Aa' or 'bF'.
    :type col: str
    :param board: The 3D game board [level][row][col].
    :type board: list
    :return: A list of three integers [k, j, i] representing the level, row, and column indices.
    :rtype: list
    :raises InvalidColumnFormat: If the input string is not in the correct format.
    :raises ColumnFullError: If the specified column is full.
    """
    # Check whether input is valid
    # e.g., are the letters in col inside (a,b,c,d,e,f) or (A,B,C,D,E,F)
    if len(col) != 2:
        raise InvalidColumnFormat("Column string must be exactly two characters long.")

    # Define valid characters for rows and columns
    row_chars = "abcdef"
    col_chars = "ABCDEF"

    char1, char2 = col[0], col[1]

    row_char = None
    col_char = None

    # Determine which character is the row and which is the column
    if char1.lower() in row_chars and char2.upper() in col_chars:
        row_char = char1.lower()
        col_char = char2.upper()
    elif char2.lower() in row_chars and char1.upper() in col_chars:
        row_char = char2.lower()
        col_char = char1.upper()
    else:
        raise InvalidColumnFormat(
            f"Invalid column format: '{col}'. Expected one lowercase (a-f) and one uppercase (A-F) character."
        )

    # xX can be converted to i and j
    j = row_chars.index(row_char)  # row index
    i = col_chars.index(col_char)  # column index

    # Get board dimensions from board
    num_levels = len(board)

    # Check  all layers and return the index of the first layer that is empty (what's left is what to return for k)
    # Iterate from bottom (level 0) upwards
    for k in range(num_levels):
        if board[k][j][i] == 0:
            return [k, j, i]

    # If after the whole check, and an empty slot (== 0) isn't found,
    # raise the ColumnFullError.
    raise ColumnFullError(f"Column {col} is full.")


###############################################################################

###############################################################################
# Task 4
def indexToPos(ind: list) -> str: 
    # shouldnt be too hard, need to check length of input, convert them to letters according to index
    # raise IndexOutOfRange of any of the integers inside input is not 0-5

###############################################################################

###############################################################################
# Task 5
def saveGame(game: dict, fname: str) -> None:
    """
    Save the game dictionary to a .csv file in the required format.

    :param game: Game dictionary with keys 'Player 1', 'Player 2', 'Who', 'Board'
    :type game: dict
    :param fname: Output filename (should end with .csv)
    :type fname: str
    :return: None
    :rtype: None
    """
    if not fname.lower().endswith(".csv"):
        raise ValueError("Filename must end with .csv")
    
    board = game['Board']

    with open(fname, mode='w', newline='') as f:
        writer = csv.writer(f)

        # Header rows
        writer.writerow(['Player 1', game['Player 1']])
        writer.writerow(['Player 2', game['Player 2']])
        writer.writerow(['Who', game['Who']])
        writer.writerow(['Board'])

        # board rows
        for l in range(5):
            for r in range(6):
                writer.writerow(board[l][r])
###############################################################################

###############################################################################
# Task 6
def loadGame(fname: str) -> dict:
    """
    Load a game dictionary from a .csv file saved in the required coursework format.

    :param fname: Filename of the CSV game file.
    :type fname: str
    :return: Game dictionary with keys 'Player 1', 'Player 2', 'Who', 'Board'
    :rtype: dict
    :raises ValueError: If the file content format is invalid.
    """
    if not isinstance(fname, str):
        raise TypeError("fname must be a string.")
    if not fname.lower().endswith(".csv"):
        raise ValueError("Filename must end with .csv")

    with open(fname, mode="r", newline="") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]

    # Basic structure checks
    if len(rows) < 34:
        raise ValueError("File is too short to be a valid saved game.")

    # Helper to read "Key,Value" rows
    def get_kv(expected_key: str, row_idx: int) -> str:
        row = rows[row_idx]
        if len(row) < 2 or row[0] != expected_key:
            raise ValueError(f"Expected '{expected_key}' on line {row_idx+1}.")
        return row[1]

    p1 = get_kv("Player 1", 0)
    p2 = get_kv("Player 2", 1)
    who_str = get_kv("Who", 2)
    
    try:
        who = int(who_str)
    except ValueError:
        raise ValueError("Who must be an integer 1 or 2.")

    if who not in (1, 2):
        raise ValueError("Who must be 1 or 2.")

    # Board marker line
    if len(rows[3]) == 0 or rows[3][0] != "Board":
        raise ValueError("Expected 'Board' on line 4.")

    board_rows = rows[4:]
    if len(board_rows) != 30:
        raise ValueError(f"Expected 30 board rows after 'Board', found {len(board_rows)}.")

    # Parse the 30 lines into a 5x6x6 board
    board = [[[0 for _ in range(6)] for _ in range(6)] for _ in range(5)]

    # function to covert the values in the csv file into the appropriatae values for each key in the game dict
    def parse_cell(value: str):
        value = value.strip()
        if value == "x":
            return "x"
        # allow "0","1","2"
        try:
            v = int(value)
        except ValueError:
            raise ValueError(f"Invalid board cell value")
        if v not in (0, 1, 2):
            raise ValueError(f"Board cell must be 0, 1, or 2, got {v}.")
        return v

    # loop through each item in each row to populate the board
    idx = 0
    for l in range(5):
        for r in range(6):
            row = board_rows[idx]
            idx += 1
            if len(row) != 6:
                raise ValueError("Each board row must contain exactly 6 values.")
            board[l][r] = [parse_cell(val) for val in row]

    return {"Player 1": p1, 
            "Player 2": p2, 
            "Who": who, 
            "Board": board}

###############################################################################

###############################################################################
# Task 7
def findValidMoves(board: list) -> list:
    #loop through all the columns in the board 
    # return all the columns where at least 1 layer isnt full (== 0)
    # return the format of list of 'xX's
    
###############################################################################

###############################################################################
# Task 8
class MoveNotMade(Exception):
    pass

def makeMove(game: dict, move: str) -> dict:
    # raise the MoveNotMade error any time an invalid move is tried
    # basically use the findValidMoves function in task7, then check if 'move' string is in that list

###############################################################################

###############################################################################
# Task 9
class GameOverError(Exception):
    pass

def isWinner(game: dict) -> int:
    
    
###############################################################################

###############################################################################
# Task 10
def suggestMove(game: dict) -> str:
    # also make use of task 7 function to first get the list of valid moves
    # since the move doesnt need to be smart we can just pick the first index of the list
    # should be very simple

###############################################################################

###############################################################################
# Task 11
def playGame():
    # basically asking for inputs
    # make use of functions written above ( u dont rlly have to wait for them to be done since u know the name alr)
    # all the steps basically follow from the task description (mostly function calls)
    # one important thing is when error is raised, dont let it crash but ask for new input
###############################################################################


###############################################################################
# Testing Function
def testFunctionCalls():
    '''
    Input:  [none]
    
    Output: [none]
    
    You can use this function to test if your function names are correct.
    To call the function: "testFunctionCalls()"
    '''
    c = input('The following function will test whether your code can be \
successfully called, i.e. you have used the correct name. \
This function does not test whether the outputs of the functions \
are of the correct type, so passing this function does not \
guarentee that your code will successfully run and you should \
still perform your own checks. \n\nIf you accept these limitations \
type "y" to proceed: ')
    if c == 'y':
        print('You have chosen to proceed.\n\n')
        try:
            newGame.__doc__
            print('Task 1: Call to "newGame" successful.\n')
        except:
            print('Task 1: Call to "newGame" UNSUCCESSFUL.\n')
        
        try:
            printBoard.__doc__
            print('Task 2: Call to "printBoard" successful.\n')
        except:
            print('Task 2: Call to "printBoard" UNSUCCESSFUL.\n')
            
        try:
            posToIndex.__doc__
            print('Task 3: Call to "posToIndex" successful.')
        except:
            print('Task 3: Call to "posToIndex" UNSUCCESSFUL.')
         
        try:
            InvalidColumnFormat()
            print('Task 3: "InvalidColumnFormat" found.')
        except:
            print('Task 3: "InvalidColumnFormat" NOT FOUND.')
        
        try:
            ColumnFullError()
            print('Task 3: "ColumnFullError" found.\n')
        except:
            print('Task 3: "ColumnFullError" NOT FOUND.\n')
         
        try:
            indexToPos.__doc__
            print('Task 4: Call to "indexToPos" successful.')
        except:
            print('Task 4: Call to "indexToPos" UNSUCCESSFUL.')
        
        try:
            IndexOutOfRange()
            print('Task 4: "IndexOutOfRange" found.\n')
        except:
            print('Task 4: "IndexOutOfRange" NOT FOUND.\n')
        
        try:
            saveGame.__doc__
            print('Task 5: Call to "saveGame" successful.\n')
        except:
            print('Task 5: Call to "saveGame" UNSUCCESSFUL.\n')
            
        try:
            loadGame.__doc__
            print('Task 6: Call to "loadGame" successful.\n')
        except:
            print('Task 6: Call to "loadGame" UNSUCCESSFUL.\n')
            
        try:
            findValidMoves.__doc__
            print('Task 7: Call to "finValidMoves" successful.\n')
        except:
            print('Task 7: Call to "findValidMoves" UNSUCCESSFUL.\n')
            
        try:
            makeMove.__doc__
            print('Task 8: Call to "makeMove" successful.')
        except:
            print('Task 8: Call to "makeMove" UNSUCCESSFUL.')
        
        try:
            MoveNotMade()
            print('Task 8: "MoveNotMade" found.\n')
        except:
            print('Task 8: "MoveNotMade" NOT FOUND.\n')
        
        try:
            isWinner.__doc__
            print('Task 9: Call to "isWinner" successful.\n')
        except:
            print('Task 9: Call to "isWinner" UNSUCCESSFUL.\n')
            
        try:
            suggestMove.__doc__
            print('Task 10: Call to "suggestMove" successful.')
        except:
            print('Task 10: Call to "suggestMove" UNSUCCESSFUL.')
            
        try:
            GameOverError()
            print('Task 10: "GameOverError" found.\n')
        except:
            print('Task 10: "GameOverError" NOT FOUND.\n')
            
        try:
            playGame.__doc__
            print('Task 11: Call to "playGame" successful.\n')
        except:
            print('Task 11: Call to "playGame" UNSUCCESSFUL.\n')
    else:
         print('You have chosen not to proceed.')   
###############################################################################