import numpy as np
from art import tprint
from time import sleep


class GameFloor:
    """
    accomodates a 3 x 3 square game floor
    contains two functions
    the first one updates the floor with the computer and user choices
    the second prints the floor
    """
    def __init__(self, floor):
        self.floor_squares = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        self.floor = floor

    def assign_value(self, x, y, user):
        self.floor_squares[x][y] = user

    def count_empties(self):
        count = 0
        for row in self.floor_squares:
            for space in row:
                if space == ' ':
                    count += 1
        return count

    def print_floor(self):
        print(f'{self.floor} floor')
        i = 0
        for row in self.floor_squares:
            sleep(0.1)
            print(f' {row[0]} ¦ {row[1]} ¦ {row[2]}')
            if i < 2:
                print('-----------')
            i += 1
        return ""


def start_game():
    """
    Writes the initial message of the site
    displays either instructions of start the game
    depending on user choice
    """
    tprint('3D TIC TAC')
    print('1 .- Instructions')
    print('2 .- Play')
    print('Please choose from the options above')
    while True:
        menu_choice = input('Enter 1 for instructions or 2 to play:\n')
        if validate_number(menu_choice, 2):
            break
    if int(menu_choice) == 1:
        instructions()
        start_game()
    else:
        play_game()


def instructions():
    """
    prints instructions read from file instructions.txt
    provides an example by calling the function example
    after this, lets the game to start
    """
    f = open('instructions.txt')
    lines = f.readlines()
    tprint('HOW TO\n')
    tprint('PLAY\n')
    for line in lines:
        sleep(0.3)
        print(line)
    input('Press enter to see example\n')
    example()
    input('Press enter to go back to the menu\n')


def example():
    """
    writes an example to show the user
    how to make a move and win
    """
    print('In the example, the machine won by 2nd option')
    print('linking vertically all floors with positions')
    print('in row = 1 and column = 2')
    FLOOR_NAMES = ['Third', 'Second', 'First']
    for name in FLOOR_NAMES:
        floor_example = GameFloor(name)
        floor_example.floor_squares[0][1] = 'X'
        floor_example.print_floor()
    print('Enjoy playing')


def play_game():
    """
    starts the game with a random move by the computer
    collects the user move and checks for win or tie
    computer moves and checks for win or tie
    """
    print('First move is by the computer')
    random_machine_move()
    while True:
        get_user_move()
        win_flag = check_win('O')
        if win_flag:
            tprint('CONGRATS')
            tprint('You Win')
            break
        full_flag = check_empty_spaces()
        if full_flag:
            tprint('THIS IS A TIE')
            break
        machine_floor_move()
        win_flag = check_win('X')
        if win_flag:
            tprint('YOU LOSE')
            tprint('TRY AGAIN')
            break
        full_flag = check_empty_spaces()
        if full_flag:
            tprint('THIS IS A TIE')
            break


def random_machine_move():
    """
    creates a random move from the machine
    updates the corresponding floor
    """
    floor_random = np.random.randint(3, size=3)
    update_floor(floor_random, 'X')


def update_floor(data, mover):
    """
    update floor with either machine or user move
    variable data is a list of numbers for [floor,row,column]
    mover variable takes a string value, either 'X' or 'O'
    finally prints the layout
    """
    floors[data[0]].assign_value(data[1], data[2], mover)
    if mover == 'X':
        for floor in floors:
            print(floor.print_floor())


def get_user_move():
    """
    gets the user entries for positions
    asks for floor number, x position and y position
    validates the entries
    if data is valid updates floors array with user entry
    otherwise asks again for data
    """
    while True:
        print('Please chose your move, providing 3 numbers from 1 to 3')
        user_move = []
        while True:
            move = input('Enter floor number, 1 for First, 2 '
                         + 'for Second or 3 for Third:\n')
            if validate_number(move, 3):
                break
        user_move.append(3 - int(move))
        while True:
            move = input('Enter the row position:\n')
            if validate_number(move, 3):
                break
        user_move.append(int(move) - 1)
        while True:
            move = input('Enter the column position:\n')
            if validate_number(move, 3):
                break
        user_move.append(int(move) - 1)
        if empty_point(user_move):
            break
        else:
            print('Space is not free, please choose a free point')
    update_floor(user_move, 'O')


def validate_number(num, max_num):
    """
    Checks that entry is a number between 1 and max_number
    raises a ValueError if entry is not a number or number outside scope
    """
    try:
        int(num)
    except ValueError:
        print(f'Invalid entry: entry must be an integer')
        return False
    if int(num) < 1 or int(num) > max_num:
        print(f'Invalid position: number must be between 1 and {max_num}')
        return False
    return True


def empty_point(data):
    """
    validates if user entry is already busy
    data is a list of numbers for [floor,row,column]
    """
    if floors[data[0]].floor_squares[data[1]][data[2]] == ' ':
        return True
    else:
        return False


def machine_floor_move():
    """
    Decides the next move from the machine by analising the floors
    Calls the update function with the selected move
    """
    win_move = find_critical_column('X')  # winning move by column
    if win_move:
        update_floor(win_move, 'X')
        return
    block_move = find_critical_column('O')  # blocking move by column
    if block_move:
        update_floor(block_move, 'X')
        return
    win_move = find_critical_row_floor('X', 'O')
    if win_move:
        update_floor(win_move, 'X')
        return
    win_move = find_critical_diagonal_floor('X', 'O')
    if win_move:
        update_floor(win_move, 'X')
        return
    block_move = find_critical_row_floor('O', 'X')
    if block_move:
        update_floor(block_move, 'X')
        return
    block_move = find_critical_diagonal_floor('O', 'X')
    if block_move:
        update_floor(block_move, 'X')
        return
    vertical_attack()


def find_critical_row_floor(mover, contender):
    """
    Find rows and lines with two spaces marked by contender
    finds if this row already contains a space filled by the mover
    if not, suggests a move to this empty space.
    """
    floor_num = 0
    for floor in floors:
        lines_sum = summarize_floor(floor.floor_squares, mover)
        ver_sum = lines_sum[:3]
        hor_sum = lines_sum[3:6]
        lines_sum_contender = summarize_floor(floor.floor_squares, contender)
        ver_sum_contender = lines_sum_contender[:3]   # sum of columns
        hor_sum_contender = lines_sum_contender[3:6]  # sum of rows
        available = 3 not in lines_sum and 3 not in lines_sum_contender
        if 2 in ver_sum and available:
            index_mover = np.where(ver_sum == 2)[0]
            for index in index_mover:
                m_move = find_empty_space_vertical(index, ver_sum_contender,
                                                   floor, floor_num)
            if m_move:
                return m_move
        if 2 in hor_sum and available:
            index_mover = np.where(hor_sum == 2)[0]
            for index in index_mover:
                m_move = find_empty_space_row(index, hor_sum_contender,
                                              floor, floor_num)
            if m_move:
                return m_move
        floor_num += 1
    return False


def find_critical_diagonal_floor(mover, contender):
    """
    Finds diagonals with two spaces marked by contender
    finds if this row already contains a space filled by the mover
    if not, suggests a move to this empty space.
    """
    floor_num = 0
    for floor in floors:
        lines_sum = summarize_floor(floor.floor_squares, mover)
        trace = lines_sum[6]
        antitrace = lines_sum[7]
        lines_sum_contender = summarize_floor(floor.floor_squares, contender)
        trace_contender = lines_sum_contender[6]
        antitrace_contender = lines_sum_contender[7]
        available = 3 not in lines_sum and 3 not in lines_sum_contender
        if trace == 2 and available:
            m_move = find_empty_space_trace(trace_contender, floor,
                                            floor_num, 't')
            if m_move:
                return m_move
        if antitrace == 2 and available:
            m_move = find_empty_space_trace(antitrace_contender, floor,
                                            floor_num, 'a')
            if m_move:
                return m_move
        floor_num += 1
    return False


def find_empty_space_vertical(index, data, floor, num):
    """
    explore the vertical lines in floor to find the empty space
    returns the empty space 3-d position
    """
    if data[index] == 0:
        for i in range(3):
            if floor.floor_squares[i][index] == " ":
                next_move = [num, i, index]
                break
        return next_move
    return False


def find_empty_space_row(index, data, floor, num):
    """
    explore the rows in floor to find the empty space
    returns the empty space 3-d position
    """
    if data[index] == 0:
        for i in range(3):
            if floor.floor_squares[index][i] == " ":
                next_move = [num, index, i]
                break
        return next_move
    return False


def find_empty_space_trace(data, floor, num, flag):
    """
    explore the trace in floor to find the empty space
    returns the empty space 3-d position
    """
    if flag == 't':
        sign = 1
        offset = 0
    else:
        sign = -1
        offset = 2
    if data == 0:
        for i in range(3):
            if floor.floor_squares[i][i*sign + offset] == " ":
                next_move = [num, i, i*sign + offset]
                break
        return next_move
    return False


def find_critical_column(mover):
    """
    Find columns with potential win for mover
    returns a 3D position if a empty space is found
    """
    if mover == 'X':
        contender = 'O'
    else:
        contender = 'X'
    column_sum = sumarize_columns(mover)
    column_sum_contender = sumarize_columns(contender)
    for i in range(3):
        for j in range(3):
            m_move = find_empty_space_column(column_sum, column_sum_contender,
                                             i, j)
            if m_move:
                return m_move
    return False


def vertical_attack():
    """
    Computer finds interfloor vertical position to create winning
    alternatives, finding lines with no user positions and one
    computer position using vertical_explore function
    """
    potential_line = vertical_explore()
    if potential_line:
        floor_num = empty_in_line(potential_line)
        move = [floor_num, potential_line[0], potential_line[1]]
        update_floor(move, 'X')
        return
    else:
        move = machine_kernel_move()
        update_floor(move, 'X')
        return


def vertical_explore():
    """
    searches for inter-floor vertical lines
    with only on computer position and no contender positions
    """
    column_sum = sumarize_columns('X')
    column_sum_contender = sumarize_columns('O')
    for i in range(3):
        for j in range(3):
            if column_sum[i, j] == 1 and column_sum_contender[i, j] == 0:
                return [i, j]
    return False


def empty_in_line(line):
    """
    finds the empty inter-floor space
    when the line joining them is a potential win
    """
    floor_num = 0
    for floor in floors:
        if floor.floor_squares[line[0]][line[1]] == ' ':
            return floor_num
        floor_num += 1


def find_empty_space_column(data, data_contender, i, j):
    """
    explore to find the empty space acrooss all floors in
    a straight line
    returns the empty space 3-d position
    """
    if data[i, j] == 2 and data_contender[i, j] == 0:
        floor_num = 0
        for floor in floors:
            if floor.floor_squares[i][j] == " ":
                next_move = [floor_num, i, j]
                break
            floor_num += 1
        return next_move
    return False


def summarize_floor(data, user):
    """
    converts data variable containing a floor into a numpy matrix
    data takes a floor class and user takes either 'X' or 'O'
    """
    floor_matrix = np.zeros((3, 3), dtype=int)
    floor_matrix_mirror = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            if data[i][j] == user:
                floor_matrix[i, j] = 1
                floor_matrix_mirror[i, 2-j] = 1
    sum_row = np.append(np.sum(floor_matrix, axis=0), np.sum(floor_matrix,
                        axis=1))
    sum_row = np.append(sum_row, np.trace(floor_matrix))
    sum_row = np.append(sum_row, np.trace(floor_matrix_mirror))
    return sum_row


def sumarize_columns(user):
    """
    sums columns and return values for the user
    """
    column_sum = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            addition = 0
            for floor in floors:
                if floor.floor_squares[i][j] == user:
                    addition += 1
            column_sum[i, j] = addition
    return column_sum


def machine_kernel_move():
    """
    uses kernels to calculate the probability matrices
    """
    max_val = []
    max_val_coor = []
    for floor in floors:
        prob_matrix = calculate_prob_matrix(floor)
        max_val.append(prob_matrix.max())
        v_max = np.argmax(prob_matrix)//3
        h_max = np.argmax(prob_matrix)-v_max*3
        max_val_coor.append([v_max, h_max])
    max_global = max_val[0]
    max_global_coor = max_val_coor[0]
    max_floor = 0
    for i in range(1, 3):
        if max_val[i] > max_global:
            max_global = max_val[i]
            max_global_coor = max_val_coor[i]
            max_floor = i
    return [max_floor, max_global_coor[0], max_global_coor[1]]


def calculate_prob_matrix(floor):
    """
    calculates and returns probability matrix for kernel based move
    the p_matrix is calculating by multiplying floor matrix and kernels
    """
    machine_multiplier = np.zeros((3, 3), dtype=int)
    user_multiplier = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            if floor.floor_squares[i][j] == 'X':
                machine_multiplier[i, j] = 1
            if floor.floor_squares[i][j] == 'O':
                user_multiplier[i, j] = 1
    p_matrix = np.add(np.matmul(machine_multiplier, machine_kernel),
                      np.matmul(user_multiplier, user_kernel))
    p_matrix = np.add(p_matrix, np.random.rand(3, 3))
    merge_matrix = np.add(machine_multiplier, user_multiplier)
    for i in range(3):
        for j in range(3):
            if merge_matrix[i, j] == 1:
                p_matrix[i, j] = 0
    count_1 = summarize_floor(floor.floor_squares, 'X')
    count_2 = summarize_floor(floor.floor_squares, 'O')
    not_available = 3 in count_1 or 3 in count_2
    if not_available:
        p_matrix[:, :] = 0
    return p_matrix


# variable floors is a structure containing all three separated floors
# each floor structure is obtained by assigning a class GameFloor
floors = [GameFloor('Third'), GameFloor('Second'), GameFloor('First')]

# define kernels as random matrix for both machine and user
machine_kernel = np.random.rand(3, 3)
user_kernel = np.random.rand(3, 3)


def check_win(mover):
    """
    Revises floors to find if either machine or user
    has a winning combination
    """
    column_count = sumarize_columns(mover)
    if 3 in column_count:
        return True
    floor_win = 0
    for floor in floors:
        floor_count = summarize_floor(floor.floor_squares, mover)
        if 3 in floor_count:
            floor_win += 1
    if floor_win == 2:
        return True
    return False


def check_empty_spaces():
    """
    Calculates empty spaces and sends flag to stop
    the game if no empty spaces left
    """
    empties = 0
    for floor in floors:
        count_1 = summarize_floor(floor.floor_squares, 'X')
        count_2 = summarize_floor(floor.floor_squares, 'O')
        available = 3 not in count_1 and 3 not in count_2
        if available:
            empties += floor.count_empties()
    if empties == 0:
        print('no spaces left')
        return True
    return False


def main():
    start_game()


main()
