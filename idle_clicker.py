import pygame
pygame.init()

# Color Library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)

# Game Settings
resolution = pygame.display.get_desktop_sizes()[0]
WIDTH, HEIGHT = resolution[0] // 2, resolution[1] // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Clicker Game')
background = black
framerate = 60
font = pygame.font.Font('freesansbold.ttf', 32)
timer = pygame.time.Clock()

# Game Variables
score = 0
button_1 = 1
button_2 = 2
button_3 = 3
button_4 = 4
button_5 = 5

def draw_task(color, y_coord, value):
    global score
    task = pygame.draw.rect(screen, white, [50, y_coord - 10, 180, 90])
    value_text = font.render(str(value), True, green)
    screen.blit(value_text, (135, y_coord + 20))
    return task

task_1 = None
task_2 = None

running = True
while running:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if task_1 and task_1.collidepoint(event.pos):
                score += 1
            if task_2 and task_2.collidepoint(event.pos):
                score += 2

    screen.fill(background)
    task_1 = draw_task(black, 70, button_1)
    
    if score >= 30:
        task_2 = draw_task(black, 170, button_2)
    else:
        task_2 = None

    
    

    display_score = font.render('Money: $'+str(round(score, 2)), True, white, black)
    screen.blit(display_score, (10, 5))
    pygame.display.flip()

pygame.quit()