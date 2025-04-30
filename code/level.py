import os
import pytmx
from settings import *
from os.path import join
from sprites import Sprite, Coin
from player import Player
from Spotlight import Spotlight
#should be working

class Level:
    def __init__(self, tmx_map, game_instance):
        self.display_surface = pygame.display.get_surface() 
        self.tmx_map = tmx_map
        self.game_instance = game_instance 

        #groups
        self.all_sprites = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.triggers = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.walls = []
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
                Player((obj.x, obj.y), self.all_sprites, self.game_instance)
            elif obj.type == 'button':
                button_surface = pygame.Surface((obj.width, obj.height), pygame.SRCALPHA)
                button_surface.fill((255, 255, 0, 128))
                button = Sprite((obj.x, obj.y), button_surface, self.triggers)
                button.prompt = obj.properties.get('prompt', None)
                print(f"Button object added at ({obj.x}, {obj.y}) with prompt '{button.prompt}'")
            elif obj.name == 'solid':
                solid_surface = pygame.Surface((obj.width, obj.height))
                solid_surface.fill((10, 0, 0))  # color for visibility
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
            elif obj.name == 'wall':
                # Add wall objects to the walls list
                wall_surface = pygame.Surface((obj.width, obj.height))
                wall_surface.fill((150, 75, 0))  # Brown color for visibility
                wall = Sprite((obj.x, obj.y), wall_surface, self.solids)
                self.all_sprites.add(wall)
                self.walls.append(wall)
                print(f"Wall object added at ({obj.x}, {obj.y}) with size ({obj.width}, {obj.height})")
            elif obj.name == 'level_end':
                # Create a trigger object for the level end
                trigger_surface = pygame.Surface((obj.width, obj.height), pygame.SRCALPHA)
                trigger_surface.fill((0, 255, 0, 128))  # Transparent green for debugging'
                level_end = Sprite((obj.x, obj.y), trigger_surface, self.triggers)
                level_end.name = 'level_end'
                print(f"Level end trigger added at ({obj.x}, {obj.y}) with size ({obj.width}, {obj.height})")
            elif obj.name == 'coin':
               coin_image = pygame.image.load(join('graphics', 'icon', 'iconCoin.png')).convert_alpha()
               value = 5
               Coin((obj.x, obj.y), [self.all_sprites, self.coins], coin_image, value=value)
            elif obj.type == 'wind_zone':
                # Create a wind zone trigger
                trigger_surface = pygame.Surface((obj.width, obj.height), pygame.SRCALPHA)
                trigger_surface.fill((0, 255, 200, 128))  # Semi-transparent blue for debugging
                wind_zone = Sprite((obj.x, obj.y), trigger_surface, self.triggers)
                wind_zone.jump_mod = obj.properties.get('jump_mod', 1.0)  # Default jump modifier is 1.0
                print(f"Wind zone added at ({obj.x}, {obj.y}) with jump_mod {wind_zone.jump_mod}")
            if obj.type == 'button':
                # Create a button object
                button_surface = pygame.Surface((obj.width, obj.height), pygame.SRCALPHA)
                button_surface.fill((255, 255, 0, 128))  # Semi-transparent yellow for debugging
                button = Sprite((obj.x, obj.y), button_surface, self.triggers)
                button.activate_object_layer = obj.properties.get('activate_object_layer', None)
                button.activate_tile_layer = obj.properties.get('activate_tile_layer', None)
                print(f"Button added at ({obj.x}, {obj.y}) to activate object layer '{button.activate_object_layer}' and tile layer '{button.activate_tile_layer}'")

    def activate_object_layer(self, layer_name):
        try:
            layer = self.tmx_map.get_layer_by_name(layer_name)
            if hasattr(layer, 'visible'):
                layer.visible = True
                print(f"Object layer '{layer_name}' activated.")
        except KeyError:
            print(f"Object layer '{layer_name}' not found.")

    def activate_tile_layer(self, layer_name):
        try:
            layer = self.tmx_map.get_layer_by_name(layer_name)
            if hasattr(layer, 'visible'):
                layer.visible = True
                print(f"Tile layer '{layer_name}' activated.")
        except KeyError:
            print(f"Tile layer '{layer_name}' not found.")

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
            collected = pygame.sprite.spritecollide(player, self.coins, dokill=True)
            for coin in collected:
               if self.game_instance.player_data.get("money_collect"):
                   self.game_instance.player_data["coins"] += coin.value * 2

               else:
                   self.game_instance.player_data["coins"] += coin.value

               if self.game_instance.coin_sound:
                   self.game_instance.coin_sound.play()
               print(f"🪙 Collected a coin! +{coin.value} → Total: {self.game_instance.player_data['coins']}")


            in_wind_zone = False
            for trigger in self.triggers:
                if player.rect.colliderect(trigger.rect) and hasattr(trigger, 'jump_mod'):
                    # Increase player's jump height based on wind zone's jump_mod
                    player.jump_force = player.default_jump_force * trigger.jump_mod
                    in_wind_zone = True
                    print(f"Player in wind zone: jump height increased to {player.jump_force}")
                elif player.rect.colliderect(trigger.rect) and hasattr(trigger, 'prompt'):
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_x]:  # Press 'X' to activate
                        if trigger.prompt == 'remove':
                            for wall in self.walls:
                                wall.image.set_alpha(0)
                                self.solids.remove(wall)
                                print(f"Wall at ({wall.rect.x}, {wall.rect.y}) removed")
                        elif trigger.prompt == 'add':
                            solid_surface = pygame.Surface((288, 32))
                            solid_surface.fill((100, 100, 100))
                            new_solid = Sprite((384, 416), solid_surface, [self.all_sprites, self.solids])
                            print(f"New solid added at ({new_solid.rect.x}, {new_solid.rect.y}) with size ({new_solid.rect.width}, {new_solid.rect.height})")
                        self.walls.clear()  # Clear the walls list
                        print(f"Button pressed at ({trigger.rect.x}, {trigger.rect.y})")
                elif player.rect.colliderect(trigger.rect) and hasattr(trigger, 'name') and trigger.name == 'level_end':
                    print("Level end trigger activated!")
                    return "next_stage"  # Signal to move to the next stage

            # Reset jump height if the player is no longer in a wind zone
            if not in_wind_zone:
                player.jump_force = player.default_jump_force
                print(f"Player left wind zone: jump height reset to {player.jump_force}")

        # Draw tile layers
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        self.display_surface.blit(tile, (x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight))

        # Draw everything
        self.display_surface.fill('white')  # Clear the screen
        self.all_sprites.draw(self.display_surface)  # Draw all sprites
        # Debug: Draw trigger areas
        for trigger in self.triggers:
            if hasattr(trigger, 'prompt'):
                pygame.draw.rect(self.display_surface, (255, 0, 0), trigger.rect, 2)
            if hasattr(trigger, 'jump_mod'):
                pygame.draw.rect(self.display_surface, (0, 255, 0), trigger.rect, 2)  # Green outline for debugging

        pygame.display.update()  # Update the display


