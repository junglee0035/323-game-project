import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from graphics.components.backround_animator import BackgroundAnimator
from graphics.components.head_bar import HeadBar  # ✅ 引入 HeadBar
from soundEffectManager import SoundEffectManager  # ✅ 导入新类

def run_shop(player_coins=0, on_return=None):
    screen = pygame.display.get_surface()
    pygame.display.set_caption("SHOP - NEXUS CORE")
    clock = pygame.time.Clock()

    bg_animator = BackgroundAnimator(screen)
    font_title = pygame.font.SysFont(None, 96)
    font_option = pygame.font.SysFont(None, 60)
    font_alert = pygame.font.SysFont(None, 40)

    def go_back():
        print("⬅️ 从商店返回原页面")
        if on_return:
            on_return()
        nonlocal running
        running = False

    head_bar = HeadBar(
        screen,
        coin_count=player_coins,
        on_go_shop=go_back,
        on_go_home=go_back
    )

    shop_effects = {
        "money_collect": False,
        "higher_jump": False,
        "skip_level": False
    }

    # ✅ 商品价格
    prices = {
        "money_collect": 50,
        "higher_jump": 100,
        "skip_level": 200
    }

    # ✅ 警告提示（商品名称 → 是否金币不足）
    show_alert = {
        "money_collect": False,
        "higher_jump": False,
        "skip_level": False
    }

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Keyboard shortcuts for purchases
                if event.key == pygame.K_1:
                    if player_coins >= prices["money_collect"]:
                        print("✅ 购买 Money Collect")
                        shop_effects["money_collect"] = True
                        player_coins -= prices["money_collect"]
                        show_alert["money_collect"] = False
                    else:
                        SoundEffectManager.play_effect("select.wav")
                        print("❗ 金币不足购买 Money Collect")
                        show_alert["money_collect"] = True

                elif event.key == pygame.K_2:
                    if player_coins >= prices["higher_jump"]:
                        print("✅ 购买 Higher Jump")
                        shop_effects["higher_jump"] = True
                        player_coins -= prices["higher_jump"]
                        show_alert["higher_jump"] = False
                    else:
                        SoundEffectManager.play_effect("select.wav")
                        print("❗ 金币不足购买 Higher Jump")
                        show_alert["higher_jump"] = True

                elif event.key == pygame.K_3:
                    if player_coins >= prices["skip_level"]:
                        print("✅ 购买 Skip Level")
                        shop_effects["skip_level"] = True
                        player_coins -= prices["skip_level"]
                        show_alert["skip_level"] = False
                    else:
                        SoundEffectManager.play_effect("select.wav")
                        print("❗ 金币不足购买 Skip Level")
                        show_alert["skip_level"] = True

                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 420 <= x <= 900:
                    if 220 <= y <= 260:
                        if player_coins >= prices["money_collect"]:
                            print("✅ 购买 Money Collect")
                            shop_effects["money_collect"] = True
                            player_coins -= prices["money_collect"]
                            show_alert["money_collect"] = False
                        else:
                            SoundEffectManager.play_effect("select.wav")
                            print("❗ 金币不足购买 Money Collect")
                            show_alert["money_collect"] = True
                    elif 300 <= y <= 340:
                        if player_coins >= prices["higher_jump"]:
                            print("✅ 购买 Higher Jump")
                            shop_effects["higher_jump"] = True
                            player_coins -= prices["higher_jump"]
                            show_alert["higher_jump"] = False
                        else:
                            SoundEffectManager.play_effect("select.wav")
                            print("❗ 金币不足购买 Higher Jump")
                            show_alert["higher_jump"] = True
                    elif 420 <= y <= 460:
                        if player_coins >= prices["skip_level"]:
                            print("✅ 购买 Skip Level")
                            shop_effects["skip_level"] = True
                            player_coins -= prices["skip_level"]
                            show_alert["skip_level"] = False
                        else:
                            SoundEffectManager.play_effect("select.wav")
                            print("❗ 金币不足购买 Skip Level")
                            show_alert["skip_level"] = True

            head_bar.handle_event(event)

        bg_animator.update(dt)
        bg_animator.draw()

        title = font_title.render("SHOP", True, (255, 255, 255))
        screen.blit(title, (560, 80))

        # 商品选项 + 红色感叹号提示
        screen.blit(font_option.render("1. Money Collect - 50", True, (255, 255, 255)), (420, 220))
        if show_alert["money_collect"]:
            screen.blit(font_alert.render("short of money", True, (255, 50, 50)), (900, 220))

        screen.blit(font_option.render("2. Higher Jump - 100", True, (255, 255, 255)), (420, 300))
        if show_alert["higher_jump"]:
            screen.blit(font_alert.render("short of money", True, (255, 50, 50)), (900, 300))

        screen.blit(font_option.render("3. Skip Level - 200", True, (200, 200, 200)), (420, 420))
        if show_alert["skip_level"]:
            screen.blit(font_alert.render("short of money", True, (255, 50, 50)), (900, 420))

        head_bar.update_coins(player_coins)
        head_bar.draw()

        pygame.display.flip()

    return shop_effects, player_coins

