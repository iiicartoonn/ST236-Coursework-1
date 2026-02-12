import csv
from copy import deepcopy

groupNumber = 6
groupName = {'Neen Rungsmaithong' : 'u2287039',\
             'Pedro Ramos Cervero' : 'u5593619',\
             'Ruihong Chang' : 'u5599966',\
             'Eric Zhang' : 'u5632225'}


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
    if not isinstance(col, str):
        raise InvalidColumnFormat("Column must be a string.")
    if len(col) != 2:
        raise InvalidColumnFormat("Column string must be exactly two characters long.")

    # Define valid characters for rows and columns
    row_chars = "abcdef"
    col_chars = "ABCDEF"

    char1, char2 = col[0], col[1]

    row_char = None
    col_char = None

    # Determine which character is the row and which is the column
    if char1.islower() and char2.isupper():
        if char1 in row_chars and char2 in col_chars:
            row_char = char1
            col_char = char2
    elif char1.isupper() and char2.islower():
        if char2 in row_chars and char1 in col_chars:
            row_char = char2
            col_char = char1
    else:
        raise InvalidColumnFormat(
            f"Invalid column format: '{col}'. Expected one lowercase (a-f) and one uppercase (A-F) character."
        )
    
    if row_char is None or col_char is None:
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

class IndexOutOfRange(Exception):
    """Index outside valid range (0-5)"""
    pass

def indexToPos(ind: list) -> str:
    """
    Converts a list of integer indices [j,i] or [k,j,i] to a column string 'Xx'.
    param ind: A list of integers, either [j,i] or [k,j,i].
                j: row index (0-5 for 'a'-'f')
                i: column index (0-5 for 'A'-'F')
                k (optional): level index (ignored if present).
    :type ind: list
    :return: A string representation of the column, e.g., 'Aa'.
    :rtype: str
    :raises ValueError: If the input list length is not 2 or 3.
    :raises IndexOutOfRange: If any index (j or i) is not an integer between 0 and 5.
    """
    # Define valid characters for rows and columns
    row_chars = "abcdef"
    col_chars = "ABCDEF"
    
    # Validate input length
    if not isinstance(ind, list) or len(ind) not in (2, 3):
        raise IndexOutOfRange("Index must be [j,i] or [k,j,i].")


    # Extract j and i
    j, i = ind[-2], ind[-1]
    k = None
    if len(ind) == 3:
        k = ind[0]

    # Validate indices are integers in range [0, 5] and k in range [0, 4]
    if not (isinstance(i, int) and isinstance(j, int) and 0 <= i <= 5 and 0 <= j <= 5):
        raise IndexOutOfRange(f"Indices j={j} and i={i} must be integers between 0 and 5 (inclusive).")
    if k is not None:
        if not isinstance(k, int) or not (0 <= k <= 4):
            raise IndexOutOfRange(f"k = {k} is invalid. k must be an integer between 0 and 4 inclusive.")

    # Convert indices back to characters
    row_char = row_chars[j]
    col_char = col_chars[i]

    return f"{col_char}{row_char}" #format 'Xx'
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
    if not isinstance(fname, str) or not fname.lower().endswith(".csv"):
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

    board_rows = [r for r in rows[4:] if r]  # ignore blank rows
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
    """
    Return a list of all valid moves on the current board.
    A move is considered valid if (row, column) stack contains at least one empty cell across 5 levels.
    Moves are returned in 'Xx' format.

    :param board: 3d game board represented as board[level][row][column]
    :type board: list
    :return: A list of all valid move strings
    :rtype: list
    """
  
    row_Chars = "abcdef"
    col_Chars = "ABCDEF"
    moves = []

    # We only need to check the highest level (index 4)
    # If the top cell is empty, the column can accept a move.
    for j in range(6): # row
        for i in range(6): # column
            if board[4][j][i] == 0:
                moves.append(col_Chars[i] + row_Chars[j]) #append in the format "Xx"
      
    return moves
      
###############################################################################

###############################################################################
# Task 8
class MoveNotMade(Exception):
    pass

def makeMove(game: dict, move: str) -> dict:
    """
    Apply a new move to the current game and return the new game state.
    
    If the new move is invalid (incorrect format or not playable), MoveNotMade exception is raised.
    
    Otherwise, a deep copy of existing game is created, 
    the counter of the current player is placed in the lowest available level,
    and the turn is switched to the other player.

    :param game: The existing game dictionary
    :type game: dict
    :param move: The new move string
    :type move: str
    :return: A new game dictionary reflecting the new move
    :rtype: dict
    """
    # raise the MoveNotMade error any time an invalid move is tried
    # basically use the findValidMoves function in task7, then check if 'move' string is in that list
    if not isinstance(move, str) or len(move) != 2: # if move is not a string or not have length 2, raise MoveNotMade
      raise MoveNotMade("Invalid Move.")

    row_Chars = "abcdef"
    col_Chars = "ABCDEF"
    c1 = move[0]
    c2 = move[1]

    if c1 in row_Chars and c2 in col_Chars: # standardise the move to 'Xx' version
      standard_Move = c2 + c1
    elif c1 in col_Chars and c2 in row_Chars:
      standard_Move = c1 + c2
    else:
      raise MoveNotMade("Invalid Move.")

    valid_Moves = findValidMoves(game["Board"]) # check whether the move is in the valid move list
    if standard_Move not in valid_Moves:
      raise MoveNotMade("Invalid Move.")

    # if no move error raised, return the game after the new move
    newgame = deepcopy(game)

    try:
        k, j, i = posToIndex(standard_Move, newgame["Board"])
    except (InvalidColumnFormat, ColumnFullError):
        raise MoveNotMade("Invalid Move.")

    player = newgame['Who']
    newgame["Board"][k][j][i] = player # mark the new move
    newgame["Who"] = 2 if player == 1 else 1 # switch the turn
    return newgame
  
###############################################################################

###############################################################################
# Task 9

def isWinner(game: dict) -> int:
    """
    Checks if either player has won (4 in a row) on the 3D board.

    A win is defined as four identical player tokens (1 or 2) in a sequence 
    along any of the 76 possible winning lines in a 6x6x5 grid (horizontal, 
    vertical, or diagonal across any 3D plane).

    Returns:
      1  -> Player 1 has won
      2  -> Player 2 has won
      0  -> no winner yet and there are still empty spaces
     -1  -> no winner and the board is full (draw)
    """
    board = game["Board"]

    # Board dimensions: 5 layers (levels), 6 rows, 6 columns
    K, J, I = 5, 6, 6

    # possible directions for "4 in a row".
    # only include each direction once (no need to check both forward and backward).
    directions = [
        (1, 0, 0),   # straight up through layers (vertical in 3D)
        (0, 1, 0),   # along rows (a->f)
        (0, 0, 1),   # along columns (A->F)

        (0, 1, 1),   # diagonal within a layer (row+col)
        (0, 1, -1),  # diagonal within a layer (row-col)

        (1, 1, 0),   # diagonal across layers and rows
        (1, -1, 0),  # diagonal across layers and rows (other way)

        (1, 0, 1),   # diagonal across layers and cols
        (1, 0, -1),  # diagonal across layers and cols (other way)

        (1, 1, 1),   # full 3D diagonal
        (1, 1, -1),  # full 3D diagonal (one axis reversed)
        (1, -1, 1),  # full 3D diagonal (one axis reversed)
        (1, -1, -1), # full 3D diagonal (two axes reversed)
    ]

    # helper function: checks if indices are inside the board
    def in_bounds(k, j, i) -> bool:
        return 0 <= k < K and 0 <= j < J and 0 <= i < I

    any_empty = False  

    # loop through every position in the 3D board
    for k in range(K):
        for j in range(J):
            for i in range(I):
                v = board[k][j][i]

                # if we ever see a 0, the board isn't full yet
                if v == 0:
                    any_empty = True
                    continue

                # blocked squares ('x') cannot start a winning line
                if v == "x":
                    continue

                # at this point v should be 1 or 2 (a player's counter)

                # try every direction from this starting point
                for dk, dj, di in directions:
                    # find possible end position
                    end_k = k + 3 * dk
                    end_j = j + 3 * dj
                    end_i = i + 3 * di

                    # if the end position would be out of bounds, skip this direction
                    if not in_bounds(end_k, end_j, end_i):
                        continue

                    # check the next 3 cells in this direction are the same as v
                    if (board[k + dk][j + dj][i + di] == v and
                        board[k + 2*dk][j + 2*dj][i + 2*di] == v and
                        board[k + 3*dk][j + 3*dj][i + 3*di] == v):
                        return v  # winner found (1 or 2)

    # no winner found anywhere on the board
    if any_empty:
        return 0   # game still ongoing
    else:
        return -1  # board full and no winner -> draw    
###############################################################################

###############################################################################
# Task 10
class GameOverError(Exception):
    pass

def suggestMove(game: dict) -> str:
    """
    Selects the next move from the available valid moves on the board by selecting the first valid coordinate found during the board scan.

    :param game: A dictionary containing the current 'Board' state and metadata.
    :type game: dict
    :return: The selected move coordinate in 'Xx' format (e.g., 'Ab').
    :rtype: str
    :raises GameOverError: If the board is full and no valid moves remain.
    """
    moves = findValidMoves(game['Board'])

    if not moves:
        raise GameOverError("No valid moves left.")

    return moves[0]  
###############################################################################

###############################################################################
# Task 11
def playGame():
    """
    Runs an interactive game loop for the 3D Connect-4 style game.

    Behaviour:
    - Prompts for Player 1 name. If Player 1 enters "load", the game is loaded from a CSV file.
    - Otherwise prompts for Player 2 name. Player 2 can be "C" to act as a computer player.
    - Prints the board after each move.
    - Repeats until Player 1 wins, Player 2 wins, or the game is a draw.

    Notes:
    - Uses previously defined functions: newGame, loadGame, printBoard, makeMove,
      isWinner, findValidMoves, suggestMove.
    - Relies on custom exceptions: MoveNotMade, GameOverError.
    """

    # loop for player names, either start new game or load existing 
    while True:
        p1 = input("Player 1 name (or 'load'): ").strip()

        # handle load option
        if p1.lower() == "load":
            fname = input("Filename: ").strip()
            try:
                game = loadGame(fname)
                break  # success -> leave loop
            except Exception as e:
                print("Could not load game:", e)
                print("Try again.\n")
                continue

        # otherwise start a new game
        p2 = input("Player 2 name (C for computer): ").strip()

        try:
            game = newGame(p1, p2)
            break  
        except Exception as e:
            print("Invalid input:", e)
            print("Try again.\n")


    # Print initial board
    print(printBoard(game["Board"]))

    # main game loop
    while True:
        # Check if anyone has won (or if the game is finished)
        w = isWinner(game)

        if w == 1:
            # Player 1 has won
            print(f"{game['Player 1']} wins!")
            return

        if w == 2:
            # Player 2 has won
            print(f"{game['Player 2']} wins!")
            return

        # If no valid moves remain, it's a draw (board is full)
        if len(findValidMoves(game["Board"])) == 0:
            print("Draw.")
            return

        # Figure out whose turn it is
        who = game["Who"]  # 1 or 2
        player = game["Player 1"] if who == 1 else game["Player 2"]

        # computer player's turn
        if player == "C":
            try:
                # Suggest any valid move and apply it
                move = suggestMove(game)
                print("Computer plays:", move)
                game = makeMove(game, move)

            except GameOverError:
                # No valid moves left
                print("Draw.")
                return

            except Exception as e:
                # Any unexpected error (helps debugging)
                print("Computer move failed:", e)
                return

        # human player
        else:
            # Keep asking until a valid move is made
            while True:
                move = input(f"{player} enter move (e.g. aA or Aa): ")
                try:
                    # Try to apply the move
                    game = makeMove(game, move)
                    break  # move successful -> exit input loop

                except MoveNotMade:
                    # Move string or column is invalid/full
                    print("Illegal move. Try again.")

                except Exception as e:
                    # Any other unexpected input-related error
                    print("Invalid input:", e)
                    print("Try again.")

        # Print the board after the move
        print(printBoard(game["Board"]))

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