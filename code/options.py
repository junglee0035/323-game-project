from settings import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame
import sys

class OptionsMenu:
    def __init__(self, game):
        self.game = game
        self.display_surface = game.display_surface
        self.clock = game.clock
        self.font = game.instruction_font

        self.resolutions = [(1280, 720), (1600, 900), (1920, 1080)]
        self.res_index = self.resolutions.index((WINDOW_WIDTH, WINDOW_HEIGHT)) if (WINDOW_WIDTH, WINDOW_HEIGHT) in self.resolutions else 0

        self.options = ["Music Volume", "SFX Volume", "Resolution", "Back"]
        self.index = 0
        self.music_volume = game.music_volume
        self.sfx_volume = game.sfx_volume

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            self.display_surface.fill((20, 20, 40))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_DOWN:
                        self.index = (self.index + 1) % len(self.options)
                        if self.game.nav_sound:
                            self.game.nav_sound.play()
                    elif event.key == pygame.K_UP:
                        self.index = (self.index - 1) % len(self.options)
                        if self.game.nav_sound:
                            self.game.nav_sound.play()
                    elif event.key == pygame.K_LEFT:
                        if self.game.nav_sound:
                            self.game.nav_sound.play()
                        if self.options[self.index] == "Music Volume":
                            self.music_volume = max(0, self.music_volume - 5)
                            pygame.mixer.music.set_volume(self.music_volume / 100)
                        elif self.options[self.index] == "SFX Volume":
                            self.sfx_volume = max(0, self.sfx_volume - 5)
                            if self.game.nav_sound:
                                self.game.nav_sound.set_volume(self.sfx_volume / 100)
                        elif self.options[self.index] == "Resolution":
                            self.res_index = (self.res_index - 1) % len(self.resolutions)
                            self.update_resolution()
                    elif event.key == pygame.K_RIGHT:
                        if self.game.nav_sound:
                            self.game.nav_sound.play()
                        if self.options[self.index] == "Music Volume":
                            self.music_volume = min(100, self.music_volume + 5)
                            pygame.mixer.music.set_volume(self.music_volume / 100)
                        elif self.options[self.index] == "SFX Volume":
                            self.sfx_volume = min(100, self.sfx_volume + 5)
                            if self.game.nav_sound:
                                self.game.nav_sound.set_volume(self.sfx_volume / 100)
                        elif self.options[self.index] == "Resolution":
                            self.res_index = (self.res_index + 1) % len(self.resolutions)
                            self.update_resolution()

                    elif event.key == pygame.K_RETURN:
                        if self.game.select_sound:
                            self.game.select_sound.play()
                        if self.options[self.index] == "Back":
                            running = False

            for i, opt in enumerate(self.options):
                selected = i == self.index
                color = (255, 255, 255) if selected else (100, 100, 100)
                
                if opt == "Music Volume":
                    value = f": {self.music_volume}"
                elif opt == "SFX Volume":
                    value = f": {self.sfx_volume}"
                elif opt == "Resolution":
                    res = self.resolutions[self.res_index]
                    value = f": {res[0]}x{res[1]}"
                else:
                    value = ""
               
                text = self.font.render(f"{opt}{value}", True, color)
                x = WINDOW_WIDTH // 2 - text.get_width() // 2
                y = 200 + i * 50
                self.display_surface.blit(text, (x, y))

            pygame.display.update()

        self.game.music_volume = self.music_volume
        self.game.sfx_volume = self.sfx_volume
    
    def update_resolution(self):
        new_res = self.resolutions[self.res_index]
        self.game.display_surface = pygame.display.set_mode(new_res)
        self.display_surface = self.game.display_surface
