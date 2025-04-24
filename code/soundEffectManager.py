import pygame
import os

class SoundEffectManager:
    @staticmethod
    def play_effect(filename):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        path = os.path.join(base_dir, "assets", "sound", filename)

        if not os.path.exists(path):
            print(f"[音效错误] 找不到音效文件：{path}")
            return

        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.8)  # 默认音量
        sound.play()
