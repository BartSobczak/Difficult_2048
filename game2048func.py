# Bartek's Difficult 2048 Game - game handling
# Last modified: 28.12.2023

# File containing the mechanics of 2048 game 
# along with additional content - the obstacles

import random
OBSTACLE_VALUE = 1
OBSTACLE_LIMIT = 8
BOARD_SIZE = 4
NEW_CELL_VAL = [2,4]


class Board_cell():

    def __init__(self):
        self.value = 0
        self.merged = False


class Game():

    def __init__(self, n_obstacles):
        self.game_board = [[Board_cell() for _ in range(4)] for _ in range(4)]
        self.number_of_moves = 0
        self.number_of_obstacles = n_obstacles
        self.score = 0
        for _ in range(2):
            self.generate_random_cell(start = True)
        self.add_obstacles()


    def random_coords(self):
        rand_col = random.randint(0,BOARD_SIZE-1)
        rand_row = random.randint(0,BOARD_SIZE-1)
        while self.game_board[rand_row][rand_col].value != 0:
            rand_col = random.randint(0,BOARD_SIZE-1)
            rand_row = random.randint(0,BOARD_SIZE-1)
        coords = (rand_row, rand_col)
        return coords


    def add_obstacles(self):
        # each obstacle contains a unique odd number, so that they can't merge 
        # with regular tiles and themselves
        for i in range(self.number_of_obstacles):
            coords = self.random_coords()
            self.game_board[coords[0]][coords[1]].value = OBSTACLE_VALUE + i*2


    def generate_random_cell(self, start):
        coords = self.random_coords()
        rd = random.uniform(0, 1)
        if rd > 0.9 and start == False:
            # 10% chance for generating 4 instead of 2 as a new cell
            self.game_board[coords[0]][coords[1]].value = NEW_CELL_VAL[1]
        else:
            self.game_board[coords[0]][coords[1]].value = NEW_CELL_VAL[0]


    def merge(self, from_cell_row, from_cell_col, into_cell_row, into_cell_col):
        self.score += self.game_board[into_cell_row][into_cell_col].value*2
        self.game_board[from_cell_row][from_cell_col].value = 0
        self.game_board[into_cell_row][into_cell_col].value *= 2
        
        
    def move_horiz(self,dir,test=False):
        # move_done is an indicator for checking if the move is possible 
        # (when we check whether the game is over)
        move_done = False
        # set the parameters for iterating
        if dir == "left":
            start_row = 0
            sign = 1
        if dir == "right":
            start_row = BOARD_SIZE - 1
            sign = -1
        # reset the merge information
        for i in range (BOARD_SIZE):
            for j in range (BOARD_SIZE):
                self.game_board[i][j].merged = False
        for r in range (BOARD_SIZE):
            # in each row we have to iterate BOARD_SIZE^2 times to make sure everything is moved correctly
            for _ in range (BOARD_SIZE-1):
                for j in range(BOARD_SIZE-1):
                    curr_cell = self.game_board[r][start_row + (j+1)*sign]
                    prev_cell = self.game_board[r][start_row + j*sign]
                    if prev_cell.value == 0 and curr_cell.value != 0:
                        # move
                        self.game_board[r][start_row + j*sign].value = curr_cell.value
                        self.game_board[r][start_row + (j+1)*sign].value = 0
                        move_done = True
                    if (prev_cell.value == curr_cell.value and curr_cell.value != 0 
                        and prev_cell.merged == False and curr_cell.merged == False):
                        # move and merge (merging disabled for checking if the game is over)
                        if not test:
                            self.merge(r, start_row + (j+1)*sign, r, start_row + j*sign)
                            self.game_board[r][start_row + j*sign].merged = True
                        move_done = True
        return move_done


    def move_vert(self, dir,test=False):
        move_done = False
        if dir == "up":
            start_col = 0
            sign = 1
        if dir == "down":
            start_col = BOARD_SIZE - 1
            sign = -1
        for i in range (BOARD_SIZE):
            for j in range (BOARD_SIZE):
                self.game_board[i][j].merged = False
        for c in range (BOARD_SIZE):
            for _ in range (BOARD_SIZE-1):
                for j in range(BOARD_SIZE-1):
                    curr_cell = self.game_board[start_col + (j+1)*sign][c]
                    prev_cell = self.game_board[start_col + j*sign][c]
                    if prev_cell.value == 0 and curr_cell.value != 0:
                        self.game_board[start_col + j*sign][c].value = curr_cell.value
                        self.game_board[start_col + (j+1)*sign][c].value = 0
                        move_done = True
                    if (prev_cell.value == curr_cell.value  and curr_cell.value != 0
                        and prev_cell.merged == False and curr_cell.merged == False):
                        if not test:
                            self.merge(start_col + (j+1)*sign, c, start_col + j*sign , c)
                            self.game_board[start_col + j*sign][c].merged = True
                        move_done = True
        return move_done


    def check_game_over(self):
        # copy the values from the game board to a temporary board
        TEMP = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                TEMP[r][c] = self.game_board[r][c].value
        # check if any move is possible (move function returns True is move is done)
        if (self.move_vert("up", test=True) == False and self.move_vert("down", test=True) == False
            and self.move_horiz("left", test=True) == False and self.move_horiz("right", test=True) == False):
            return True
        # reset the board to the initial state, in case if any move was done
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.game_board[r][c].value = TEMP[r][c]
        return False
        

    def check_victory(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.game_board[r][c].value == 2048:
                    return True   
        return False