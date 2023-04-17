import pygame
import numpy as np

# Initialisierung von Pygame
pygame.init()

# Größe des Gitterfelds
width, height = 640, 480
cell_size = 10

# Erstellung des Fensters
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Erstellung des Gitterfelds
rows = height // cell_size
cols = width // cell_size
grid = np.zeros((rows, cols))

# Funktion zum Aktualisieren des Gitterfelds
def update_grid(grid):
    new_grid = np.copy(grid)
    for i in range(rows):
        for j in range(cols):
            # Berechnung der Anzahl von Nachbarn
            neighbors = grid[(i-1) % rows][(j-1) % cols] + \
                        grid[(i-1) % rows][j] + \
                        grid[(i-1) % rows][(j+1) % cols] + \
                        grid[i][(j-1) % cols] + \
                        grid[i][(j+1) % cols] + \
                        grid[(i+1) % rows][(j-1) % cols] + \
                        grid[(i+1) % rows][j] + \
                        grid[(i+1) % rows][(j+1) % cols]
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

# Funktion zum Zeichnen des Gitterfelds
def draw_grid(grid):
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                pygame.draw.rect(screen, WHITE, (j*cell_size, i*cell_size, cell_size, cell_size), 1)
            else:
                pygame.draw.rect(screen, BLACK, (j*cell_size, i*cell_size, cell_size, cell_size), 2)

# Funktion zum Anzeigen des Menüs
def draw_menu():
    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, WHITE)
    stop_text = font.render("Stop", True, WHITE)
    slower_text = font.render("Slower", True, WHITE)
    faster_text = font.render("Faster", True, WHITE)
    pygame.draw.rect(screen, WHITE, (0, height//2, width, height//2))
    screen.blit(start_text, (20, height//2 + 20))
    screen.blit(stop_text, (20, height//2 + 60))
    screen.blit(slower_text, (width//2 - 70, height//2 + 20))
    screen.blit(faster_text, (width//2 - 70, height//2 + 60))

#Hauptprogramm
running = False
clock = pygame.time.Clock()
generation = 0
speed = 10

#Schleife für die Ereignisverarbeitung
while True:
# Ereignisse abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if event.type == pygame.MOUSEBUTTONDOWN:
    # Überprüfen, ob der Button "Start" geklickt wurde
        if width//2 - 70 < event.pos[0] < width//2 + 70 and height//2 + 20 < event.pos[1] < height//2 + 50:
            running = True
        # Überprüfen, ob der Button "Stop" geklickt wurde
        if width//2 - 70 < event.pos[0] < width//2 + 70 and height//2 + 60 < event.pos[1] < height//2 + 90:
            running = False
        # Überprüfen, ob der Button "Slower" geklickt wurde
        if 20 < event.pos[0] < 120 and height//2 + 20 < event.pos[1] < height//2 + 50:
            speed += 5
        # Überprüfen, ob der Button "Faster" geklickt wurde
        if 20 < event.pos[0] < 120 and height//2 + 60 < event.pos[1] < height//2 + 90:
            speed -= 5    

    # Hintergrund zeichnen
    screen.fill(BLACK)

    # Menü zeichnen
    draw_menu()

    # Gitterfeld aktualisieren und zeichnen
    if running:
        grid = update_grid(grid)
        generation += 1
    
    draw_grid(grid)

    # Generation und Geschwindigkeit anzeigen
    font = pygame.font.Font(None, 24)
    gen_text = font.render("Generation: " + str(generation), True, WHITE)
    speed_text = font.render("Speed: " + str(speed), True, WHITE)
    screen.blit(gen_text, (20, 20))
    screen.blit(speed_text, (width - 100, 20))

    # Bildschirm aktualisieren
    pygame.display.update()

    # Zeitverzögerung
    clock.tick(speed)