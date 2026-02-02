import csv
from copy import deepcopy

groupNumber = 0
groupName = {'Matthew Thorpe' : 'u2272464',\
             'Person 2 name' : 'Person 2 Username',\
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

###############################################################################

###############################################################################
# Task 3

###############################################################################

###############################################################################
# Task 4

###############################################################################

###############################################################################
# Task 5

###############################################################################

###############################################################################
# Task 6

###############################################################################

###############################################################################
# Task 7

###############################################################################

###############################################################################
# Task 8

###############################################################################

###############################################################################
# Task 9

###############################################################################

###############################################################################
# Task 10

###############################################################################

###############################################################################
# Task 11

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