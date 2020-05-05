import pygame
import random
import time
import numpy as np, numpy.random
from Solver import solve, valid
pygame.font.init()

class Grid:
    def __init__(self,board,screen):
        self.board = board
        self.screen = screen
        self.cubes = [[],[],[],[],[],[],[],[],[]]
        for i in range(9):
            for j in range(9):
                self.cubes[i].append(Cube(board[i*9+j],i,j))

    def draw(self):
        black = (0, 0, 0)
        # draws outer squares
        for i in range(3):
            for j in range(3):
                x = j * 180
                y = i * 180
                pygame.draw.rect(screen, (black), (x, y, 180, 180), 3)

        # draws inner squares/cubes (these are the objects)
        for i in range(9):
            for j in range(9):
                y = i * 60
                x = j * 60
                self.cubes[i][j].draw_cube(self.screen,(0, 0, 0),x,y,1)
                if self.cubes[i][j].value is not None:
                    if self.cubes[i][j].unchangeable == False:
                        self.cubes[i][j].place_number(x, y,(128,128,128))
                    else:
                        self.cubes[i][j].place_number(x, y, (0,0,0))
                elif self.cubes[i][j].value is None and self.cubes[i][j].tmp_val is not None :
                    self.cubes[i][j].place_temp_number(x, y, (128, 128, 128))


    def reset_screen(self):
        self.screen.fill((255,255,255))
        pygame.draw.rect(screen, (0, 0, 0), (40, 552, 100, 40), 2)
        fnt = pygame.font.SysFont("comicsans", 25)
        text = fnt.render("Check", 1, (0, 0, 0))
        screen.blit(text, (65, 565))
        pygame.draw.rect(screen, (0, 0, 0), (220, 552, 100, 40), 2)
        text = fnt.render("Solve", 1, (0, 0, 0))
        screen.blit(text, (250, 565))
        pygame.draw.rect(screen, (0, 0, 0), (400, 552, 100, 40), 2)
        text = fnt.render("New Board", 1, (0, 0, 0))
        screen.blit(text, (405, 565))
        self.draw()

    def click(self,coord):

        i = coord[1] // 60
        j = coord[0] // 60
        x = j*60
        y = i*60

        self.reset_screen()
        if y < 540:
            for m in range(9):
                for n in range(9):
                    if self.cubes[m][n].clicked_status() == True:
                        self.cubes[m][n].clicked = False

            self.cubes[i][j].draw_cube(self.screen,(255,0,0),x,y,3)
            self.cubes[i][j].clicked = True

        x = coord[0]
        y = coord[1]
        if x >= 40 and x <= 140 and y >= 550 and y <= 590:
            self.button_check()
        elif x >= 220 and x <= 320 and y >= 550 and y <= 590:
            self.button_solve()
        elif x >= 400 and x <= 500 and y >= 550 and y <= 590:
            self.button_new_board()

    def click_with_keyboard(self,i,j):
        if i > 8:
            i = 8
        elif i < 0:
            i = 0
        if j > 8:
            j = 8
        elif j < 0:
            j = 0

        x = j * 60
        y = i * 60


        self.reset_screen()

        for m in range(9):
            for n in range(9):
                if self.cubes[m][n].clicked_status() == True:
                    self.cubes[m][n].clicked = False

        self.cubes[i][j].draw_cube(self.screen, (255, 0, 0), x, y, 3)
        self.cubes[i][j].clicked = True


    def set_temp(self,num):
        i, j = self.selected()
        x = i * 60
        y = j * 60
        self.cubes[i][j].tmp_val = num
        self.reset_screen()
        self.click_with_keyboard(i,j)
        self.cubes[i][j].place_temp_number(y,x,(128,128,128))

    def set(self):
        i, j = self.selected()
        x = i * 60
        y = j * 60
        self.cubes[i][j].value = self.cubes[i][j].tmp_val
        self.cubes[i][j].tmp_val = None
        self.cubes[i][j].place_number(y,x,(128,128,128))
        self.reset_screen()
        self.click_with_keyboard(i, j)

    def selected(self):
        for i in range(9):
            for j in range(9):
                if self.cubes[i][j].clicked_status() == True:
                    return i, j

        return False


    def unchangeable(self):
        i,j = self.selected()
        return self.cubes[i][j].get_unchangeable()

    def button_check(self):
        pygame.draw.rect(screen, (255, 0, 0), (40, 552, 100, 40), 2)
        text = fnt.render("Check", 1, (0, 0, 0))
        screen.blit(text, (65, 565))
        pygame.display.update()
        time.sleep(0.15)
        self.solver()
        self.reset_screen()
        for i in range(9):
            for j in range(9):
                x = i*60
                y = j*60
                if self.board[i*9+j] != self.cubes[i][j].value:
                    self.cubes[i][j].draw_circle(self.screen, (255,0, 0), 20, 3)


    def button_solve(self):
        pygame.draw.rect(screen, (255, 0, 0), (220, 552, 100, 40), 2)
        text = fnt.render("Solve", 1, (0, 0, 0))
        screen.blit(text, (250, 565))
        pygame.display.update()
        time.sleep(0.15)
        self.solver()
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].value = self.board[i*9+j]
        self.reset_screen()

    def button_new_board(self):
        pygame.draw.rect(screen, (255, 0, 0), (400, 552, 100, 40), 2)
        text = fnt.render("New Board", 1, (0, 0, 0))
        screen.blit(text, (405, 565))
        pygame.display.update()
        time.sleep(0.15)
        self.new_board()
        self.reset_screen()


    def solver(self):
        solve(self.board, self.cubes, self)

    def new_board(self):
        base = [[1,2,3,4,5,6,7,8,9],
                [4,5,6,7,8,9,1,2,3],
                [7,8,9,1,2,3,4,5,6],
                [2,3,1,5,6,4,8,9,7],
                [5,6,4,8,9,7,2,3,1],
                [8,9,7,2,3,1,5,6,4],
                [3,1,2,6,4,5,9,7,8],
                [6,4,5,9,7,8,3,1,2],
                [9,7,8,3,1,2,6,4,5]]

        # # step 1: swap numbers
        # for i in range(9):
        #     rand = random.randint(0,9)
        #     swap(i, rand, base)

        # # step 2: sawp 1-3 rows, 4-6 rows, and 7-9 rows
        # for i in range(9):
        #     rand = random.randint(0,2)
        #     block_num = i // 3
        #     swap_row = block_num*3 + rand
        #     swap_rows(i, swap_row,base)

        # step 3: swap 1-3 columns, 4-6 columns, and 7-9 columns
        # for i in range(9):
        #     rand = random.randint(0,2)
        #     block_num = i // 3
        #     swap_column = block_num*3 + rand
        #     swap_columns(i, swap_column,base)

        # step 4: swap blocks of rows
        # for i in range(3):
        #     rand = random.randint(0,2)
        #     swap_rows3x3(i,rand,base)

        # step 5: swap bolcks of columns
        print("")
        for i in range(9):
            print(base[i])
        for i in range(3):
            rand = random.randint(0, 2)
            swap_columns3x3(i, rand, base)
            print(i, rand)
        for i in range(9):
            print(base[i])

        # taking 36 random numbers
        b= []
        for i in range(36):
            b.append(1)
        for i in range(45):
            b.append(None)
        random.shuffle(b)

        for i in range(9):
            for j in range(9):
                if b[i*9+j] == 1:
                    board[i*9+j] = base[i][j]
                else:
                    board[i*9+j] = None


        self.cubes = [[], [], [], [], [], [], [], [], []]
        for i in range(9):
            for j in range(9):
                self.cubes[i].append(Cube(board[i * 9 + j], i, j))


class Cube:
    rows=cols=9
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.clicked = False
        self.tmp_val = None
        if self.value == None:
            self.unchangeable = False
        else:
            self.unchangeable = True

    def draw_cube(self,screen,color,x,y,thickness):
        pygame.draw.rect(screen, (color), (x, y, 60, 60), thickness)

    def draw_circle(self,screen,color,radius,width):
        x = self.col*60
        y = self.row*60
        pygame.draw.circle(screen, (color), (x+32, y+30), radius, width)


    def place_number(self,x,y,color):
        fnt = pygame.font.SysFont("comicsans", 40)
        num = self.value
        text = fnt.render(str(num), 1, color)
        screen.blit(text, (x+25,y+20))


    def place_temp_number(self,x,y,color):
        fnt = pygame.font.SysFont("comicsans", 30)
        num = self.tmp_val
        text = fnt.render(str(num), 1, color)
        screen.blit(text, (x + 40, y + 10))

    def value(self):
        return value

    def clicked_status(self):
        return self.clicked
    def get_unchangeable(self):
        return self.unchangeable

def swap(num, rand_num,board):
    if num == 0 or rand_num == 0 or num == rand_num:
        return None

    for i in range(9):
        for j in range(9):
            if board[i][j] == num:
                board[i][j] = rand_num
            elif board[i][j] == rand_num:
                board[i][j] = num

    return None

def swap_rows(row,swap_row,board):
    if row == swap_row:
        return None
    board[row],board[swap_row] = board[swap_row],board[row]
    return None

def swap_columns(column,swap_column,board):
    if column == swap_column:
        return None
    for i in range(9):
        board[i][column], board[i][swap_column] = board[i][swap_column], board[i][column]
    return None

def swap_rows3x3(block,swap_block,board):
    if block == swap_block:
        return None
    board[block*3],board[swap_block*3] = board[swap_block*3],board[block*3]
    board[block*3+1], board[swap_block*3+1] = board[swap_block*3+1], board[block*3+1]
    board[block*3+2], board[swap_block*3+2] = board[swap_block*3+2], board[block*3+2]
    return None

def swap_columns3x3(block,swap_block,board):
    if block == swap_block:
        return None
    for i in range(9):
        board[i][block], board[i][swap_block] = board[i][swap_block], board[i][block]
    return None

#sudoku board
board = [7, 8, None, 4, None, None, 1, 2, None,
              6, None, None, None, 7, 5, None, None, 9,
              None, None, None, 6, None, 1, None, 7, 8,
              None, None, 7, None, 4, None, 2, 6, None,
              None, None, 1, None, 5, None, 9, 3, None,
              9, None, 4, None, 6, None, None, None, 5,
              None, 7, None, 3, None, None, None, 1, 2,
              1, 2, None, None, None, 7, 4, None, None,
              None, 4, 9, 2, None, 6, None, None, 7]

# screen stats
screen = pygame.display.set_mode((541,600))
pygame.display.set_caption("Sudoku")
screen.fill((255,255,255))

fnt = pygame.font.SysFont("comicsans", 25)

pygame.draw.rect(screen, (0,0,0), (40, 552, 100, 40), 2)
text = fnt.render("Check", 1, (0, 0, 0))
screen.blit(text, (65, 565))

pygame.draw.rect(screen, (0,0,0), (220, 552, 100, 40), 2)
text = fnt.render("Solve", 1, (0, 0, 0))
screen.blit(text, (250, 565))

pygame.draw.rect(screen, (0,0,0), (400, 552, 100, 40), 2)
text = fnt.render("New Board", 1, (0, 0, 0))
screen.blit(text, (405, 565))



# make sudoku template
cube = Cube(10,10,10)
grid = Grid(board,screen)
grid.draw()


running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        grid.click(pygame.mouse.get_pos())


    if event.type == pygame.KEYDOWN:
        c = grid.selected()
        if event.key == pygame.K_LEFT:
            if grid.selected() == False:
                grid.click_with_keyboard(0, 0)
            else:
                grid.click_with_keyboard(c[0], c[1] - 1)
        elif event.key == pygame.K_RIGHT:
            if grid.selected() == False:
                grid.click_with_keyboard(0,0)
            else:
                grid.click_with_keyboard(c[0],c[1]+1)
        elif event.key == pygame.K_UP:
            if grid.selected() == False:
                grid.click_with_keyboard(0, 0)
            else:
                grid.click_with_keyboard(c[0]-1, c[1])
        elif event.key == pygame.K_DOWN:
            if grid.selected() == False:
                grid.click_with_keyboard(0, 0)
            else:
                grid.click_with_keyboard(c[0]+1, c[1])
        elif event.key == pygame.K_1:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(1)
        elif event.key == pygame.K_2:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(2)
        elif event.key == pygame.K_3:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(3)
        elif event.key == pygame.K_4:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(4)
        elif event.key == pygame.K_5:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(5)
        elif event.key == pygame.K_6:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(6)
        elif event.key == pygame.K_7:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(7)
        elif event.key == pygame.K_8:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(8)
        elif event.key == pygame.K_9:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(9)
        elif event.key == pygame.K_BACKSPACE:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set_temp(None)
                grid.set()
        elif event.key == pygame.K_RETURN:
            if grid.selected() != False and grid.unchangeable() == False:
                grid.set()




    pygame.display.update()
# pygame automatically quits modules
pygame.quit()