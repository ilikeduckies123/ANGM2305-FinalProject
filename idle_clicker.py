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
manager_income_timer = 0

#draw buttons function
buttons = [
    {"value": 1, "name": 'Manager 1', "unlock_cost": 10,
     "unlocked": True, "manager_cost": 100, "manager_count": 0},
    {"value": 2, "name": 'Manager 2', "unlock_cost": 50,
     "unlocked": False, "manager_cost": 500, "manager_count": 0},
    {"value": 5, "name": 'Manager 3', "unlock_cost": 100,
     "unlocked": False, "manager_cost": 1000, "manager_count": 0},
    {"value": 10, "name": 'Manager 4', "unlock_cost": 500,
     "unlocked": False, "manager_cost": 5000, "manager_count": 0},
    {"value": 100, "name": 'Manager 5', "unlock_cost": 1000,
     "unlocked": False, "manager_cost": 10000, "manager_count": 0},
]

def draw_task(y_coord, btn):
    if btn["unlocked"]:
        task = pygame.draw.rect(screen, white, [50, y_coord - 10, 220, 100])
        value_text = font.render(str(btn["value"]), True, green)
        screen.blit(value_text, (135, y_coord + 20))
    else:
        task = pygame.draw.rect(screen, red, [50, y_coord - 10, 220, 90])
        value_text = font.render(f"Unlock: {btn['unlock_cost']}", True, white)
        screen.blit(value_text, (60, y_coord + 20))
    return task

def draw_buttons(color, y_coord, name, manager_cost, manager_count):
    # Cost Button
    cost_button = pygame.draw.rect(screen, color, [350, y_coord, 180, 40])
    name_text = font.render(str(name), True, black)
    screen.blit(name_text, name_text.get_rect(center=cost_button.center))

    manager_button = pygame.draw.rect(screen, color, [350, y_coord + 40, 160, 40])
    manager_text = font.render(f"{manager_cost} ({manager_count})", True, black)
    screen.blit(manager_text, manager_text.get_rect(center=manager_button.center))
                    
    return cost_button, manager_button

task_rects = []
button_rects = []

running = True
while running:
    dt = timer.tick(60) / 1000
    manager_income_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (_, manager_button) in enumerate(button_rects):
                if manager_button and manager_button.collidepoint(event.pos):
                    if score >= buttons[i]["manager_cost"]:
                        score -= buttons[i]["manager_cost"]
                        buttons[i]["manager_count"] += 1
                        buttons[i]["manager_cost"] = int(buttons[i]["manager_cost"] * 1.2)

            for i, task in enumerate(task_rects):
                if task and task.collidepoint(event.pos):
                    if buttons[i]["unlocked"]:
                        score += buttons[i]["value"]
                    else:
                        if score >= buttons[i]["unlock_cost"]:
                            score -= buttons[i]["unlock_cost"]
                            buttons[i]["unlocked"] = True

    if manager_income_timer >= 0.25:
        for btn in buttons:
            if btn["manager_count"] > 0:
                score += btn["value"] * btn["manager_count"]
        manager_income_timer = 0

    screen.fill(background)

    task_rects = []
    button_rects = []
    start_y = 70
    spacing = 140

    for i, btn in enumerate(buttons):
        y = start_y + i * spacing
        task_rect = draw_task(y, btn)
        cost_button, manager_button = draw_buttons(white, y, btn["name"],
                                                    btn["manager_cost"],
                                                    btn["manager_count"])
        task_rects.append(task_rect)
        button_rects.append((cost_button, manager_button))

    display_score = font.render('Money: $'+str(round(score, 2)), True, white, black)
    screen.blit(display_score, (47, 15))
    buy_managers = font.render("Buy Managers:", True, white)
    screen.blit(buy_managers, (347, 15))
    pygame.display.flip()

pygame.quit()