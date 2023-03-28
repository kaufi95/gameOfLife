import pygame

BLACK = (0, 0, 0)
WHITE = (100, 100, 100)
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 720


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
                SystemExit()

        pygame.display.update()


def drawGrid():
    block_size = 10
    for x in range(WINDOW_WIDTH // block_size):
        for y in range(WINDOW_HEIGHT // block_size):
            rect = pygame.Rect(x*block_size, y*block_size,
                               block_size, block_size)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


if __name__ == "__main__":
    main()
