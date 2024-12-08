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
field_of_view = math.pi
distance_of_view = 250
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
    boids.append(Pointer(center_screen, 25, color, 0, 0.1))

special_boid = Pointer(center_screen, 30, red, 0, 0.1)

def detec_bodies(self, field_of_view, distance_of_view, *bodies):
    nearby_distances = []
    nearby_directions = []
    for body in bodies:
        # Calculate the distance between the two boids
        distance = math.dist(self.center, body.center)
        if distance <= distance_of_view:
            angle_of_view = math.atan2(self.center[1] - body.center[1], self.center[0] - body.center[0])
            # Normalize angles to the range [0, 2π)
            angle_of_view = angle_of_view % (2 * math.pi)
            left_limit = (self.direction - field_of_view / 2) % (2 * math.pi)
            right_limit = (self.direction + field_of_view / 2) % (2 * math.pi)
            # Check if angle_of_view is within the field of view, accounting for wrap-around
            if left_limit <= right_limit:
                in_view = left_limit <= angle_of_view <= right_limit
            else:
                in_view = angle_of_view >= left_limit or angle_of_view <= right_limit
            # If the body is in the field of view, add it to the nearby_bodies list
            if in_view:
                pygame.draw.line(screen, blue, self.center, body.center, 2)
                nearby_distances.append(distance)
                nearby_directions.append((self.center[0] - body.center[0], self.center[1] - body.center[1]))
    
    return nearby_distances, nearby_directions

def compute_weighted_direction(distances, directions):
    weighted_dir = np.array([0.0, 0.0])  # Start with a zero vector
    if distances:
        distances = np.array(distances)
        weights = 1 / (distances + 0.001)  # Higher weight for closer boids
        
        # Normalize weights to ensure their sum equals 1
        weights /= np.sum(weights)

        # Compute the weighted direction by summing the scaled vectors
        for dir, weight in zip(directions, weights):
            weighted_dir[0] += dir[0] * weight
            weighted_dir[1] += dir[1] * weight

    # Normalize the resulting direction vector
    magnitude = np.linalg.norm(weighted_dir)
    if magnitude > 0:  # Avoid dividing by zero
        weighted_dir /= magnitude

    return weighted_dir

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
            for i in range(1, len(boids)):
                angle = np.random.choice(angles_array)
                boids[i].direction = angle
            counter = 0

        # Resets the scene
        screen.fill(black)

        near_dis, near_dir = detec_bodies(special_boid, field_of_view, distance_of_view, *boids)
        weigh_dir = compute_weighted_direction(near_dis, near_dir)
        special_boid.direction = special_boid.direction*0.99 + 0.01*math.atan2(-weigh_dir[1], -weigh_dir[0])

        for boid in boids:
            boid.move_foward()
            boid.display()
        
        special_boid.move_foward()
        special_boid.display()

        # Display everything in the screen
        pygame.display.flip()
        counter += 1

if __name__ == '__main__':
    main()

    