import pygame
import sys

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# Define character properties
CHARACTER_RADIUS = 25  # Character as a circle
character_x = 400
character_y = 400
character_speed = 5
character_velocity_y = 0
is_jumping = False

# Define gravity and jump height
gravity = 1
jump_strength = -25

# Set up the clock
clock = pygame.time.Clock()

# Define the platforms (initial world positions)
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 50, 1600, 50),  # Ground, wider for scrolling
    pygame.Rect(100, SCREEN_HEIGHT - 150, 200, 20),
    pygame.Rect(400, SCREEN_HEIGHT - 250, 200, 20),
    pygame.Rect(200, SCREEN_HEIGHT - 350, 200, 20),
    pygame.Rect(600, SCREEN_HEIGHT - 450, 200, 20)
]

# Camera setup
camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Initially showing full screen

def draw_character(x, y):
    # Draw the character as a circle at the camera's offset
    pygame.draw.circle(screen, BLACK, (x - camera.x, y - camera.y), CHARACTER_RADIUS)

def draw_platforms():
    # Draw the platforms relative to the camera's position
    for plat in platforms:
        pygame.draw.rect(screen, BLACK, plat.move(-camera.x, -camera.y))

def handle_collision(character_rect):
    global character_y, character_velocity_y, is_jumping

    # Check for collision with platforms
    on_ground = False
    for plat in platforms:
        # Adjust platform positions relative to camera
        plat_rect = plat.move(-camera.x, -camera.y)  # Move the platform by the camera's offset

        if character_rect.colliderect(plat_rect):
            if character_velocity_y > 0:  # Only reset when falling
                character_y = plat.top - CHARACTER_RADIUS
                character_velocity_y = 0
                is_jumping = False
                on_ground = True
                break

    if not on_ground:
        character_velocity_y += gravity  # Apply gravity if not on ground

def update_camera():
    global camera

    # Update the camera to follow the character
    camera.x = character_x - SCREEN_WIDTH // 2
    camera.y = character_y - SCREEN_HEIGHT // 2

    # Make sure the camera doesn't go out of bounds
    if camera.x < 0:
        camera.x = 0
    if camera.y < 0:
        camera.y = 0
    if camera.x > 1600 - SCREEN_WIDTH:  # Assuming level width is 1600px
        camera.x = 1600 - SCREEN_WIDTH
    if camera.y > SCREEN_HEIGHT:  # Limiting camera to stay within screen height
        camera.y = SCREEN_HEIGHT

# Main game loop
while True:
    screen.fill(WHITE)  # Fill the screen with white

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of the keyboard
    keys = pygame.key.get_pressed()

    # Move the character
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x += character_speed

    # Jumping logic
    if not is_jumping and keys[pygame.K_SPACE]:
        character_velocity_y = jump_strength
        is_jumping = True

    # Update character's vertical position
    character_velocity_y += gravity
    character_y += character_velocity_y

    # Prevent the character from falling below the screen
    if character_y > SCREEN_HEIGHT - CHARACTER_RADIUS:
        character_y = SCREEN_HEIGHT - CHARACTER_RADIUS
        character_velocity_y = 0
        is_jumping = False

    # Define the character's rect for collision detection (circle)
    character_rect = pygame.Rect(character_x - CHARACTER_RADIUS, character_y - CHARACTER_RADIUS, CHARACTER_RADIUS * 2, CHARACTER_RADIUS * 2)

    # Handle collisions with platforms
    handle_collision(character_rect)

    # Update the camera position
    update_camera()

    # Draw everything with the camera offset
    draw_platforms()

    # Draw the character relative to the camera's position
    draw_character(character_x, character_y)

    # Update the screen
    pygame.display.flip()

    # Set the frame rate
    clock.tick(FPS)
