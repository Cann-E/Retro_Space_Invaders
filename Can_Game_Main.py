from pygame import *
init()
import Can_Game_Functions

# Plane position and speed
plane_x, plane_y = 100, 300  # Initial position of the plane
plane_width, plane_height = 100, 75  # Size of the plane
speed = 10

# Screen setup
WIDTH, HEIGHT = 1200, 800  # Screen dimensions
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Cans Game")
clock = time.Clock()

# Load assets
background = transform.scale(image.load("Images/lake.jpg"), (WIDTH, HEIGHT))
plane = transform.scale(image.load("Images/plane.png").convert_alpha(), (plane_width, plane_height))

# Load sound
mixer.init()
sound_all = mixer.Sound("Sounds/Plane_Sound_can.wav")

# Assign a channel for the sound
channel = mixer.Channel(0)  
# <----------Game Loop-------------->
run = True
while run:
    # Draw the background
    screen.blit(background, (0, 0))
    # Draw the plane
    screen.blit(plane, (plane_x, plane_y))

    for evnt in event.get():
        if evnt.type == QUIT:
            run = False  

    # Handle key presses for movement
    keys = key.get_pressed()

    if (
        keys[K_LEFT] and plane_x > 0 or
        keys[K_UP] and plane_y > 0 or
        keys[K_RIGHT] and plane_x < WIDTH - plane_width or
        keys[K_DOWN] and plane_y < HEIGHT - plane_height
    ):
        # Start playing the sound if it's not already playing
        if not channel.get_busy():
            channel.play(sound_all, loops=-1)  

        # Move the plane
        if keys[K_LEFT] and plane_x > 0:
            plane_x -= speed
        if keys[K_UP] and plane_y > 0:
            plane_y -= speed
        if keys[K_RIGHT] and plane_x < WIDTH - plane_width:
            plane_x += speed
        if keys[K_DOWN] and plane_y < HEIGHT - plane_height:
            plane_y += speed
    else:
        # Stop the sound when no movement keys are pressed
        if channel.get_busy():
            channel.stop()

    # Update the display
    display.update()
    clock.tick(60)

quit()
