# importing libraries/modules
import random


# defining functions
def mine_board(rows, cols, mines):
    """generate the game board with all positions left empty using two for
    loops and the range() function, we can take the variables from the
    function to tell us the size of the board. It essentially creates a
    number of lists inside a list or a 2d list/multidimensional array, for
    each list inside the main list represents the rows of the grid so if you
    were to print all the rows in generate_board using a for loop, it will
    stack them on top of each other, and then you can see the columns as
    well. Each value inside each row/list is the first value in the columns.
    """
    generate_board = [['-' for c in range(cols)] for r in range(rows)]

    # populate the board with mines, if we consider the board as two axis
    # from 0 to the length of the variable rows/cols then if we were to
    # use randint() from the random module to randomly pick both the rows and
    # cols coordinates on the board we can randomly place a mine at that
    # location on the already generated variable generate_board
    for m in range(mines):
        random_row = random.randint(0, rows - 1)
        random_column = random.randint(0, cols - 1)
        generate_board[random_row][random_column] = '#'

    # displays the generated board in grid format, with the mines placed
    for line in generate_board:
        print(line)

    # using nested for loops we can iterate through all the cells on the board
    # finding all the cells that do not have mines and calculating how many
    # mines are around that cell
    for row_cell in range(rows):
        for col_cell in range(cols):

            # finds the cells that are not mines and initialises a mine_count
            # variable with the value 0
            if generate_board[row_cell][col_cell] != '#':
                mine_count = 0

                # nested for loops to iterate through the 8 cells surrounding
                # the current cell, which will not be a mine, this is to count
                # the number of mines around the current position, so we can
                # set the value of the current cell to mine_count
                for row_offset in range(-1, 2):
                    for col_offset in range(-1, 2):

                        # two conditions set the boundaries on the main board
                        # between 0 and rows/cols for both axis of the board,
                        # this condition is only met when the current cell +
                        # the offset is inbetween the boundaries of the board
                        if (0 <= row_cell + row_offset < rows) and \
                                (0 <= col_cell + col_offset < cols):

                            # now we know we are inside the boundaries of the
                            # board IF the current cell is a mine + 1 to the
                            # count, it continues to loop and for every square
                            # inside the board that == '#' it + 1 to the count
                            if generate_board[row_cell + row_offset][col_cell + col_offset] == '#':
                                mine_count += 1

                # sets the current cell position to the mine_count variable
                # cast as a string
                generate_board[row_cell][col_cell] = str(mine_count)

    return generate_board


# assigning a function call, to a variable
generate = mine_board(5, 5, 6)

print("\n")

# displays the return value from the function in a grid format
for row in generate:
    print(row)
