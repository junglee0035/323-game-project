import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((32, 32))  # Placeholder for player sprite
        self.image.fill('blue')  # Fill with a color for visibility
        self.rect = self.image.get_rect(topleft=pos)

        # Movement attributes
        self.speed = 200  # Pixels per second
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 1200
        self.jump_force = -500
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w]:  # Move up
            self.direction.y = -1
        if keys[pygame.K_s]:  # Move down
            self.direction.y = 1
        if keys[pygame.K_a]:  # Move left
            self.direction.x = -1
        if keys[pygame.K_d]:  # Move right
            self.direction.x = 1
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = self.jump_force
            self.on_ground = False
    
    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt
        if self.direction.y > 1000:
            self.direction.y = 1000

    def move(self, dt, solids):
        # Move horizontally and check for collisions
        self.rect.x += self.direction.x * self.speed * dt
        for solid in solids:
            if self.rect.colliderect(solid.rect):
                if self.direction.x > 0:  # Moving right
                    self.rect.right = solid.rect.left
                elif self.direction.x < 0:  # Moving left
                    self.rect.left = solid.rect.right

        # Move vertically and check for collisions
        self.rect.y += self.direction.y * dt
        self.on_ground = False
        for solid in solids:
            if self.rect.colliderect(solid.rect):
                if self.direction.y > 0:  # Moving down
                    self.rect.bottom = solid.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:  # Moving up
                    self.rect.top = solid.rect.bottom
                    self.direction.y = 0

    def update(self, dt, solids):
        self.handle_input()
        self.apply_gravity(dt)
        self.move(dt, solids)