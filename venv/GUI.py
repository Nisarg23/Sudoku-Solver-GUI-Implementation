import pygame
import time
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
                self.cubes[i][j].place_numbers(x, y)


    def clear_screen(self):
        self.screen.fill((255,255,255))
        fnt = pygame.font.SysFont("comicsans", 40)
        text = fnt.render("Time: ", 1, (0, 0, 0))
        screen.blit(text, (380, 560))

    def click(self,coord):
        i = coord[1] // 60
        j = coord[0] // 60
        x = j*60
        y = i*60

        self.clear_screen()
        self.draw()

        for m in range(9):
            for n in range(9):
                if self.cubes[m][n].clicked_status() == True:
                    self.cubes[m][n].clicked = False

        self.cubes[i][j].draw_cube(self.screen,(255,0,0),x,y,3)
        self.cubes[i][j].clicked = True
        print(self.selected())

    def click_with_mouse(self,i,j):
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


        self.clear_screen()
        self.draw()

        for m in range(9):
            for n in range(9):
                if self.cubes[m][n].clicked_status() == True:
                    self.cubes[m][n].clicked = False

        self.cubes[i][j].draw_cube(self.screen, (255, 0, 0), x, y, 3)
        self.cubes[i][j].clicked = True
        print(self.selected())
    def set(self):
        pass

    def selected(self):
        for i in range(9):
            for j in range(9):
                if self.cubes[i][j].clicked_status() == True:
                    return i, j

        return False


class Cube:
    rows=cols=9
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.clicked = False

    def draw_cube(self,screen,color,x,y,thickness):
        pygame.draw.rect(screen, (color), (x, y, 60, 60), thickness)

    def place_numbers(self,x,y):
        if self.value is not None:
            fnt = pygame.font.SysFont("comicsans", 40)
            num = self.value
            text = fnt.render(str(num), 1, (0, 0, 0))
            screen.blit(text, (x+25,y+20))

    def value(self):
        return value

    def clicked_status(self):
        return self.clicked

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
fnt = pygame.font.SysFont("comicsans", 40)
text = fnt.render("Time: ", 1, (0, 0, 0))
screen.blit(text, (380, 560))


# make sudoku template
cube = Cube(10,10,10)
grid = Grid(board,screen)
grid.draw()
pygame.display.update()


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
                grid.click_with_mouse(0, 0)
            else:
                grid.click_with_mouse(c[0], c[1] - 1)
        elif event.key == pygame.K_RIGHT:
            if grid.selected() == False:
                grid.click_with_mouse(0,0)
            else:
                grid.click_with_mouse(c[0],c[1]+1)
        elif event.key == pygame.K_UP:
            if grid.selected() == False:
                grid.click_with_mouse(0, 0)
            else:
                grid.click_with_mouse(c[0]-1, c[1])
        elif event.key == pygame.K_DOWN:
            if grid.selected() == False:
                grid.click_with_mouse(0, 0)
            else:
                grid.click_with_mouse(c[0]+1, c[1])


    pygame.display.update()
# pygame automatically quits modules
pygame.quit()