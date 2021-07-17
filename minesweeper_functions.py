import pygame
pygame.init()
from tkinter import *
import random
import time

# TKINTER INPUT CONTROL 

def test_settings(rows, mines):
    # Error handling function for conflicting inputs
    
    try:
        rows = int(rows)
    except ValueError:
        return 1.1
    
    try:
        mines = int(mines)
    except ValueError:
        return 1.2
    
    if rows < 2 or rows > 15:
        return 2
    
    if mines > rows**2:
        return 3
    
    return 0
    
    
# TIME FUNCTION

def time_conversor(seconds):
    minn = 60 # number of seconds in a minute
    mins = seconds//minn
    if mins == 0:
        secs = seconds
        
    else:
        secs = seconds - mins*minn 
        
    time_formated = str(mins) + ":" + str(secs)
    return time_formated


#VARIABLES FOR PYGAME SETUP

WIDTH = 650 # window size

GREY = (128, 128, 128) # for the grid
RED = (255, 0, 0) # for a mine that exploded
WHITE = (255, 255, 255) # for a covered square
BLACK = (0, 0, 0) # for a flag 

YELLOW = (255,255,0) # for 0
LIME = (0,255,0) # for 1
GREEN = (0,128,0) # for 2
AQUA = (0,255,255) # for 3
TEAL = (0,128,128) # for 4
BLUE = (0,0,255) # for 5
NAVY = (0,0,128) # for 6
FUCHSIA = (255,0,255) # for 7
PURPLE = (128,0,128) # for 8


# PYGAME AUXILIAR FUNCTIONS

def size_numbers(rows):
    # function that decides the size of the board depending on the rows and collumns
    # also handles exceptions
    if rows < 2:
        pass
        raise Exception('The row number must be greater than 1')
        
    elif rows > 1 and rows < 5:
        size = 128
        
    elif rows > 4 and rows < 6:
        size = 64
        
    elif rows > 5 and rows < 16:
        size = 32
      
   # the limit for the row number is already controlled in the Tkinter interface 
    return size


def make_grid(rows, width):
    # function to build the matrix that enable to construct the board later
    # rows = number of rows of the board
    # width = pixel length of the window
    # grid = matrix (list of lists) with all 0
	grid = []
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			grid[i].append(0)
    
    # 'grid' is the matrix (list of lists) of the board  
	return grid



def draw_grid(win, rows, width):
    # function to draw the empty board--> called in the aux function 'draw'
	gap = width // rows # every square width
	for i in range(rows):
		pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))
            
            
            
def draw(win,font,grid,rows,width):
    # function that draws the board with the Nodes during all the game
    win.fill(WHITE)
    gap = width // rows
    for row in range(rows):
        for col in range(rows):
            
            if grid[row][col] == 0:
                COLOR = WHITE
                color = WHITE
                NUMBER = ' '
                
            elif grid[row][col] == 'F':
                COLOR = WHITE
                color = BLACK
                NUMBER = "F"
                
            elif grid[row][col] == 10:
                COLOR = GREY
                color = GREY
                NUMBER = "0"
                
            elif grid[row][col] ==1:
                COLOR = GREY
                color = LIME
                NUMBER = "1"
                
            elif grid[row][col] ==2:
                COLOR = GREY
                color = GREEN
                NUMBER = "2"
                
            elif grid[row][col] ==3:
                COLOR = GREY
                color = AQUA
                NUMBER = "3"
                
            elif grid[row][col] ==4:
                COLOR = GREY
                color = TEAL
                NUMBER = "4"
                
            elif grid[row][col] ==5:
                COLOR = GREY
                color = BLUE
                NUMBER = "5"
                
            elif grid[row][col] ==6:
                COLOR = GREY
                color = NAVY
                NUMBER = "6"
                
            elif grid[row][col] ==7:
                COLOR = GREY
                color = FUCHSIA
                NUMBER = "7"
                
            elif grid[row][col] ==8:
                COLOR = GREY
                color = PURPLE
                NUMBER = '8'
            
            elif grid[row][col] == 9:
                COLOR = RED
                color = BLACK
                NUMBER = 'B'
            
            pygame.draw.rect(win,COLOR,(col*gap, row*gap, gap, gap ))
            show_number(win,font,NUMBER,col*gap + gap/3,row*gap + gap/3,color)
           
    draw_grid(win,rows,width)
    pygame.display.update()
    
    
def get_clicked_pos(pos, rows, width):
    # function that saves the (matrix) position when a certain square is clicked 
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def show_number(win,font,n,x,y,col):
    # function that shows the number of mines next to a square in the Tkinter interface
    number = font.render(n,True,col)
    win.blit(number,(x,y))



# AUXILIAR FUNCTIONS FOR THE GAME ALGORITHM

def colindant(M,R):
    # function that gets the position coordinates of the adjacent points of a given point
    # M is the matrix (list of lists) with the points
    # P is a list with the coordinates of a point in M
    P = []
    dim = len(M)
    x = R[0]
    y = R[1]
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i == dim or y+j == dim or x+i<0 or y+j<0:
                continue
            P.append((x+i,y+j))
    
    P = set(P)
    P.remove((x,y))
    return P


def mines_setup(grid,rows,total_mines):
    # function that randomly sets the mine's positions
    # grid is a list of lists
    mines_left = total_mines
    # placing the mines
    while mines_left != 0:
        
        random_x, random_y = random.randrange(0,rows) , random.randrange(0,rows)
                
        if grid[random_x][random_y] !=9:
            mines_left = mines_left - 1
            grid[random_x][random_y] = 9
            neighbours = colindant(grid,[random_x, random_y])
            for neigh in neighbours:
                if grid[neigh[0]][neigh[1]] != 9:
                    grid[neigh[0]][neigh[1]] += 1
                else:
                    pass
        else:
            pass
    return grid