import pygame
import numpy
import json
import pygame_widgets
from pygame_widgets.button import Button

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
    global grid, board_surface, control_surface, speed, running, clock
    pygame.init()
    pygame.display.set_caption("Game Of Life")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

    # make the surface for the grid
    board_surface = screen.subsurface(
        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT - CONTROLS_HEIGHT)
    )
    board_surface.fill(BLACK)

    # make the surface for the controls
    control_surface = screen.subsurface(
        (0, WINDOW_HEIGHT - CONTROLS_HEIGHT), (WINDOW_WIDTH, CONTROLS_HEIGHT)
    )

    grid = numpy.zeros((COLS, ROWS))

    while True:
        update_game()
        events = pygame.event.get()
        for event in events:
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
                            event.pos[0] // BLOCKSIZE,
                            (event.pos[1] - BLOCKSIZE // 2) // BLOCKSIZE,
                        )
                        if (
                            grid[x][y] == 0
                            and x > 0
                            and x < COLS - 1
                            and y > 0
                            and y < ROWS - 1
                        ):
                            grid[x][y] = 1
                        else:
                            grid[x][y] = 0

        draw_controls()
        pygame_widgets.update(events)
        pygame.display.update()


def update_game():
    global grid, generation, speed, running, clock
    if running:
        clock.tick(speed * 2)
        generation += 1
        grid = update_grid()
    drawGrid()


def update_grid():
    global grid
    new_grid = numpy.copy(grid)
    for i in range(COLS):
        if i == 0 or i == COLS - 1:
            continue
        for j in range(ROWS):
            if j == 0 or j == ROWS - 1:
                continue
            # Berechnung der Anzahl von Nachbarn
            neighbors = (
                grid[i - 1][j - 1]
                + grid[i - 1][j]
                + grid[i - 1][j + 1]
                + grid[i][j - 1]
                + grid[i][j + 1]
                + grid[i + 1][j - 1]
                + grid[i + 1][j]
                + grid[i + 1][j + 1]
            )
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
    global grid, board_surface
    board_surface.fill(BLACK)
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x * BLOCKSIZE, y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
            if grid[x][y] == 1:
                pygame.draw.rect(board_surface, YELLOW, rect)
            else:
                pygame.draw.rect(board_surface, GRAY, rect, 1)


def draw_controls():
    global generation, speed
    control_surface.fill((0, 50, 0))
    font = pygame.font.SysFont("Arial", 16)
    gen_text = font.render("Generation: " + str(generation), True, WHITE)
    speed_text = font.render("Speed: " + str(speed), True, WHITE)

    control_surface.blit(gen_text, (20, 15))
    control_surface.blit(speed_text, (WINDOW_WIDTH - 100, 15))

    global running

    text = "Start" if not running else "Stop"
    Button(
        control_surface,
        110,
        40,
        80,
        40,
        text=text,
        fontSize=16,
        inactiveColour=YELLOW,
        pressedColour=GRAY,
        onClick=play_or_pause,
    )

    Button(
        control_surface,
        210,
        40,
        80,
        40,
        text="Reset",
        fontSize=16,
        inactiveColour=YELLOW,
        pressedColour=GRAY,
        onClick=reset_game,
    )

    Button(
        control_surface,
        310,
        40,
        80,
        40,
        text="Save",
        fontSize=16,
        inactiveColour=YELLOW,
        pressedColour=GRAY,
        onClick=save_grid,
    )

    Button(
        control_surface,
        410,
        40,
        80,
        40,
        text="Load",
        fontSize=16,
        inactiveColour=YELLOW,
        pressedColour=GRAY,
        onClick=load_grid,
    )

    Button(
        control_surface,
        510,
        40,
        40,
        40,
        text="+",
        fontSize=16,
        inactiveColour=YELLOW,
        pressedColour=GRAY,
        onClick=lambda: change_speed(1),
    )

    Button(
        control_surface,
        570,
        40,
        40,
        40,
        text="-",
        fontSize=16,
        inactiveColour=YELLOW,
        pressedColour=GRAY,
        onClick=lambda: change_speed(-1),
    )


def reset_game():
    global grid, generation, running, speed
    running = False
    speed = 10
    grid = numpy.zeros((COLS, ROWS))
    generation = 0


def play_or_pause():
    global running
    if not running:
        running = True
        print("play")
    else:
        running = False
        print("pause")


def change_speed(value):
    global speed
    print("speed: " + str(value))
    if value == 1:
        speed += 1
    elif value == -1:
        if speed > 3:
            speed -= 1


def save_grid():
    global grid
    json_string = json.dumps(grid.tolist())
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json_string)


def load_grid():
    global grid
    with open("data.json", "r", encoding="utf-8") as f:
        json_string = f.read()
        list = json.loads(json_string)
        grid = numpy.array(list)


if __name__ == "__main__":
    main()
