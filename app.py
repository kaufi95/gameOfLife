# https://stackoverflow.com/questions/55408277/pygame-best-way-to-implement-buttons

import pygame
import numpy
from button import Button

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 720
CONTROLS_HEIGHT = 100

BLOCKSIZE = 10

ROWS = (WINDOW_HEIGHT - CONTROLS_HEIGHT) // BLOCKSIZE
COLS = WINDOW_WIDTH // BLOCKSIZE

running = False
clock = pygame.time.Clock()
generation = 0
speed = 10


def main():
    global grid, board, controls, speed, running, clock
    pygame.init()
    pygame.display.set_caption("Game Of Life")

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

    # make the surface for the grid
    board = screen.subsurface(
        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT - CONTROLS_HEIGHT))
    board.fill(BLACK)

    # make the surface for the controls
    controls = screen.subsurface(
        (0, WINDOW_HEIGHT - CONTROLS_HEIGHT), (WINDOW_WIDTH, CONTROLS_HEIGHT))
    controls.fill((0, 50, 0))

    draw_controls()

    grid = numpy.zeros((COLS, ROWS))

    while True:
        update_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[1] < WINDOW_HEIGHT - CONTROLS_HEIGHT + BLOCKSIZE / 2:
                        (x, y) = (
                            event.pos[0] // BLOCKSIZE, (event.pos[1] - BLOCKSIZE // 2) // BLOCKSIZE)
                        if (grid[x][y] == 0):
                            grid[x][y] = 1
                        else:
                            grid[x][y] = 0

        pygame.display.update()


def update_game():
    global grid, generation, speed, running, clock
    if running:
        clock.tick(speed)
        generation += 1
        grid = update_grid()
    drawGrid()
    draw_information()


def update_grid():
    global grid
    new_grid = numpy.copy(grid)
    for i in range(COLS):
        if (i == 0 or i == COLS-1):
            continue
        for j in range(ROWS):
            if (j == 0 or j == ROWS-1):
                continue
            # Berechnung der Anzahl von Nachbarn
            neighbors = grid[i-1][j-1] + \
                grid[i-1][j] + \
                grid[i-1][j+1] + \
                grid[i][j-1] + \
                grid[i][j+1] + \
                grid[i+1][j-1] + \
                grid[i+1][j] + \
                grid[i+1][j+1]
            # Regel 1: Eine tote Zelle mit genau drei lebenden Nachbarn wird lebendig.
            if grid[i][j] == 0 and neighbors == 3:
                new_grid[i][j] = 1
            # Regel 2: Eine lebende Zelle mit weniger als zwei lebenden Nachbarn stirbt.
            elif grid[i][j] == 1 and neighbors < 2:
                new_grid[i][j] = 0
            # Regel 3: Eine lebende Zelle mit mehr als drei lebenden Nachbarn stirbt.
            elif grid[i][j] == 1 and neighbors > 3:
                new_grid[i][j] = 0
    return new_grid


def drawGrid():
    global grid, board
    board.fill(BLACK)
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
            if grid[x][y] == 1:
                pygame.draw.rect(board, YELLOW, rect)
            else:
                pygame.draw.rect(board, GRAY, rect, 1)

def draw_information():
    global generation, speed
    font = pygame.font.SysFont('Arial', 16)
    gen_text = font.render("Generation: " + str(generation), True, WHITE)
    speed_text = font.render("Speed: " + str(speed), True, WHITE)

    controls.d.blit(gen_text, (20, 15))
    controls.blit(speed_text, (WINDOW_WIDTH - 100, 15))

def draw_controls():
    global bstart, bstop, bspeedp, bspeedn

    bstart = Button(110, 40 , 80, 40, (200, 200, 0), (100, 100, 0), 'start')
    bstart.draw(controls)
    bstart.clicked = start()

    # bstart = drawButton('start', 80, 40)
    # controls.blit(bstart, (110, 40))

    bstop = drawButton('stop', 80, 40)
    controls.blit(bstop, (210, 40))

    bsave = drawButton('save', 80, 40)
    controls.blit(bsave, (310, 40))

    bload = drawButton('load', 80, 40)
    controls.blit(bload, (410, 40))

    bspeedp = drawButton('+', 40, 40)
    controls.blit(bspeedp, (510, 40))

    bspeedn = drawButton('-', 40, 40)
    controls.blit(bspeedn, (570, 40))


def drawButton(name, x, y):
    button_surface = pygame.Surface((x, y))
    button_surface.fill(YELLOW)
    font = pygame.font.SysFont('Arial', 12)
    text_surface = font.render(name, True, (0, 0, 0))
    button_surface.blit(text_surface, (
        button_surface.get_rect().centerx - text_surface.get_rect().centerx,
        button_surface.get_rect().centery - text_surface.get_rect().centery
    ))
    return button_surface


def start():
    global running
    running = True
    print("start")


def stop():
    global running
    running = False
    print("stop")


def change_speed(value):
    global speed
    if value == 1:
        speed += 5
    elif value == -1:
        if speed > 5:
            speed -= 5


def saveGrid():
    global grid
    # save_file = open("gridData.json", "w")
    # json.dump
    # save grid to file
    pass


def loadGrid():
    global grid
#     import json
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
    # load grid from file and write to grid
    pass


if __name__ == "__main__":
    main()
