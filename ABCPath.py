LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_MAX_INDEX = 25
locations_dictionary = {}


def initialize_locations_dictionary(clues, A_location):
    global locations_dictionary
    for letter in LETTERS:
        if letter != 'A' and letter != 'Z':
            curr_clue = clues[letter]
            if 'row' in curr_clue:
                row = curr_clue[1]
                relevant_indexes = [[row, 0], [row, 1], [row, 2], [row, 3], [row, 4]]
            elif 'col' in curr_clue:
                col = curr_clue[1]
                relevant_indexes = [[0, col], [1, col], [2, col], [3, col], [4, col]]
            else:
                diag_type = curr_clue[1]
                if diag_type == 0:
                    relevant_indexes = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
                elif diag_type == 1:
                    relevant_indexes = [[4, 0], [3, 1], [2, 2], [1, 3], [0, 4]]
            locations_dictionary[letter] = relevant_indexes
    # print locations_dictionary
    preProcessing(A_location)


def preProcessing(A_location):
    global locations_dictionary
    flag = True
    while flag:
        flag = False
        for index in range(len(locations_dictionary)):
            letter = sorted(locations_dictionary.iterkeys())[index]
            if index == 0:
                before_letter_locations = A_location
            else:
                before_letter = sorted(locations_dictionary.iterkeys())[index - 1]
                before_letter_locations = locations_dictionary[before_letter]
            if index + 1 < len(locations_dictionary):
                next_letter = sorted(locations_dictionary.iterkeys())[index + 1]
                next_letter_locations = locations_dictionary[next_letter]
            else:
                next_letter_locations = []
            letter_locations = locations_dictionary[letter]
            remove_locations = []
            for loc in letter_locations:
                remove_before = True
                curr_row = loc[0]
                curr_col = loc[1]
                for before_loc in before_letter_locations:
                    before_row = before_loc[0]
                    before_col = before_loc[1]
                    if abs(before_row - curr_row) <= 1 and abs(before_col - curr_col) <= 1 and not \
                            (abs(before_row - curr_row) == 0 and abs(before_col - curr_col) == 0) and not loc == A_location[0]:
                        remove_before = False
                if remove_before:
                    if loc in locations_dictionary[letter]:
                        remove_locations.append(loc)
                        flag = True
                remove_next = True
                for next_loc in next_letter_locations:
                    next_row = next_loc[0]
                    next_col = next_loc[1]
                    if abs(next_row - curr_row) <= 1 and abs(next_col - curr_col) <= 1 and not \
                            (abs(next_row - curr_row) == 0 and abs(next_col - curr_col) == 0) and not loc == A_location[0]:
                        remove_next = False
                if remove_next and letter != 'Y':
                    if loc in locations_dictionary[letter]:
                        remove_locations.append(loc)
                        flag = True
            for location in remove_locations:
                if location in locations_dictionary[letter]:
                    locations_dictionary[letter].remove(location)
    flag = False
    for letter in locations_dictionary:
        if locations_dictionary[letter]:
            flag = True
    if not flag:
        print 'no solution for this board'
        exit(0)


def compute_optionals(optional_locations, prev_row, prev_col, letter, board):
    for index in locations_dictionary[letter]:
        if abs(prev_row - index[0]) <= 1 and abs(prev_col - index[1]) <= 1 and not \
                (abs(prev_row - index[0]) == 0 and abs(prev_col - index[1]) == 0) \
                and board[index[0]][index[1]] == '0':
            optional_locations.append(index)
    return optional_locations


def findABCPath(board, letter, prev_letter):
    print board
    pause = True
    for i in board:
        if '0' in i:
            pause = False
            break
    if pause:
        print board
        exit(0)
    else:
        prev_row = prev_letter[0]
        prev_col = prev_letter[1]
        optional_locations = []
        compute_optionals(optional_locations, prev_row, prev_col, LETTERS[letter], board)
        if not optional_locations:
            print 'hi'
            return
        for loc in optional_locations:
            print loc
            board[loc[0]][loc[1]] = LETTERS[letter]
            if letter < LETTERS_MAX_INDEX-1:
                findABCPath(board, letter+1, [loc[0], loc[1]])
                board[loc[0]][loc[1]] = '0'
            else:
                findABCPath(board, letter, [loc[0], loc[1]])
                board[loc[0]][loc[1]] = '0'

clues = {'B': ['col', 4], 'C': ['row', 2], 'D': ['col', 3], 'E': ['col', 4], 'F': ['col', 3], 'G': ['row', 4],
         'H': ['row', 3], 'I': ['row', 4], 'J': ['diag', 1], 'K': ['row', 3], 'L': ['row', 2], 'M': ['diag', 0],
         'N': ['col', 2], 'O': ['row', 0], 'P': ['diag', 1], 'Q': ['row', 1], 'R': ['row', 1], 'S': ['col', 2],
         'T': ['diag', 0], 'U': ['col', 1], 'V': ['row', 0], 'W': ['col', 0], 'X': ['col', 0], 'Y': ['col', 1]}

clues2 = {'B': ['col', 2], 'C': ['diag', 1], 'D': ['row', 4], 'E': ['row', 3], 'F': ['col', 1], 'G': ['diag', 1],
         'H': ['col', 0], 'I': ['row', 2], 'J': ['col', 0], 'K': ['diag', 0], 'L': ['col', 2], 'M': ['row', 2],
         'N': ['diag', 0], 'O': ['col', 3], 'P': ['row', 4], 'Q': ['row', 3], 'R': ['col', 4], 'S': ['row', 1],
         'T': ['col', 4], 'U': ['col', 3], 'V': ['row', 0], 'W': ['col', 1], 'X': ['row', 0], 'Y': ['row', 1]}

noSolclues = {'B': ['col', 3], 'C': ['diag', 1], 'D': ['row', 4], 'E': ['row', 3], 'F': ['col', 1], 'G': ['diag', 1],
         'H': ['col', 0], 'I': ['row', 2], 'J': ['col', 0], 'K': ['diag', 0], 'L': ['col', 2], 'M': ['row', 2],
         'N': ['diag', 0], 'O': ['col', 3], 'P': ['row', 4], 'Q': ['row', 3], 'R': ['col', 4], 'S': ['row', 1],
         'T': ['col', 4], 'U': ['col', 2], 'V': ['row', 0], 'W': ['col', 1], 'X': ['row', 0], 'Y': ['row', 1]}


board = []
board2 = []
noSolBoard = []
for i in range(5):
    board.append([])
    board2.append([])
    noSolBoard.append([])
    for j in range(5):
       board[i].append('0')
       board2[i].append('0')
       noSolBoard[i].append('0')
board[2][4] = 'A'
board2[1][3] = 'A'
noSolBoard[1][3] = 'A'

curr_clues = clues
A_location = [[2,4]]
curr_board = board

initialize_locations_dictionary(curr_clues, A_location)
findABCPath(curr_board, 1, A_location[0])

flag = False

for index in curr_board:
    if not flag:
        for i in index:
            if not flag:
                if '0' in i:
                    print 'no solution for this board'
                    flag = True
if not flag:
    print curr_board



