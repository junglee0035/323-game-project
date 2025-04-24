from settings import * 
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from options import OptionsMenu
from shop import run_shop
from save_system import save_game, load_game
import os

class Game:
    def __init__(self):
        pygame.init()  # initialize Pygame
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Main display surface
        pygame.display.set_caption('Nexus Core - Prototype')  # Title for game windowed
        self.clock = pygame.time.Clock()  # Frame rate

        # Fonts
        self.title_font = pygame.font.SysFont("lucidaconsole", int(self.display_surface.get_height() * 0.07))
        self.instruction_font = pygame.font.SysFont("lucidaconsole", int(self.display_surface.get_height() * 0.035))
        self.coin_font = pygame.font.SysFont("lucidaconsole", 24)

        # Load player data
        self.player_data = load_game()

        # Load and scale background for title screen
        self.bg_image = pygame.image.load(join('graphics', 'ui', 'title_bg.png')).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Logo
        try:
            self.logo = pygame.image.load(join('graphics', 'ui', 'logo.png')).convert_alpha()
        except:
            self.logo = None

        # Sounds
        try:
            self.nav_sound = pygame.mixer.Sound(join('sound', 'nav.wav'))
            self.nav_sound.set_volume(0.4)
        except:
            self.nav_sound = None

        try:
            self.select_sound = pygame.mixer.Sound(join('sound', 'select.wav'))
            self.select_sound.set_volume(0.7)
        except:
            self.select_sound = None

        try:
            self.shop_sound = pygame.mixer.Sound(join('sound', 'shop.wav'))
            self.shop_sound.set_volume(0.6)
        except:
            self.shop_sound = None
            print("⚠️ Shop sound failed to load.")

        try:
            self.coin_sound = pygame.mixer.Sound(join('sound', 'coin.wav'))
            self.coin_sound.set_volume(0.6)
        except:
            self.coin_sound = None
            print("⚠️ Coin sound failed to load.")

        try:
            self.purchase_sound = pygame.mixer.Sound(join('sound', 'purchase.wav'))
            self.purchase_sound.set_volume(0.6)
        except:
            self.purchase_sound = None
            print("⚠️ Purchase sound failed to load.")

        # Menu state
        self.menu_options = ["START", "OPTIONS", "QUIT"]  # Menu options
        self.selected_index = 0
        self.music_volume = 50
        self.sfx_volume = 50
        self.flicker_timer = 0
        self.show_prompt = True
        self.start_time = None

        # Level management
        self.tmx_maps = {
            0: load_pygame(join('data', 'levels', 'Spotlight.tmx')),
            1: load_pygame(join('data', 'levels', 'wind_zone.tmx')),
            2: load_pygame(join('data', 'levels', 'wall.tmx')),
            3: load_pygame(join('data', 'levels', 'bridge.tmx')),
            4: load_pygame(join('data', 'levels', 'tipping_platforms.tmx')),
            5: load_pygame(join('data', 'levels', 'acid_pool.tmx')),
            6: load_pygame(join('data', 'levels', 'lava_pool.tmx')),
        }

        self.current_index = 0
        self.current_stage = Level(self.tmx_maps[self.current_index], self, self.player_data)

    def draw_titlescreen(self):
        self.display_surface.blit(self.bg_image, (0, 0))
        elapsed = pygame.time.get_ticks() - self.start_time
        fade_alpha = min(255, elapsed // 2)

        if self.logo:
            logo_surf = pygame.transform.scale(self.logo, (700, 400))
            logo_surf.set_alpha(fade_alpha)
            logo_x = (WINDOW_WIDTH // 2 - logo_surf.get_width() // 2)
            logo_y = 80
            self.display_surface.blit(logo_surf, (logo_x, logo_y))
        else:
            title_surf = self.title_font.render("NEXUS CORE", True, (255, 255, 255))
            title_surf.set_alpha(fade_alpha)
            self.display_surface.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 100))

        if fade_alpha >= 255:
            for i, option in enumerate(self.menu_options):
                color = (255, 255, 255) if i == self.selected_index else (100, 100, 100)
                option_surf = self.instruction_font.render(option, True, color)
                y = 360 + i * 40
                self.display_surface.blit(option_surf, (WINDOW_WIDTH // 2 - option_surf.get_width() // 2, y))
            pygame.display.update()

    def titlescreen(self):
        try:
            pygame.mixer.music.load(join('sound', 'titlescreen.wav'))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            print("Title music failed to load.")

        self.start_time = pygame.time.get_ticks()
        self.selected_index = 0

        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.menu_options)
                        if self.nav_sound: self.nav_sound.play()
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.menu_options)
                        if self.nav_sound: self.nav_sound.play()
                    elif event.key == pygame.K_RETURN:
                        if self.select_sound: self.select_sound.play()
                        selected = self.menu_options[self.selected_index]
                        if selected == "START":
                            pygame.mixer.music.stop()
                            return
                        elif selected == "OPTIONS":
                            OptionsMenu(self).run()
                        elif selected == "QUIT":
                            pygame.quit()
                            sys.exit()
            self.draw_titlescreen()

    def run(self):
        self.titlescreen()

        while True:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game(self.player_data)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.USEREVENT:
                    if event.dict.get('custom_type') == 'next_stage':
                        self.load_next_level()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.open_shop_menu()

            if self.current_stage:
                result = self.current_stage.run(dt)
                if result == "next_stage":
                    self.load_next_level()

            # Display coin icon and count
            coin_icon = pygame.image.load(join('graphics', 'icon', 'iconCoin.png')).convert_alpha()
            coin_icon = pygame.transform.scale(coin_icon, (32, 32))
            self.display_surface.blit(coin_icon, (15, 15))

            coin_text = self.coin_font.render(str(self.player_data['coins']), True, (255, 222, 0))
            self.display_surface.blit(coin_text, (55, 20))

            pygame.display.update()

    def load_next_level(self):
        self.current_index = (self.current_index + 1) % len(self.tmx_maps)
        self.current_stage = Level(self.tmx_maps[self.current_index], self, self.player_data)

    def open_shop_menu(self):
        result, self.player_data["coins"] = run_shop(player_coins=self.player_data["coins"])
        if result.get("money_collect"):
            print("🪙 Money collect activated.")
            self.player_data["has_money_collect"] = True
            if self.purchase_sound:
                self.purchase_sound.play()
        if result.get("higher_jump"):
            print("🦘 Higher jump activated.")
            self.player_data["higher_jump"] = True
            if self.purchase_sound:
                self.purchase_sound.play()
        if result.get("skip_level"):
            print("⏭️ Skipping to next level...")
            if self.purchase_sound:
                self.purchase_sound.play()
            self.load_next_level()

        save_game(self.player_data)

if __name__ == '__main__':
    game = Game()
    game.run()
