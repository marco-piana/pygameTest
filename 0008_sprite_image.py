# Import the pygame module
import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACK_COLOR = (0, 51, 51)
ERBA_HEIGHT = 13
TERRA_HEIGHT = 30


def init_erba(screen_current):
    surf_erba = pygame.Surface((SCREEN_WIDTH, ERBA_HEIGHT))
    surf_erba.fill((29, 240, 36))
    screen_current.blit(surf_erba, (0, SCREEN_HEIGHT - ERBA_HEIGHT - TERRA_HEIGHT))
    return surf_erba


def init_terra(screen_current):
    surf_terra = pygame.Surface((SCREEN_WIDTH, TERRA_HEIGHT))
    surf_terra.fill((153, 76, 0))
    screen_current.blit(surf_terra, (0, SCREEN_HEIGHT - TERRA_HEIGHT))
    return surf_terra


# Preparare il tabellone
def init_screen():
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    base_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Fill the screen
    base_screen.fill(BACK_COLOR)

    init_terra(base_screen)
    init_erba(base_screen)
    # Create a surface and pass in a tuple containing its length and width

    return base_screen


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("img/spacenav2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.killed = False

    # Move the sprite based on user keypresses
    def update(self, keys):
        if keys[K_UP]:
            self.rect.move_ip(0, -1)
        if keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT-ERBA_HEIGHT-TERRA_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT-ERBA_HEIGHT-TERRA_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("img/arrow1.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("img/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Prima prova di videogioco fatto con Marco
if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    screen = init_screen()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    clouds_up = pygame.sprite.Group()
    clouds_down = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Create a custom event for adding a new enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 500)

    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 500)

    pygame.display.flip()

    # Variable to keep the main loop running
    running = True

    # Main loop
    while running:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                print("Ho premuto un tasto...")

                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    print("In questo momento esco dopo aver premuto ESC")
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                print("In questo momento esco eseguento il quit!")
                running = False

            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)

            # Add a new cloud?
            elif event.type == ADDCLOUD:
                print("Arriva una nuvola...")
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                cloud_type = random.randint(0, 1)
                if cloud_type == 0:
                    clouds_up.add(new_cloud)
                else:
                    clouds_down.add(new_cloud)

        screen = init_screen()

        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Nuvole che passano sotto al player
        for cloud in clouds_down:
            cloud.update()
            screen.blit(cloud.surf, cloud.rect)

        #NOTE: in base all'ordine di blit si stabilisce l'ordine di visualizzazione
        for entity in all_sprites:
            entity.update(pressed_keys)
            screen.blit(entity.surf, entity.rect)

            # Check if any enemies have collided with the player
            if pygame.sprite.spritecollideany(player, enemies):
                # If so, then remove the player and stop the loop
                player.kill()
                running = False

        for enemy in enemies:
            enemy.update()
            screen.blit(enemy.surf, enemy.rect)

        # Nuvole che passano sopra il player
        for cloud in clouds_down:
            cloud.update()
            screen.blit(cloud.surf, cloud.rect)

        pygame.display.flip()