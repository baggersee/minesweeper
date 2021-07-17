import pygame
pygame.init()
from tkinter import *
import random
import time
from minesweeper_functions import *
    
# MAIN GAME FUNCTION

def main(win,width,ROWS,num_mines):
    
    num_squares = ROWS**2 - num_mines # number of available squares
    num_flags = num_mines
    board = make_grid(ROWS, width)
   
    num_size = size_numbers(ROWS)
    font = pygame.font.Font('freesansbold.ttf',num_size)
    
    field = make_grid(ROWS, width)
    field = mines_setup(field, ROWS, num_mines)
    
    # setting up the parameters of the game
    run = True
    freeze = False
    victory = False
    defeat = False
    
    # initializing the sets of the dug squares or the squares with flags
    dug_set = set()
    flag_set = set()
    
    # starting to count the time
    initial_time = time.time()
    clock_time_mins = 0
    
    while run:
    
        draw(WIN,font,board,ROWS,width)
        
        # computing the time
        clock_time_secs = int(time.time() - initial_time)
        clock_time = time_conversor(clock_time_secs)
        
        if freeze == False:
            
            pygame.display.set_caption("#mines = "+str(num_flags)+" "*20 + "clock: "+ clock_time)
            
        for event in pygame.event.get():
            
            if victory == False:
                # check if already won
                if len(dug_set) == num_squares and len(flag_set) == num_mines:
                    pygame.display.set_caption("YOU WON   :D" + " "*5 + "Press SPACE to play again")
                    victory = True
                    freeze = True
            
            if defeat:
                # gets here if defeated
                pygame.display.set_caption("BOOOM   :(" + " "*5 + "Press SPACE to play again")
                defeat = False
                freeze = True
            
            if freeze:
                # we make 'quitting' and 'playing again' the only possible events
                if event.type == pygame.QUIT:
                    run = False
                    global playing
                    playing = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False
                        start()
                        
            else:
                # gets here if its possible to dig--> standard movement
                
                # quiting the game
                if event.type == pygame.QUIT:
                    run = False
                    playing = False
                
                # digging--> left click
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    # getting the positions in the matrix
                    col,row = get_clicked_pos(pos,ROWS,width) 
                    if (row,col) in dug_set:
                        pass
                        # already dug here -> choosing again
                    
                    if board[row][col] == 'F':
                        pass
                    
                    # dig in a mine
                    elif field[row][col] == 9:
                        # making all the board visible
                        for row in range(ROWS):
                            for col in range(ROWS):
                                if field[row][col] == 0:
                                    board[row][col] = 10
                                else:
                                    board[row][col] = field[row][col]
                        defeat = True
                    
                    # dig in a square with mines next to it
                    elif field[row][col] > 0:
                        dug_set.add((row,col))
                        board[row][col] = field[row][col]
                        
                    # dig in a square with no mines in its surroundings
                    elif field[row][col] ==0:
                        dug_set.add((row,col))
                        board[row][col] = 10
                        # now digging recursively until every square is at least next to a mine
                        P = colindant(board,[row,col])
                        
                        while P != set():
                            # picking the first item in P
                            point = list(P)[0]
                            # getting its coordinates
                            x,y = point[0], point[1]
                            
                            # it is a point with a mine
                            if field[x][y] == 9:
                                # this will never be the case at first iteration
                                P.remove(point)
                                continue 
                            
                            # already dug square
                            elif point in dug_set:
                                P.remove(point)
                                continue
                            
                            elif board[x][y] == 'F':
                                P.remove(point)
                                continue
                                
                            elif field[x][y] > 0:
                                dug_set.add((x,y))
                                P.remove(point)
                                board[x][y] = field[x][y]
                                    
                            elif field[x][y] == 0:
                                dug_set.add((x,y))
                                # we get its colindants
                                R = colindant(board,point)
                                P.remove(point)
                                P = P.union(R)
                                board[x][y] = 10 
                        
                # putting a flag --> right click
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    col,row = get_clicked_pos(pos,ROWS,width)
                    
                    # covered square
                    if board[row][col] == 0:
                        board[row][col] = 'F'
                        num_flags = num_flags - 1
                        if field[row][col] == 9:
                            flag_set.add((row,col)) # putting a flag in a place with a mine
                            
                    # squares with a flag on it
                    elif board[row][col] == 'F':
                        board[row][col] = 0
                        num_flags = num_flags + 1
                        if field[row][col] == 9:
                            flag_set.remove((row,col)) 
                        
                # re-start --> space key
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # setting up new game
                        board = make_grid(ROWS, width)
                        field = make_grid(ROWS, width)
                        field = mines_setup(field, ROWS, num_mines)
                        dug_set = set()
                        flag_set = set()
                        initial_time = time.time()
                        freeze = False
                        num_flags = num_mines
                        
    pygame.quit()


# TKINTER GAME FUNCTION
def start():
    
    global ROW
    ROW = 3
    
    root = Tk()
    root.title('Minesweeper settings')
    root.geometry('500x180')
    
    # Positions of the labels
    rows_select_label = Label(root,text='Choose the number of rows (2-15):')
    rows_select_label.grid(row=0,column=0)
    
    rows_select_label = Label(root,text='Choose the number of mines:')
    rows_select_label.grid(row=1,column=0)
    
    # Choice of the number of rows and the number of mines
    e_1 = Entry(root,width=5,borderwidth=1)
    e_1.grid(row=0, column=1, columnspan=3, padx=2, pady=2)
    
    e_2 = Entry(root,width=5,borderwidth=1)
    e_2.grid(row=1, column=1, columnspan=3, padx=2, pady=2)
    
    def play():
        global ROWS, num_mines
        ROWS = e_1.get() 
        num_mines = e_2.get()
        test = test_settings(ROWS,num_mines)
        global ROW
        ROW = ROW + 1
        
        if test==0:
            
            root.destroy()
            # we call the main function to play
            global WIN
            ROWS = int(ROWS)
            num_mines = int(num_mines)
            WIN = pygame.display.set_mode((WIDTH, WIDTH))
            main(WIN,WIDTH,ROWS, num_mines)
                
        elif test==1.1:
            e_1.delete(0,END)
            e_2.delete(0,END)
            # printing errors
                
            error_label = Label(root,text='no number was given in "rows" and/or "mines"')
            error_label.grid(row=ROW,column=0,columnspan=3,rowspan=1)
           
                
        elif test==1.2:
            e_1.delete(0,END)
            e_2.delete(0,END)
            # printing errors:
                
            error_label = Label(root,text='no number was given in "rows" and/or "mines" ')
            error_label.grid(row=ROW,column=0,columnspan=3,rowspan=1)
            
            
            
        elif test==2:
            e_1.delete(0,END)
            e_2.delete(0,END)
            # printing errors:
               
            error_label = Label(root,text='the number of rows cannot be less than 2 or more than 15')
            error_label.grid(row=ROW,column=0,columnspan=3,rowspan=1)
            
            
            
        elif test==3:
            e_1.delete(0,END)
            e_2.delete(0,END)
            # printing errors:
               
            error_label = Label(root,text='the number of mines cannot exceed rows^2')
            error_label.grid(row=ROW,column=0,columnspan=3,rowspan=1)
          
        return
        
    # button to run the game
    solving_button = Button(root, text="Let's play!",padx=2,pady=2,borderwidth=2,command= lambda: play())
    solving_button.grid(row=3,column=1,columnspan=4)
        
    root.mainloop()
    
# RUNNING THE GAME FUNCTION
start()
