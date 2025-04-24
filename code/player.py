import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, game):
        super().__init__(group)
        self.image = pygame.Surface((32, 32))  # Placeholder for player sprite
        self.image.fill('blue')  # Fill with a color for visibility
        self.rect = self.image.get_rect(topleft=pos)

        # Movement attributes
        self.game = game
        self.speed = 200  # Pixels per second
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 1300
        self.jump_force = -500
        self.on_ground = False
        self.jump_boost_active = False
        self.jump = False
        self.jump_buffered = False

        if self.game.player_data.get("higher_jump"):
            self.jump_force = -700

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_a]:  # Move left
            self.direction.x = -1
        if keys[pygame.K_d]:  # Move right
            self.direction.x = 1

        if keys[pygame.K_SPACE]:
            if not self.jump_buffered and self.on_ground:
                self.jump = True
                self.jump_buffered = True
        else:
            self.jump_buffered = False

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

        # prevents double jumping
        if self.jump and self.on_ground:
            jump_force = self.jump_force * 1.5 if self.jump_boost_active else self.jump_force
            self.direction.y = jump_force
            self.jump = False

        self.apply_gravity(dt)
        self.move(dt, solids)
