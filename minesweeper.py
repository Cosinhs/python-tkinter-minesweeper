# Python Version 3
# File: minesweeper.py

from tkinter import *
import tkinter.messagebox
import random

class Minesweeper:
    
    width, height = 15, 15
    mines_percent = 0.1
    
    def __init__(self, master):

        # import images
        self.tile_plain = PhotoImage(file = "images/tile_plain.gif")
        self.tile_clicked = PhotoImage(file = "images/tile_clicked.gif")
        self.tile_mine = PhotoImage(file = "images/tile_mine.gif")
        self.tile_mine_red = PhotoImage(file = "images/tile_mine_red.gif")
        self.tile_flag = PhotoImage(file = "images/tile_flag.gif")
        self.tile_wrong = PhotoImage(file = "images/tile_wrong.gif")
        self.tile_no = {}
        for x in range(1, 9):
            self.tile_no[x] = PhotoImage(file = "images/tile_"+str(x)+".gif")

        # set up frame
        frame = Frame(master)
        frame.pack()

        # show "Minesweeper" at the top
        self.label_top = Label(frame, text="Minesweeper")
        self.label_top.grid(row = 0, column = 0, columnspan = self.width)

        # create flag and clicked tile variables
        self.flags = 0
        self.correct_flags = 0
        self.lclicked = 0
        self.first_clicked = 1

        # create buttons
        self.buttons = {}
        self.mines = 0
        for x in range(1, self.height + 1):
            for y in range(self.width):
                isMine = 0
                # tile image changeable for debug reasons:
                gfx = self.tile_plain
                # currently random amount of mines
                if random.uniform(0.0, 1.0) < self.mines_percent:
                    isMine = 1
                    self.mines += 1
                self.buttons[(x, y)] = { "buttonWidget": Button(frame, image = gfx), "isMine": isMine, "clickState": 0, "nearbyMines": 0, "key": (x, y) }
                self.buttons[(x, y)]["buttonWidget"].bind('<ButtonRelease-1>', self.lclick_wrapper((x, y)))
                self.buttons[(x, y)]["buttonWidget"].bind('<ButtonRelease-3>', self.rclick_wrapper((x, y)))
        
        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key]["buttonWidget"].grid( row = key[0], column = key[1] )

        # find nearby mines and display number on tile
        for key in self.buttons:
            nearby_mines = 0
            for neighbor in self.get_neighbors(key):
                if self.buttons[neighbor]["isMine"] == 1:
                    nearby_mines += 1
            # store mine count in button data list
            self.buttons[key]["nearbyMines"] = nearby_mines
            '''
            if self.buttons[key]["isMine"] == 0:
                if nearby_mines != 0:
                    self.buttons[key]["buttonWidget"].config(image = self.tile_no[self.buttons[key]["nearbyMines"]])
            elif self.buttons[key]["isMine"] == 1:
                self.buttons[key]["buttonWidget"].config(image = self.tile_mine)
            '''
            
        #add mine and count at the end
        self.label_mines = Label(frame, text = "Mines: "+str(self.mines))
        self.label_mines.grid(row = self.height + 1, column = 0, columnspan = self.width // 2)

        self.label_flags = Label(frame, text = "Flags: "+str(self.flags))
        self.label_flags.grid(row = self.height + 1, column = self.width // 2, columnspan = self.width // 2)
        '''
        self.label_lclicked = Label(frame, text = "Lclicked: "+str(self.lclicked))
        self.label_lclicked.grid(row = self.height + 2, column = 0, columnspan = self.width)
        '''
        self.button_replay = Button(frame, text = "Play again", command = self.replay)
        self.button_replay.grid(row = self.height + 2, column = 0, columnspan = self.width)
        
    ## End of __init__

    def replay(self):
        self.mines = 0
        self.flags = 0
        self.correct_flags = 0
        self.lclicked = 0
        self.first_clicked = 1
        for key in self.buttons:
            isMine = 0
            # tile image changeable for debug reasons:
            gfx = self.tile_plain
            # currently random amount of mines
            if random.uniform(0.0, 1.0) < self.mines_percent:
                isMine = 1
                self.mines += 1
            self.buttons[key]["isMine"] = isMine
            self.buttons[key]["buttonWidget"].config(image = gfx)
            self.buttons[key]["clickState"] = 0
            self.buttons[key]["buttonWidget"].bind('<ButtonRelease-1>', self.lclick_wrapper(key))
            self.buttons[key]["buttonWidget"].bind('<ButtonRelease-3>', self.rclick_wrapper(key))
            
        for key in self.buttons:
            nearby_mines = 0
            for neighbor in self.get_neighbors(key):
                if self.buttons[neighbor]["isMine"] == 1:
                    nearby_mines += 1
            # store mine count in button data list
            self.buttons[key]["nearbyMines"] = nearby_mines
            
        self.label_mines.config(text = "Mines: "+str(self.mines))
        self.label_flags.config(text = "Flags: "+str(self.flags))
        
    def get_neighbors(self, key):
        x, y = key[0], key[1]
        to_return = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
        for t in to_return[:]:
            if t[0] in (0, self.height + 1) or t[1] in (-1, self.width):
                to_return.remove(t)
        return to_return

    def lclick_wrapper(self, key):
        return lambda Button: self.lclick(self.buttons[key])

    def rclick_wrapper(self, key):
        return lambda Button: self.rclick(self.buttons[key])

    def lclick(self, button_data):
        if self.first_clicked:
            if button_data["isMine"] == 1:
                button_data["isMine"] = 0
                no_mine_tile = []
                for key in self.buttons:
                    if self.buttons[key]["isMine"] == 0:
                        no_mine_tile.append(key)
                mine_pos = random.choice(no_mine_tile)
                self.buttons[mine_pos]["isMine"] = 1
                # calculate nearby mines again
                for key in [mine_pos, button_data["key"]]:
                    nearby_mines = 0
                    for neighbor in self.get_neighbors(key):
                        if self.buttons[neighbor]["isMine"] == 1:
                            nearby_mines += 1
                    self.buttons[key]["nearbyMines"] = nearby_mines         
                for key in self.get_neighbors(mine_pos):
                    self.buttons[key]["nearbyMines"] += 1
                for key in self.get_neighbors(button_data["key"]):
                    self.buttons[key]["nearbyMines"] -= 1
            '''
            print(button_data["key"])
            print(mine_pos)
            for key in self.buttons:
                if self.buttons[key]["isMine"] == 0:
                    if self.buttons[key]["nearbyMines"] != 0:
                        self.buttons[key]["buttonWidget"].config(image = self.tile_no[self.buttons[key]["nearbyMines"]])
                    else:
                        self.buttons[key]["buttonWidget"].config(image = self.tile_plain)
                elif self.buttons[key]["isMine"] == 1:
                    self.buttons[key]["buttonWidget"].config(image = self.tile_mine)
            '''
            self.first_clicked = 0
        
        if button_data["clickState"] == 0:
            if button_data["isMine"] == 1: #if a mine
                # show all mines and check for flags
                for key in self.buttons:
                    if self.buttons[key]["isMine"] != 1 and self.buttons[key]["clickState"] == 2:
                        self.buttons[key]["buttonWidget"].config(image = self.tile_wrong)
                    elif self.buttons[key]["isMine"] == 1 and self.buttons[key]["clickState"] != 2:
                        self.buttons[key]["buttonWidget"].config(image = self.tile_mine)
                        
                button_data["buttonWidget"].config(image = self.tile_mine_red)
                # end game
                self.gameover()
            else:
                button_data["clickState"] = 1
                self.lclicked += 1
                # change image
                if button_data["nearbyMines"] == 0:
                    button_data["buttonWidget"].config(image = self.tile_clicked)
                    self.clear_empty_tiles(button_data["key"])
                else:
                    button_data["buttonWidget"].config(image = self.tile_no[button_data["nearbyMines"]])
                #self.update_lclicked()
                if self.lclicked == self.width * self.height - self.mines:
                    self.victory()

    def rclick(self, button_data):
        # if not clicked
        if button_data["clickState"] == 0:
            button_data["buttonWidget"].config(image = self.tile_flag)
            button_data["clickState"] = 2
            #button_data["buttonWidget"].unbind('<ButtonRelease-1>')
            # if a mine
            if button_data["isMine"] == 1:
                self.correct_flags += 1
            self.flags += 1
            self.update_flags()
        # if flagged, unflag
        elif button_data["clickState"] == 2:
            button_data["buttonWidget"].config(image = self.tile_plain)
            button_data["clickState"] = 0
            #button_data["buttonWidget"].bind('<ButtonRelease-1>', self.lclick_wrapper(button_data["key"]))
            # if a mine
            if button_data["isMine"] == 1:
                self.correct_flags -= 1
            self.flags -= 1
            self.update_flags()
        if self.mines == self.correct_flags == self.flags:
            self.victory()


    def clear_empty_tiles(self, main_key):
        queue = [main_key]
        while queue:
            key = queue.pop(0)
            for neighbor in self.get_neighbors(key):
                if self.buttons[neighbor]["clickState"] == 0:
                    if self.buttons[neighbor]["nearbyMines"] == 0:
                        self.buttons[neighbor]["buttonWidget"].config(image = self.tile_clicked)
                        queue.append(neighbor)
                    else:
                        self.buttons[neighbor]["buttonWidget"].config(image = self.tile_no[self.buttons[neighbor]["nearbyMines"]])
                    self.buttons[neighbor]["clickState"] = 1
                    self.lclicked += 1
    
    def gameover(self):
        tkinter.messagebox.showinfo("Game Over", "You Lose!")
        for key in self.buttons:
            self.buttons[key]["buttonWidget"].unbind('<ButtonRelease-1>')
            self.buttons[key]["buttonWidget"].unbind('<ButtonRelease-3>')

    def victory(self):
        tkinter.messagebox.showinfo("Game Over", "You Win!")
        for key in self.buttons:
            self.buttons[key]["buttonWidget"].unbind('<ButtonRelease-1>')
            self.buttons[key]["buttonWidget"].unbind('<ButtonRelease-3>')

    def update_flags(self):
        self.label_flags.config(text = "Flags: "+str(self.flags))

    def update_lclicked(self):
        self.label_lclicked.config(text = "Lclicked: "+str(self.lclicked))

### END OF CLASSES ###

def main():
    # create Tk widget
    root = Tk()
    # set program title
    root.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(root)
    # run event loop
    root.mainloop()

if __name__ == "__main__":
    main()
