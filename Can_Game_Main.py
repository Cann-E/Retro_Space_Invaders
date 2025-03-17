import pygame
from Can_Game_Functions import Plane, AlienShip, Explosion, draw_background, check_collision, screen

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Create objects
plane = Plane(100, 300, 10)
alien_ship = AlienShip(500, 50, 5)
explosions = []  # Stores explosion effects

# Game Loop
run = True
while run:
    draw_background()  # Draw background
    plane.draw()       # Draw plane
    alien_ship.draw()  # Draw alien ship

    # Draw explosions
    for explosion in explosions:
        explosion.draw()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Plane shoots when space is pressed
                plane.shoot()

    # Move objects
    keys = pygame.key.get_pressed()
    plane.move(keys)
    alien_ship.move()

    # Check for collisions (Bullets hitting targets)
    if check_collision(plane.bullets[:], alien_ship, explosions):  # Use a copy to avoid modifying list during iteration
        print("Alien ship hit!")
    if check_collision(alien_ship.bullets[:], plane, explosions):
        print("Plane hit!")

    # Update display
    pygame.display.update()
    clock.tick(60)  # Limit frame rate

pygame.quit()
