from settings import * 
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        sprite_path = os.path.join("graphics", "player", "ball4En.png")
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=pos)

        # Movement attributes
        self.speed = 200
        self.direction = pygame.math.Vector2(0, 0)

        self.gravity = 1300
        self.jump_force = -600
        self.jump = False
        self.jump_buffered = False
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)

        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        
        if input_vector.length_squared() > 0:
            input_vector = input_vector.normalize()

        self.direction.x = input_vector.x

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
        # Horizontal movement
        self.rect.x += self.direction.x * self.speed * dt
        for solid in solids:
            if self.rect.colliderect(solid.rect):
                if self.direction.x > 0:
                    self.rect.right = solid.rect.left
                elif self.direction.x < 0:
                    self.rect.left = solid.rect.right

        # Vertical movement
        self.rect.y += self.direction.y * dt  # Use gravity-scaled direction.y directly
        self.on_ground = False
        for solid in solids:
            if self.rect.colliderect(solid.rect):
                if self.direction.y > 0:
                    self.rect.bottom = solid.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.rect.top = solid.rect.bottom
                    self.direction.y = 0
        
    

    def update(self, dt, solids):
        self.handle_input()

        if self.jump and self.on_ground:
            self.direction.y = self.jump_force
            self.jump = False

        self.apply_gravity(dt)
        self.move(dt, solids)
