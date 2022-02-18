# Import the pygame module
import pygame

from pygame.locals import (
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
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.isMoved = False

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


# Prima prova di videogioco fatto con Marco
if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    screen = init_screen()

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()
    screen.blit(player.surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

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

        screen = init_screen()

        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()


        player.update(pressed_keys)
        screen.blit(player.surf, player.rect)

        pygame.display.flip()


