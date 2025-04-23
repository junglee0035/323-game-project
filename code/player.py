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
        self.rect.y += self.direction.y * self.speed * dt
        for solid in solids:
            if self.rect.colliderect(solid.rect):
                if self.direction.y > 0:  # Moving down
                    self.rect.bottom = solid.rect.top
                elif self.direction.y < 0:  # Moving up
                    self.rect.top = solid.rect.bottom

    def update(self, dt, solids):
        self.handle_input()
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.move(dt, solids)