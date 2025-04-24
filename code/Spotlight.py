import pygame
import math

class Spotlight(pygame.sprite.Sprite):
    def __init__(self, rotation_point, radius, speed, group, start_angle=220, end_angle=150):
        super().__init__(group)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)  # Spotlight size
        self.rect = self.image.get_rect(center=rotation_point)

        # Rotation attributes
        self.rotation_point = rotation_point  # Rotation point
        self.radius = radius  # Distance from the rotation point
        self.angle = start_angle  # Current angle in degrees
        self.speed = speed  # Rotation speed in degrees per second
        self.start_angle = start_angle  # Starting angle of the swing
        self.end_angle = end_angle  # Ending angle of the swing
        self.direction = -1  # -1 for counterclockwise, 1 for clockwise

    def update(self, dt):
        # Update the angle to swing back and forth
        self.angle += self.speed * dt * self.direction
        if self.angle > self.start_angle:
            self.angle = self.start_angle
            self.direction = -1  # Reverse direction
        elif self.angle < self.end_angle:
            self.angle = self.end_angle
            self.direction = 1  # Reverse direction

        # Clear the previous image
        self.image.fill((0, 0, 0, 0))  # Transparent background

        # Calculate the three points of the triangular beam
        start_x, start_y = self.rotation_point
        end_x1 = start_x + self.radius * math.cos(math.radians(self.angle - 90 - 15))  # Adjusted for downward direction
        end_y1 = start_y + self.radius * math.sin(math.radians(self.angle - 90 - 15))
        end_x2 = start_x + self.radius * math.cos(math.radians(self.angle - 90 + 15))  # Adjusted for downward direction
        end_y2 = start_y + self.radius * math.sin(math.radians(self.angle - 90 + 15))

        # Draw the triangular beam
        pygame.draw.polygon(
            self.image,
            (255, 255, 0, 128),  # Yellow color with transparency
            [(start_x - self.rect.left, start_y - self.rect.top),  # Rotation point
             (end_x1 - self.rect.left, end_y1 - self.rect.top),  # Left edge of the beam
             (end_x2 - self.rect.left, end_y2 - self.rect.top)]  # Right edge of the beam
        )
