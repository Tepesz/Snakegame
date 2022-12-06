# This is a version of the popular game Snake that we programmed using pygame
# First, import the necessary modules. This game runs on pygame - if you are having difficulty loading it, try adding !pip3 install pygame as a new first line
import pygame
from enum import Enum
import random
import time

# Create a class that includes the directions in which the snake will later move
class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

# We store a preset speed in the variable "speed"
speed = 10

# We define variables for the window in which the game will be played. This makes it easier to use later on
window_width = 1080
window_height = 720

# We run pygame and create a window with the name "Snakegame" using the .set_caption and display.set_mode commands
pygame.init()
pygame.display.set_caption("Snakegame")
window = pygame.display.set_mode((window_width, window_height))

# We create an object to control the fps of our game using .time.Clock()
refresh_controller = pygame.time.Clock()


# We define the initial position of our snake's head and body. These will be stored in a list
snake_position = [250, 250]
snake_body = [[250, 250],
              [240, 250],
              [230, 250]]

# We define the first position that the food spawns in
food_position = [100, 100]

# We save the number 20 in the variable scale, which we will use often in the code
scale = 20

# We set the default direction to right
direction = Direction.RIGHT

# The score is defined as a global variable and set it to 0
global score
score = 0

# Now that the prerequisites are defined, we can start to program the functions that the game will run on
# We begin by adding a function handle_keys that lets the player give an input using the arrow keys which outputs the new direction the snake should head in
def handle_keys(direction):
    new_direction = direction
    # We do this using the .KEYDOWN command, which detects if a button on the keyboard of the player is pressed down
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        # If the key for the corresponding direction is pressed down and the snake won't do a 180 degree turn, the direction of the snake is changed to the input
        if event.key == pygame.K_UP and direction != Direction.DOWN:
            new_direction = Direction.UP
        if event.key == pygame.K_DOWN and direction != Direction.UP:
            new_direction = Direction.DOWN
        if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
            new_direction = Direction.RIGHT
        if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
            new_direction = Direction.LEFT
    return new_direction

# Now we have to actually make the snake move towards this direction. We update the X or Y coordinate of snake_position respectively by 20 pixels, and let the snake keep on moving in the new direction until a change is entered
def move_snake(direction):
    if direction == Direction.UP:
        snake_position[1] -= scale
    if direction == Direction.DOWN:
        snake_position[1] += scale
    if direction == Direction.LEFT:
        snake_position[0] -= scale
    if direction == Direction.RIGHT:
        snake_position[0] += scale
    # We also have to let the snake grow - we do this by adding a new part at the end of the list that is snake.body . We will change the growing mechanism later.
    snake_body.insert(0, list(snake_position))

# Next, we have to generate the objective of the game, the food that the snake consumes.
def generate_new_food():
    # We do this by randomly generating two X and Y coordinates at which the food will spawn if the function is triggered
    food_position[0] = random.randint(5, ((window_width - 2) // scale) * scale)
    food_position[1] = random.randint(5, ((window_height - 2) // scale) * scale)

# Now we have to define what happens if the snake eats the food.
def get_food():
    global score
    # Using an if statement, we check if the position (X/Y coordinates) of the snake's head corresponds to the position of the food (within 20 pixels for accuracy)
    if abs(snake_position[0] - food_position[0]) < 20 and abs(snake_position[1] - food_position[1]) < 20:
        # If the statement is true, add 10 points to the score and generate new food using the function we created earlier
        score += 10
        generate_new_food()
    # If not, remove the last part of the snake's body using .pop - this way the snake appears to be moving without growing.
    # In essence, a new part of the snake is generated every tick at the end of the body, but will always be removed if the snake hasn't consumed a new item of food
    else:
        snake_body.pop()

# We have to paint the game and give the snake and food shapes - black for the background, green circles for the snake, red rectangels for the food
def repaint():
    window.fill(pygame.Color(0, 0, 0))
    for body in snake_body:
        pygame.draw.circle(window, pygame.Color(0, 255, 0), (body[0], body[1]), scale / 2)
    pygame.draw.rect(window, pygame.Color(255, 0, 0),
                     pygame.Rect(food_position[0] - scale / 2, food_position[1] - scale / 2, scale, scale))


#when the snake dies, we want a game over message to appear on the screen
def game_over_message():
  #we first define in which font and color the score will be displayed
    font = pygame.font.SysFont("Arial", scale * 3)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    rect.midtop = (window_width / 2, window_height / 2)
    window.blit(render, rect)
    pygame.display.flip()
    #before quitting the game, we want the score to be on the screen for 5 seconds
    time.sleep(5)
    pygame.quit
    exit(0)

#now we need to define, in which cases the snake dies
#the snake dies when she either touches herself or the edges of the game window
def game_over():
    if snake_position[0] < 0 or snake_position[0] > window_width - 10:
        game_over_message()
    if snake_position[1] < 0 or snake_position[1] > window_height - 10:
        game_over_message()
    for blob in snake_body[1:]:
        if snake_position[0] == blob[0] and snake_position[1] == blob[1]:
            game_over_message()

#now we need to define a function that defines in what color and what font the score gets displayed
def paint_hud():
    font = pygame.font.SysFont("Arial", scale * 2)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    window.blit(render, rect)
    pygame.display.flip()

#to keep the game running, we need to store all our defined functions in a game loop, so that all the functions keep running
def game_loop():
    direction = Direction.RIGHT
    while True:
        direction = handle_keys(direction)
        move_snake(direction)
        get_food()
        repaint()
        game_over()
        paint_hud()
        pygame.display.update()
        refresh_controller.tick()
        time.sleep(0.5)

#we need to make sure, that the game loop function, that keeps the game running will be called up
if __name__ == "__main__":
    game_loop()