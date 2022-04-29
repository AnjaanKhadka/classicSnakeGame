import pygame
import random

pygame.init()
offset = 30
width, height = 400, 400 + offset
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Classic Snake Game")
pygame.display.update()
unit = 10
font = pygame.font.SysFont('Arial', 15)
text = font.render("score", True, (255, 255, 255))
clock = pygame.time.Clock()
blocks_x = width / unit
left, right, up, down = 0, 1, 2, 3


def background():
    screen.fill((35, 35, 35))
    pygame.draw.rect(screen, (135, 135, 135), ((0, 0), (width, offset)))


def draw_unit(x, y, col):
    x, y = int(x), int(y)
    pygame.draw.rect(screen, col, ((x * unit + 1, y * unit + offset + 1), (unit - 2, unit - 2)))


def draw_bold_unit(x, y, ):
    x, y = int(x), int(y)
    pygame.draw.rect(screen, (255, 255, 255), ((x * unit, y * unit + offset), (unit, unit)))


def draw_snake(snake, food):
    for i in range(len(snake)-1):
        x = snake[i] % blocks_x
        y = snake[i] / blocks_x
        for j in range(len(food) - 1):
            if food[j] == snake[i]:
                draw_bold_unit(x, y)
        draw_unit(x, y, (255, 255, 255))
    draw_unit(snake[i+1] % blocks_x, snake[i+1] / blocks_x, (0, 0, 255))

def draw_food(snake):
    for i in range(len(snake)):
        x = snake[i] % blocks_x
        y = snake[i] / blocks_x
        draw_unit(x, y, (255, 0, 0))


def generate_food(food, snake):
    done = False
    while not done:
        done=True
        pos = random.randint(0, (blocks_x)**2-1)
        for i in snake:
            if pos==i: done=False
    food.append(pos)
    return food


def is_right_possible(snake):
    ret = True
    if (snake[len(snake) - 1] + 1) % blocks_x == 0:
        ret = False
    return ret


def is_left_possible(snake):
    ret = True
    if snake[len(snake) - 1] % blocks_x == 0:
        ret = False
    return ret


def is_up_possible(snake):
    ret = True
    if snake[len(snake) - 1] < blocks_x:
        ret = False
    return ret


def is_down_possible(snake):
    ret = True
    if snake[len(snake) - 1] > blocks_x * (blocks_x - 1):
        ret = False
    return ret


def is_over(snake):
    for i in range(len(snake) - 1):
        if snake[len(snake) - 1] == snake[i]:
            return True
    return False


def move_right(snake):
    snake.append(snake[len(snake) - 1] + 1)
    return snake


def move_left(snake):
    snake.append(snake[len(snake) - 1] - 1)
    return snake


def move_up(snake):
    snake.append(snake[len(snake) - 1] - blocks_x)
    return snake


def move_down(snake):
    snake.append(snake[len(snake) - 1] + blocks_x)
    return snake


food = []
snake = [11, 12, 13]
food = generate_food(food,snake)
running = True
movement = right
score=0
while running:
    text = font.render("score         "+str(score), True, (255, 255, 255))
    background()
    screen.blit(text,(int(width/2)-40,5))
    temp_movement = movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and movement != right:
                temp_movement = left
            elif event.key == pygame.K_RIGHT and movement != left:
                temp_movement = right
            elif event.key == pygame.K_UP and movement != down:
                temp_movement = up
            elif event.key == pygame.K_DOWN and movement != up:
                temp_movement = down
    movement = temp_movement
    no_remove = False
    for i in range(len(food)):
        if food[i] == snake[len(snake) - 1]:
            food = generate_food(food, snake)
            score+=1
        if food[i] == snake[0]:
            no_remove = True
            food.remove(food[i])
            break

    if not is_over(snake):
        if movement == left and is_left_possible(snake):
            snake = move_left(snake)
            if not no_remove: snake.remove(snake[0])
        elif movement == up and is_up_possible(snake):
            snake = move_up(snake)
            if not no_remove: snake.remove(snake[0])
        elif movement == down and is_down_possible(snake):
            snake = move_down(snake)
            if not no_remove: snake.remove(snake[0])
        elif movement == right and is_right_possible(snake):
            snake = move_right(snake)
            if not no_remove: snake.remove(snake[0])
        else:
            running = False
    else:
        running = False
    draw_food(food)
    draw_snake(snake, food)
    pygame.display.update()
    pygame.time.delay(120)
