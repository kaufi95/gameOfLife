import pygame

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

WINDOW_HEIGHT = 480
WINDOW_WIDTH = 720

BLOCKSIZE = 10
GRID = [[0 for x in range(WINDOW_HEIGHT // BLOCKSIZE)]
        for y in range(WINDOW_WIDTH // BLOCKSIZE)]


def main():

    global SCREEN, CLOCK

    pygame.init()

    pygame.display.set_caption("Game Of Life")

    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    running = True

    while running:
        drawGrid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event.pos)
                    GRID[event.pos[0] // BLOCKSIZE][event.pos[1] // BLOCKSIZE] = 1

        pygame.display.update()


def drawGrid():
    for x in range(GRID.__len__()):
        for y in range(GRID[x].__len__()):
            if GRID[x][y] == 1:
                rect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE,
                                   BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(SCREEN, YELLOW, rect)
            else:
                rect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE,
                                   BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(SCREEN, GRAY, rect, 1)


if __name__ == "__main__":
    main()
