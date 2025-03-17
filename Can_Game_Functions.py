import pygame
import random

# Initialize pygame
pygame.init()

# Screen Constants
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load assets
background = pygame.transform.scale(pygame.image.load("Images/lake.jpg"), (WIDTH, HEIGHT))
explosion_img = pygame.transform.scale(pygame.image.load("Images/explosion.png"), (50, 50))  # Explosion effect

# Load sound
pygame.mixer.init()
sound_shoot = pygame.mixer.Sound("Sounds/Shoot.wav")
sound_explosion = pygame.mixer.Sound("Sounds/Explosion.wav")

# Colors
WHITE = (255, 255, 255)

# 🚀 Plane Class
class Plane:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.width, self.height = 100, 75
        self.image = pygame.transform.scale(pygame.image.load("Images/plane.png").convert_alpha(), (self.width, self.height))
        self.bullets = []  # Stores bullets

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.speed

    def shoot(self):
        bullet = Bullet(self.x + self.width, self.y + self.height // 2, 10, "up")  # Shoots right
        self.bullets.append(bullet)
        sound_shoot.play()  # Play shooting sound

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.move()
            bullet.draw()


# 👾 Alien Ship Class (Shoots Left)
class AlienShip:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 1  # Moves right initially
        self.width, self.height = 100, 75
        self.image = pygame.transform.scale(pygame.image.load("Images/alien_ship.png").convert_alpha(), (self.width, self.height))
        self.bullets = []  # Stores bullets
        self.shoot_cooldown = 0  # Cooldown for auto-shooting

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x + self.width >= WIDTH:
            self.direction *= -1  # Change movement direction

        # Auto-Shoot bullets every 60 frames (~1 sec)
        if self.shoot_cooldown == 0:
            self.shoot()
            self.shoot_cooldown = 60  # Reset cooldown
        else:
            self.shoot_cooldown -= 1  # Decrease cooldown

    def shoot(self):
        bullet = Bullet(self.x, self.y + self.height // 2, 10, "down")  # Shoots left
        self.bullets.append(bullet)
        sound_shoot.play()  # Play shooting sound

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.move()
            bullet.draw()


# 💥 Bullet Class (For both Plane & Alien)
class Bullet:
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # "up" for plane, "down" for alien
        self.width, self.height = 5, 15  # Make bullets vertical
        self.color = (255, 255, 255)  # White bullets

    def move(self):
        if self.direction == "up":
            self.y -= self.speed  # Plane bullets go UP
        elif self.direction == "down":
            self.y += self.speed  # Alien bullets go DOWN

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


# 🎆 Explosion Effect
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 30  # Explosion duration

    def draw(self):
        if self.timer > 0:
            screen.blit(explosion_img, (self.x, self.y))
            self.timer -= 1


# 🔧 Function to Draw Background
def draw_background():
    screen.blit(background, (0, 0))


# 🔥 Function to Check Bullet Collision
def check_collision(bullets, target, explosions):
    for bullet in bullets:
        if target.x < bullet.x < target.x + target.width and target.y < bullet.y < target.y + target.height:
            explosions.append(Explosion(target.x, target.y))  # Create explosion
            sound_explosion.play()  # Play explosion sound
            bullets.remove(bullet)  # Remove bullet
            return True
    return False
