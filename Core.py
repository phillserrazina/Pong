import pygame
import random
import time

pygame.init()

display_width = 800
display_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Window Setup
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()


# Call to draw the player's pad
def player(playerx, playery, playerw, playerh, color):
    pygame.draw.rect(screen, color, [playerx, playery, playerw, playerh])


# Call to draw the ball
def ball(ballx, bally, ballw, ballh, color):
    pygame.draw.rect(screen, color, [ballx, bally, ballw, ballh])


# Call to draw the cpu's pad
def cpu(cpux, cpuy, cpuw, cpuh, color):
    pygame.draw.rect(screen, color, [cpux, cpuy, cpuw, cpuh])


# Displays a custom message to the screen
def message_display(text, x, y, font, color):
    font = pygame.font.SysFont("comicsansms", font)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


# Pauses the game if player presses "P"
def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(black)
        message_display("Pause", display_width/2 - 140, display_height/2 - 100, 100, white)
        message_display("Press C to continue or Q to quit.", display_width/2 - 250, display_height/2 + 60, 35, white)
        pygame.display.update()
        clock.tick(5)


# Counts the score
def score(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Score: "+str(count), True, white)
    screen.blit(text, (0, 0))


# Call this function to start the game
def main():

    # Ball Info

    ball_startx = (display_width * 0.5)
    ball_starty = (display_height * 0.45)
    ball_speed_available = [-7, 7]
    ball_speedy = random.choice(ball_speed_available)
    ball_speedx = random.choice(ball_speed_available)
    ball_width = 25
    ball_height = 25

    # Player Info

    player_startx = (display_width * 0.05)
    player_starty = (display_height * 0.45)
    player_speed = 0
    player_width = 30
    player_height = 100

    # CPU Info

    cpu_x = (display_width * 0.90)
    cpu_y = (display_height * 0.45)
    cpu_speed = 0
    cpu_width = 30
    cpu_height = 100

    switch = [-1, 1]
    count = 0

    game_exit = False

    # Main game loop
    while not game_exit:

        # Handles the pressed keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed = -10

                elif event.key == pygame.K_DOWN:
                    player_speed = 10

                elif event.key == pygame.K_p:
                    pause()

                elif event.key == pygame.K_d:
                    ball_startx = (display_width * 0.5)
                    ball_starty = (display_height * 0.45)
                    ball_speedy = random.choice(switch) * ball_speedy
                    ball_speedx = random.choice(switch) * ball_speedy

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_speed = 0

        # CPU AI
        if ball_starty > cpu_y:
            cpu_speed = 7

        elif ball_starty < cpu_y:
            cpu_speed = -7

        elif ball_starty == cpu_y:
            cpu_speed = 0

        # Player, CPU and ball speed change
        player_starty += player_speed
        cpu_y += cpu_speed
        ball_starty += ball_speedy
        ball_startx += ball_speedx

        # Gives the screen a black background color, draws player, ball,
        # CPU and score
        screen.fill(black)
        player(player_startx, player_starty, player_width, player_height, white)
        ball(ball_startx, ball_starty, ball_width, ball_height, white)
        cpu(cpu_x, cpu_y, cpu_width, cpu_height, white)
        score(count)

        # This doesn't let the player go off boundaries
        if player_starty > display_height - player_height or player_starty < 0:
            player_speed = 0

        # This doesn't let the ball go off boundaries
        if ball_starty > display_height - ball_height or ball_starty < 0:
            ball_speedy = -ball_speedy

        # If the ball goes pass the player, the message "You lost" is shown
        # along with the final score
        if ball_startx < 0:
            message_display("You Lost", display_width * 0.25, display_height * 0.3, 100, white)
            message_display("Score: " + str(count), display_width * 0.46, display_height * 0.6, 25, red)
            pygame.display.update()
            time.sleep(1)

            main()

        # If the ball goes pass the CPU, it returns to it's original position
        # and the player's score increases by 1
        if ball_startx > display_width - ball_width - 20:
            time.sleep(0.1)
            ball_startx = (display_width * 0.5)
            ball_starty = (display_height * 0.45)
            ball_speedy = random.choice(switch) * ball_speedy
            ball_speedx = random.choice(switch) * ball_speedy
            count += 1

        # This tells the computer what should happen if the ball hits the player's pad
        if player_starty + player_height > ball_starty and ball_starty + ball_height > player_starty:

            if 0 < ball_startx < player_startx + player_width - 10:
                message_display("You Lost", display_width * 0.25, display_height * 0.3, 100, white)
                message_display("Score: " + str(count), display_width * 0.46, display_height * 0.6, 25, red)
                pygame.display.update()
                time.sleep(1)

                main()

            elif ball_startx < player_startx + player_width:
                ball_speedx = -ball_speedx
                ball_speedy = random.choice(switch) * ball_speedy
                ball_speedx += 2
                ball_speedy *= 1.05

        # This tells the computer what should happen if the ball hits the CPU's pad
        if cpu_height + cpu_y > ball_starty and ball_starty + ball_height > cpu_y:

            if display_width > ball_startx > cpu_x - cpu_width + 10:
                time.sleep(0.1)
                ball_startx = (display_width * 0.5)
                ball_starty = (display_height * 0.45)
                ball_speedy = random.choice(switch) * ball_speedy
                ball_speedx = random.choice(switch) * ball_speedy
                count += 1

            elif ball_startx > cpu_x - cpu_width:
                ball_speedx = -ball_speedx
                ball_speedy = random.choice(switch) * ball_speedy

        # Updates the screen 30 times per second
        pygame.display.update()
        clock.tick(30)

main()
pygame.quit()
quit()
