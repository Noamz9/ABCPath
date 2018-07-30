LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_MAX_INDEX = 25
phrase = '('


def create_clauses(clues, A_location):
    global phrase
    # makes sure that one letter exactly is located at each cell
    for cell in range(25):
        list_of_letters_in_cell = []
        for letter in LETTERS:
            if letter != 'A' and letter != 'Z' and letter_in_cell(letter, cell, clues):
                list_of_letters_in_cell.append(letter)
        cell_clause = build_clauses(list_of_letters_in_cell, cell)
        print 'cell clause: ' + str(cell_clause)
        phrase += cell_clause

    # makes sure that every letter is located at exactly one cell
    for letter in LETTERS:
        if letter != 'A' and letter != 'Z':
            temp_list_of_cells = compute_relevant_locations(clues[letter])
            list_of_cells = []
            for index in temp_list_of_cells:
                list_of_cells.append((index[0] * 5) + index[1])
            letter_clause = build_clauses_letters(list_of_cells, letter)
            phrase += letter_clause

    adjacent_pairs = []
    for letter_index in range(24):
        adjacent_pairs.append([LETTERS[letter_index], LETTERS[letter_index + 1]])
    for pair in adjacent_pairs:
        if pair[0] != 'A':
            adjacent_clause = compute_optionals(pair[0], pair[1], clues[pair[0]], clues[pair[1]])
        else:
            adjacent_clause = compute_optionals(pair[0], pair[1], [A_location], clues[pair[1]])
        phrase += adjacent_clause
    phrase = phrase[:-5] + ')'
    print 'phrase: ' + str(phrase)


def compute_optionals(first_letter, second_letter, first_letter_clue, second_letter_clue):
    if first_letter != 'A':
        first_relevant_indexes = compute_relevant_locations(first_letter_clue)
    else:
        first_relevant_indexes = first_letter_clue
    second_relevant_indexes = compute_relevant_locations(second_letter_clue)
    ans = ''
    for index in first_relevant_indexes:
        first = True
        first_cell = (5 * index[0]) + index[1]
        for sec_index in second_relevant_indexes:
            if abs(sec_index[0] - index[0]) <= 1 and abs(sec_index[1] - index[1]) <= 1 and not \
                    (abs(sec_index[0] - index[0]) == 0 and abs(sec_index[1] - index[1]) == 0):
                if first:
                    ans += '(NOT X' + str(first_cell) + first_letter
                    first = False
                second_cell = (5 * sec_index[0]) + sec_index[1]
                ans += ' OR X' + str(second_cell) + second_letter
        if ans != '':
            ans += ') AND '
    print first_letter + ' ' + second_letter + ' ' + ans
    return ans


def compute_relevant_locations(clue):
    if 'row' in clue:
        row = clue[1]
        ans = [[row, 0], [row, 1], [row, 2], [row, 3], [row, 4]]
    elif 'col' in clue:
        col = clue[1]
        ans = [[0, col], [1, col], [2, col], [3, col], [4, col]]
    else:
        diag_type = clue[1]
        if diag_type == 0:
            ans = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
        elif diag_type == 1:
            ans = [[4, 0], [3, 1], [2, 2], [1, 3], [0, 4]]
    return ans


def build_clauses_letters(list_of_cells, letter):
    clause = ''
    for i in range(len(list_of_cells)):
        for j in range(i + 1, len(list_of_cells)):
            if list_of_cells[j] != list_of_cells[i]:
                clause += '(NOT X' + str(list_of_cells[i]) + letter + ' OR NOT X' + str(list_of_cells[j]) + \
                          letter + ') AND '
    return clause


def build_clauses(list_of_letters_in_cell, cell):
    clause = ''
    for i in range(len(list_of_letters_in_cell)):
        for j in range(i + 1, len(list_of_letters_in_cell)):
            if list_of_letters_in_cell[j] != list_of_letters_in_cell[i]:
                clause += '(NOT X' + str(cell) + list_of_letters_in_cell[i] + ' OR NOT X' + str(cell) + list_of_letters_in_cell[j] + ') AND '
    return clause


def letter_in_cell(letter, cell, clues):
    ans = False
    direction = clues[letter][0]
    index = clues[letter][1]
    if direction == 'row':
        if index * 5 <= cell <= (index * 5) + 4:
            ans = True
    elif direction == 'col':
        list_of_cells= []
        for i in range(5):
            list_of_cells.append(index + (i * 5))
        if cell in list_of_cells:
            ans = True
    elif direction == 'diag':
        list_of_cells = []
        if index == 0:
            for i in range(5):
                list_of_cells.append(index + (i * 6))
        else:
            for i in range(5):
                list_of_cells.append(4 + (i * 4))
        if cell in list_of_cells:
            ans = True
    return ans


clues = {'B': ['col', 4], 'C': ['row', 2], 'D': ['col', 3], 'E': ['col', 4], 'F': ['col', 3], 'G': ['row', 4],
         'H': ['row', 3], 'I': ['row', 4], 'J': ['diag', 1], 'K': ['row', 3], 'L': ['row', 2], 'M': ['diag', 0],
         'N': ['col', 2], 'O': ['row', 0], 'P': ['diag', 1], 'Q': ['row', 1], 'R': ['row', 1], 'S': ['col', 2],
         'T': ['diag', 0], 'U': ['col', 1], 'V': ['row', 0], 'W': ['col', 0], 'X': ['col', 0], 'Y': ['col', 1]}
board = []
for i in range(5):
    board.append([])
    for j in range(5):
       board[i].append('0')
board[2][4] = 'A'
A_location = [2,4]
create_clauses(clues, A_location)
