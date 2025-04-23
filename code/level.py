import os
import pytmx
from settings import *
from sprites import Sprite
from player import Player
from Spotlight import Spotlight

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface() 

        #groups
        self.all_sprites = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.triggers = pygame.sprite.Group()
        self.setup(tmx_map)

    def setup(self, tmx_map):
        try:
            objects_layer = tmx_map.get_layer_by_name('Objects')
            print("Objects layer found.")
        except KeyError:
            print("Objects layer not found.")
            return

        # Handle objects from the Objects layer
        for obj in objects_layer:
            print(f"Object found: {obj.name} at ({obj.x}, {obj.y})")
            if obj.name == 'player':
                Player((obj.x, obj.y), self.all_sprites)
            elif obj.name == 'solid':
                solid_surface = pygame.Surface((obj.width, obj.height))
                solid_surface.fill((100, 100, 100))  # color for visibility
                solid = Sprite((obj.x, obj.y), solid_surface, self.solids)
                self.all_sprites.add(solid)
                print(f"Solid object added at ({obj.x}, {obj.y}) with size ({obj.width}, {obj.height})")
            elif obj.name == 'spotlight':
                # Get spotlight properties from the Tiled map
                rotation_point = (obj.properties['rotation_point_x'], obj.properties['rotation_point_y'])
                radius = obj.properties['radius']
                speed = obj.properties['speed']
                start_angle = obj.properties.get('start_angle', 220)  # Default to 220 degrees
                end_angle = obj.properties.get('end_angle', 120)  # Default to 150 degrees
                spotlight = Spotlight(rotation_point, radius, speed, self.all_sprites, start_angle, end_angle)
                self.all_sprites.add(spotlight)
                print(f"Spotlight added at rotation point {rotation_point} with radius {radius}, speed {speed}, start_angle {start_angle}, and end_angle {end_angle}")
            elif obj.name == 'level_end':
                # Create a trigger object for the level end
                trigger_surface = pygame.Surface((obj.width, obj.height), pygame.SRCALPHA)
                trigger_surface.fill((0, 255, 0, 128))  # Transparent green for debugging
                trigger = Sprite((obj.x, obj.y), trigger_surface, self.triggers)
                print(f"Level end trigger added at ({obj.x}, {obj.y}) with size ({obj.width}, {obj.height})")

    def run(self, dt):
        # Update all sprites
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                sprite.update(dt, self.solids)
            else:
                sprite.update(dt)

        # Check for collisions with triggers
        player = next((sprite for sprite in self.all_sprites if isinstance(sprite, Player)), None)
        if player:
            for trigger in self.triggers:
                if player.rect.colliderect(trigger.rect):
                    if trigger in self.triggers:
                        print("Level end trigger activated!")
                        return "next_stage"  # Signal to move to the next stage

        # Draw everything
        self.display_surface.fill('white')  # Clear the screen
        self.all_sprites.draw(self.display_surface)  # Draw all sprites

        # Debug: Draw trigger areas
        for trigger in self.triggers:
            pygame.draw.rect(self.display_surface, (0, 255, 0), trigger.rect, 2)  # Green outline for debugging

