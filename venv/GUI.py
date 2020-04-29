import pygame
import time
pygame.font.init()

def random_number_generator(easy,medium,hard):
    pass


class Cube:
    rows=cols=9
    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def draw_outer_squares(self,screen):
        black = (0,0,0)
        for i in range(3):
            for j in range(3):
                y = i*180
                x = j*180
                pygame.draw.rect(screen, (black), (x, y, 180, 180), 3)

    def draw_smaller_squares(self,screen):
        black = (0, 0, 0)
        for i in range(7):
            for j in range(7):
                y = i * 60
                x = j * 60
                pygame.draw.rect(screen, (black), (x, y, 180, 180), 1)


# screen stats
screen = pygame.display.set_mode((541,600))
pygame.display.set_caption("Sudoku")
white = (255,255,255)
screen.fill(white)
fnt = pygame.font.SysFont("comicsans", 40)
text = fnt.render("Time: ", 1, (0,0,0))
screen.blit(text, (380, 560))
cube = Cube(10,10,10,10,10)
cube.draw_outer_squares(screen)
cube.draw_smaller_squares(screen)
pygame.display.update()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False



# pygame automatically quits modules
pygame.quit()