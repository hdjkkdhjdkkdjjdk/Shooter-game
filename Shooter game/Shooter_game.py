import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the window to be full screen
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Player
player_size = 50
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]

# Enemies
enemy_size_range = (20, 60)  # Range of enemy sizes
enemy_speed = 5
enemy_list = []

# Bullets
bullet_size = 5
bullet_speed = 10
bullet_list = []

# Score
score = 0

# Function to create enemies
def create_enemies():
    delay = random.random()
    if len(enemy_list) < 5 and delay < 0.05:
        enemy_size = random.randint(*enemy_size_range)
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos, enemy_size])

# Function to move enemies
def move_enemies():
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)

# Function to draw enemies
def draw_enemies():
    for enemy_pos in enemy_list:
        pygame.draw.rect(window, RED, (enemy_pos[0], enemy_pos[1], enemy_pos[2], enemy_pos[2]))

# Function to move bullets
def move_bullets():
    for bullet_pos in bullet_list:
        if bullet_pos[1] > 0:
            bullet_pos[1] -= bullet_speed
        else:
            bullet_list.remove(bullet_pos)

# Function to draw bullets
def draw_bullets():
    for bullet_pos in bullet_list:
        pygame.draw.rect(window, GREEN, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))

# Function to detect collision between bullets and enemies
def collision_detection():
    global score
    for enemy_pos in enemy_list:
        for bullet_pos in bullet_list:
            if bullet_pos[1] <= enemy_pos[1] + enemy_pos[2] and \
               bullet_pos[0] >= enemy_pos[0] and \
               bullet_pos[0] <= enemy_pos[0] + enemy_pos[2]:
                enemy_list.remove(enemy_pos)
                bullet_list.remove(bullet_pos)
                score += 1  # Increase score when enemy is hit
                break

# Function to display the score
def display_score():
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, [10, 10])

# Function to end the game if the player collides with an enemy
def game_over():
    game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
    window.blit(game_over_text, [WIDTH // 2 - 200, HEIGHT // 2 - 50])
    pygame.display.update()

    # Wait for the player to press 'R' to restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main function
def main():
    global score
    score = 0  # Reset score at the start of the game
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    bullet_pos = [player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1]]
                    bullet_list.append(bullet_pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 5
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += 5

        window.fill(WHITE)
        create_enemies()
        move_enemies()
        draw_enemies()
        move_bullets()
        draw_bullets()
        collision_detection()
        display_score()

        pygame.draw.rect(window, BLACK, (player_pos[0], player_pos[1], player_size, player_size))

        # Check for collision between player and enemies
        for enemy_pos in enemy_list:
            if enemy_pos[1] + enemy_pos[2] >= player_pos[1] and \
               enemy_pos[0] + enemy_pos[2] >= player_pos[0] and \
               enemy_pos[0] <= player_pos[0] + player_size:
                game_over()

        pygame.display.update()
        clock.tick(30)  # Set the frame rate to 30 frames per second

# Start the game
if __name__ == "__main__":
    main()

