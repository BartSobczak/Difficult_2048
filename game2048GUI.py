# Bartek's Difficult 2048 Game - the GUI
# Last modified: 28.12.2023

# This file contains functions for displaying the windows and the contents of the game.
# Handling and displaying the grid of board cells is based/inspired by Kite's youtube tutorial:
# https://www.youtube.com/watch?v=b4XP2IcI-Bg&t=37s

from tkinter import *
import time
import game2048func

MOVE_DIRECTIONS = ["left","right","up","down"]
EDGE_LENGTH = 400
CELL_COUNT = 4
CELL_PAD = 10
CELL_FONT = ("Helvetica", 40, "bold")
GAME_COLOR = "#969693"
EMPTY_COLOR = "#a8a8a5"
OBSTACLE_COLOR = "#0e1769"

CELL_COLORS = {2: "#c9c9c1", 4: "#e8e4bc", 8: "#e0a85e", 16: "#f07016",
                   32: "#e83838", 64: "#b30202", 128: "#faf370",
                   256: "#fcff4f", 512: "#d6d929", 1024: "#b2b518",
                   2048: "#64ab07", 4096: "#24bf8c", 8192: "#0e4e8a"}

LABEL_COLORS = {2: "#000000", 4: "#000000", 8: "#000000", 16: "#ffffff",
                   32: "#ffffff", 64: "#ffffff", 128: "#000000",
                   256: "#000000", 512: "#000000", 1024: "#000000",
                   2048: "#ffffff", 4096: "#ffffff", 8192: "#ffffff",}

class GUI(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.grid()
        self.choose_obstacles()
        

    def choose_obstacles(self):
        # creates an initial window with a slider for obstacles selection
        self.master.title('2048')
        self.sld_label = Label(self, text="Select the number of obstacles: 0")
        self.sld_label.grid(row=0, column=0, columnspan=4, pady=10)
        #slider for selecting the no. of obstacles
        self.slider = Scale(self, from_=0, to=game2048func.OBSTACLE_LIMIT, orient=HORIZONTAL, length=200, 
                            command=self.on_slider_change)
        self.slider.grid(row=1, column=0, columnspan=2)
        self.submit_button = Button(self, text="Start Game", command=self.start_game)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)


    def on_slider_change(self, value):
            self.sld_label.config(text=f"Select the number of obstacles: {value}")


    def start_game(self):
        self.victory_achieved = False
        n_obstacles = int(self.slider.get())
        # Clear the window
        for widget in self.winfo_children():
            widget.destroy()
        # Initialize the game
        self.game = game2048func.Game(n_obstacles)      
        self.upper_info()
        self.master.title('2048')
        self.master.bind("<Left>", self.left_arw_press)
        self.master.bind("<Right>", self.right_arw_press)
        self.master.bind("<Up>", self.up_arw_press)
        self.master.bind("<Down>", self.down_arw_press)
        self.grid_cells = []
        self.build_grid()
        self.draw_grid_cells()
        self.mainloop()


    def restart(self):
        self.game_over_window.destroy()
        self.master.destroy()
        root = Tk()
        app = GUI(master=root)
        app.mainloop()


    def upper_info(self):
        label = Label(self, text = "score: ", font=("Arial", 25), height=1)
        label.grid(row=0, column=0)
        label2 = Label(self, text = str(self.game.score), font=("Arial", 25), height=1)
        label2.grid(row=1, column=0)


    def build_grid(self):
        background = Frame(self, bg=GAME_COLOR,
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()
        for row in range(CELL_COUNT):
            grid_row = []
            for col in range(CELL_COUNT):
                cell = Frame(background, bg=EMPTY_COLOR,
                             width=EDGE_LENGTH / CELL_COUNT,
                             height=EDGE_LENGTH / CELL_COUNT)
                cell.grid(row=row, column=col, padx=CELL_PAD,
                          pady=CELL_PAD)
                cell_text = Label(master=cell, text="",
                          bg=EMPTY_COLOR,
                          justify=CENTER, font=CELL_FONT, width=5, height=2)
                cell_text.grid()
                grid_row.append(cell_text)

            self.grid_cells.append(grid_row)


    def draw_grid_cells(self):
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.game.game_board[row][col].value
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="", bg=EMPTY_COLOR)
                elif tile_value % 2 != 0:
                    self.grid_cells[row][col].configure(
                        text=";(", bg=OBSTACLE_COLOR, fg = "#ffffff")
                else:
                    self.grid_cells[row][col].configure(text=str(
                        tile_value), bg=CELL_COLORS[tile_value],
                        fg=LABEL_COLORS[tile_value])
        self.update_idletasks()
    
    # commands binded to arrow moves
    def left_arw_press(self, event):
        self.make_move(MOVE_DIRECTIONS[0])


    def right_arw_press(self, event):
        self.make_move(MOVE_DIRECTIONS[1])


    def up_arw_press(self, event):
        self.make_move(MOVE_DIRECTIONS[2])


    def down_arw_press(self, event):
        self.make_move(MOVE_DIRECTIONS[3])


    def make_move(self, direction):
        moved = False
        if direction == MOVE_DIRECTIONS[0] or direction == MOVE_DIRECTIONS[1]: 
            moved = self.game.move_horiz(direction)
        if direction == MOVE_DIRECTIONS[2] or direction == MOVE_DIRECTIONS[3]: 
            moved = self.game.move_vert(direction)
        if (moved):
            #for the visual purposes, we can make new tile appear slightly later
            self.draw_grid_cells()
            self.game.generate_random_cell(start = False)
            self.upper_info()
            time.sleep(0.1)    
            self.draw_grid_cells()
        if not self.victory_achieved:
            if self.game.check_victory():
                self.victory_achieved = True
                self.game_over_window(victory=True)
                self.update_idletasks()
        if self.game.check_game_over():
            self.master.title('2048 - GAME OVER!!!!!!!!!!')
            self.game_over_window(victory=False)
            self.update_idletasks()


    def game_over_window(self, victory):
        if victory:
            window_title = "2048 - You Win"
            window_size = '400x200'
            upper_text = "CONGRATULATIONS, YOU WIN"
            if self.game.number_of_obstacles == self.game.OBSTACLE_LIMIT:
                upper_text = 'You really need to touch grass.'
        else:
            window_title = "2048 - Game over"
            upper_text = "GAME OVER"
            window_size = '400x150'
        self.game_over_window = Tk()
        self.game_over_window.title(window_title)
        self.game_over_window.geometry(window_size)
        title_label = Label(self.game_over_window, text=upper_text, font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        score_label = Label(self.game_over_window, text=f"Score: {self.game.score}", font=("Arial", 14))
        score_label.pack(pady=10)
        newgame_button = Button(self.game_over_window, text="New Game", command=self.restart)
        newgame_button.pack(pady=10)
        if victory:
            continue_button = Button(self.game_over_window, text="Keep playing", 
                                     command=self.game_over_window.destroy)
            continue_button.pack(pady=10)
        self.game_over_window.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = GUI(master=root)
    app.mainloop()