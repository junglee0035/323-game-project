# src/UI/components/headBar.py
import pygame
import os

# 获取当前文件夹路径（也就是 components 目录）
CURRENT_DIR = os.path.dirname(__file__)
# 拼接图标路径，跳到上级目录再进 icon 文件夹
ICON_DIR = os.path.join(CURRENT_DIR, "..", "icon")

class HeadBar:
    def __init__(self, screen, coin_count, on_go_shop, on_go_home):
        """
        初始化 HeadBar 状态栏

        参数：
        - screen：Pygame 屏幕对象
        - coin_count：初始金币数量
        - on_go_shop：点击金币图标时触发的函数
        - on_go_home：点击房子图标时触发的函数
        """
        self.screen = screen
        self.coin_count = coin_count
        self.on_go_shop = on_go_shop
        self.on_go_home = on_go_home

        # 字体和高度
        self.font = pygame.font.SysFont(None, 36)
        self.bar_height = 60

        # ✅ 加载图标
        self.coin_icon = pygame.image.load(os.path.join(ICON_DIR, "iconCoin.png")).convert_alpha()
        self.home_icon = pygame.image.load(os.path.join(ICON_DIR, "iconHome.png")).convert_alpha()

        # ✅ 缩放为统一大小
        self.coin_icon = pygame.transform.scale(self.coin_icon, (40, 40))
        self.home_icon = pygame.transform.scale(self.home_icon, (40, 40))

        # ✅ 设置图标位置
        self.coin_rect = self.coin_icon.get_rect(topleft=(20, 10))  # 左上角金币图标
        self.home_rect = self.home_icon.get_rect(topright=(self.screen.get_width() - 60, 10))  # 右上角主页图标

    def update_coins(self, new_count):
        """更新金币数量"""
        self.coin_count = new_count

    def draw(self):
        """绘制状态栏：金币图标 + 数量 + 返回图标"""

        # 背景可选绘制，当前透明

        # ✅ 绘制金币图标
        self.screen.blit(self.coin_icon, self.coin_rect.topleft)

        # ✅ 绘制金币数字
        coin_text = self.font.render(str(self.coin_count), True, (255, 215, 0))  # 金黄色
        self.screen.blit(coin_text, (self.coin_rect.right + 10, self.coin_rect.top + 5))

        # ✅ 绘制返回主页图标
        self.screen.blit(self.home_icon, self.home_rect.topleft)

    def handle_event(self, event):
        """处理鼠标点击事件：判断是否点中了图标"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.coin_rect.collidepoint(event.pos):
                print("🪙 点击金币图标 → 跳转商店")
                if self.on_go_shop:
                    self.on_go_shop()
            elif self.home_rect.collidepoint(event.pos):
                print("🏠 点击主页图标 → 返回首页")
                if self.on_go_home:
                    self.on_go_home()