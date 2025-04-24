import os
import pytmx
from settings import *
from sprites import Sprite, Coin  
from player import Player
from Spotlight import Spotlight
from os.path import join

class Level:
    def __init__(self, tmx_map, game_instance, player_data):
        self.display_surface = pygame.display.get_surface()
        self.game_instance = game_instance

        # Store reference to player_data so we can update coins
        self.player_data = player_data

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.triggers = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        try:
            objects_layer = tmx_map.get_layer_by_name('Objects')
            print("Objects layer found.")
        except KeyError:
            print("Objects layer not found.")
            return

        for obj in objects_layer:
            if obj.name == 'player':
                Player((obj.x, obj.y), self.all_sprites, self.game_instance)

            elif obj.name == 'solid':
                solid_surface = pygame.Surface((obj.width, obj.height))
                solid_surface.fill((100, 100, 100))
                solid = Sprite((obj.x, obj.y), solid_surface, self.solids)
                self.all_sprites.add(solid)

            elif obj.name == 'spotlight':
                rotation_point = (obj.properties['rotation_point_x'], obj.properties['rotation_point_y'])
                radius = obj.properties['radius']
                speed = obj.properties['speed']
                start_angle = obj.properties.get('start_angle', 220)
                end_angle = obj.properties.get('end_angle', 120)
                spotlight = Spotlight(rotation_point, radius, speed, self.all_sprites, start_angle, end_angle)
                self.all_sprites.add(spotlight)

            elif obj.name == 'level_end':
                trigger_surface = pygame.Surface((obj.width, obj.height), pygame.SRCALPHA)
                trigger_surface.fill((0, 255, 0, 128))
                trigger = Sprite((obj.x, obj.y), trigger_surface, self.triggers)

            elif obj.name == 'coin':
                coin_image = pygame.image.load(join('graphics', 'icon', 'iconCoin.png')).convert_alpha()
                value = 5
                Coin((obj.x, obj.y), [self.all_sprites, self.coins], coin_image, value=value)

    def run(self, dt):
        # Update all sprites
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                sprite.update(dt, self.solids)
            else:
                sprite.update(dt)

        # Get player instance
        player = next((sprite for sprite in self.all_sprites if isinstance(sprite, Player)), None)

        # Check coin collection
        if player:
            collected = pygame.sprite.spritecollide(player, self.coins, dokill=True)
            for coin in collected:
                if self.game_instance.player_data.get("money_collect"):
                    self.player_data["coins"] += coin.value * 2
                else:
                    self.player_data["coins"] += coin.value
                if self.game_instance.coin_sound:
                    self.game_instance.coin_sound.play()
                print(f"🪙 Collected a coin! +{coin.value} → Total: {self.player_data['coins']}")

            # Check for level end trigger
            for trigger in self.triggers:
                if player.rect.colliderect(trigger.rect):
                    print("Level end trigger activated!")
                    return "next_stage"

        # Draw everything
        self.display_surface.fill('white')
        self.all_sprites.draw(self.display_surface)

        # Draw trigger outlines for debugging
        for trigger in self.triggers:
            pygame.draw.rect(self.display_surface, (0, 255, 0), trigger.rect, 2)

        return None
