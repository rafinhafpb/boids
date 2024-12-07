import pygame
import numpy as np
import math
import sys
from colors import *
from shapes import Circle, Dot, Triangle, Pointer
from dynamics import rotate_vector

# Define the screen size
screen_size = screen_width, screen_height = 1080, 720

# Define fps limit
FPS = 30

# Modifiable variables #
nb_boids = 20
constants = f, zeta, r = [1, 1, 2]    # Define control parameters for animation
# ----------------------- #

# Define cursor type
cursor = pygame.cursors.diamond

# Setting display and getting the surface object
pygame.init()
pygame.mouse.set_cursor(cursor)
screen = pygame.display.set_mode(screen_size)
center_screen = np.array(screen.get_size())/2
clock = pygame.time.Clock()
boids = []

for _ in range(nb_boids):
    color = random_color
    boids.append(Pointer(center_screen, 20, color, 0, [0.1, 0.1]))

def main():
    angles_array = np.linspace(0, 2*np.pi, 100)
    angle = np.random.choice(angles_array)
    counter = 0
    #Limit FPS
    clock.tick(FPS)

    while(True):

        # Condition to clase the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        if counter == 5000:
            for boid in boids:
                angle = np.random.choice(angles_array)
                boid.direction = angle
            counter = 0
        
        # Resets the scene
        screen.fill(black)

        for boid in boids:
            boid.move_foward()
            boid.display()

        # Display everything in the screen
        pygame.display.flip()
        counter += 1

if __name__ == '__main__':
    main()

    