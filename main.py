import pygame
import random
import os

# Initialize the pygame module
pygame.init()

pygame.mixer.init()

# Canvas Width and height
screen_width = 900
screen_height = 600
# Making of Game Window
gameWindow = pygame.display.set_mode((screen_width, screen_height))

bg_img = pygame.image.load("images/bg.jpg")
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height)).convert_alpha()
welcome_img = pygame.image.load("images/welcome.jpg")
welcome_img = pygame.transform.scale(welcome_img, (screen_width, screen_height)).convert_alpha()
gameover_img = pygame.image.load("images/gameover.jpg")
gameover_img = pygame.transform.scale(gameover_img, (screen_width, screen_height)).convert_alpha()
apple_img = pygame.image.load("images/apple.png")
apple_img = pygame.transform.scale(apple_img, (33, 33)).convert_alpha()

# Title Caption for game window
pygame.display.set_caption("Snake Game, Developed by Shery")
pygame.display.update()

# Color define
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
green = (0, 255, 0)

# This function is used to count the time 
clock = pygame.time.Clock()

# To set the form to write in game window
font = pygame.font.SysFont(None, 45)

# Set the text in Game window
def screenText(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Plotting of Snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Welcome Screen
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(blue)
        gameWindow.blit(welcome_img, (0, 0))
        screenText("Welcome to Snakes", white, 260, 250)
        screenText("Press Space Bar To Play", white, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('music/back.mp3')
                    pygame.mixer.music.play()
                    gameLoop()
        pygame.display.update()
        clock.tick(60)

# Game Loop
def gameLoop():
    # Game Specific Variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 25
    apple_x = random.randint(20, int(screen_width / 2))
    apple_y = random.randint(20, int(screen_height / 2))
    # Define the initial velocity of the snake
    velocity_x = 5
    velocity_y = 0
    init_velocity = 5 # Speed of the Snake
    score = 0 # Initial Score
    fps = 60 # Frame Per Rate

    # To increment in the length of snake  
    snk_list = []
    snk_len = 1

    # Check if the file exists or not
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    # Read the highscore
    with open("highscore.txt", "r") as f:
        highscore = f.read()
        highscore = int(highscore)

    while not exit_game:
        # What happens when the game over variable is true
        if game_over:
            # Writing the highscore
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            # What happens when the game is over
            gameWindow.fill(black)
            gameWindow.blit(gameover_img, (0, 0))
            screenText("Press Enter To Continue...", green, 200, 380)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        # Game Logic
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                # Tracking the Keys of the Keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - apple_x) < 16 and abs(snake_y - apple_y) < 16:
                score += 10
                snk_len += 3
                if score > highscore:
                    highscore = score
                apple_x = random.randint(20, int(screen_width / 2))
                apple_y = random.randint(20, int(screen_height / 2))

            gameWindow.fill(black)
            gameWindow.blit(bg_img, (0, 0))

            # Making the head of snake at the start of the game 
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            screenText(f"Score: {score}  ----  Highscore: {highscore}", blue, 5, 5)

            # Logic for the boundary and when the snake bites its body
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('music/gameover.mp3')
                pygame.mixer.music.play()
            if snake_x > screen_width or snake_x < 0 or snake_y > screen_height or snake_y < 0:
                game_over = True
                pygame.mixer.music.load('music/gameover.mp3')
                pygame.mixer.music.play()

            # Cutting the head when the length of the snake is greater than the snk_list
            if len(snk_list) > snk_len:
                del snk_list[0]

            plot_snake(gameWindow, white, snk_list, snake_size)
            gameWindow.blit(apple_img, (apple_x, apple_y))

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

pygame.mixer.music.load('music/welcome.mp3')
pygame.mixer.music.play()
welcome()
