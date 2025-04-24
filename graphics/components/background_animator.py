import pygame
import os

class BackgroundAnimator:
    def __init__(self, screen, folder_path=None, size=(1280, 720), interval=200):
        self.screen = screen
        self.interval = interval
        self.timer = 0
        self.index = 0
        self.images = []

        # ✅ 自动构造正确的图片路径（兼容任意调用位置）
        if folder_path is None:
            current_dir = os.path.dirname(__file__)  # /src/UI/components
            folder_path = os.path.join(current_dir, "..","ui")
            folder_path = os.path.abspath(folder_path)

        print(f"📂 正在加载背景图路径: {folder_path}")

        # ✅ 加载背景图片
        for filename in ["BGimage.png", "BGimage.png", "BGimage.png"]:
            path = os.path.join(folder_path, filename)
            if os.path.exists(path):
                image = pygame.transform.scale(pygame.image.load(path), size)
                self.images.append(image)
                print(f"✅ 加载背景图: {filename}")
            else:
                print(f"❌ 背景图不存在: {path}")

        if not self.images:
            raise RuntimeError("⚠️ 没有成功加载任何背景图！")

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.interval:
            self.index = (self.index + 1) % len(self.images)
            self.timer = 0

    def draw(self):
        if self.images:
            self.screen.blit(self.images[self.index], (0, 0))