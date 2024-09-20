import pygame
import sys
import os
from music import *  # 导入 music.py

# 初始化 Pygame
pygame.init()


def resource_path(relative_path):
    """獲取打包後的資源路徑"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 在打包後會創建一個臨時目錄，資源會被放在這裡
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_image(path, size=None):
    """加載並選擇性縮放圖片"""
    image = pygame.image.load(resource_path(path))
    if size:
        image = pygame.transform.scale(image, size)
    return image

def load_font(path, size):
    """加載字體"""
    return pygame.font.Font(resource_path(path), size)

# 設定顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# 字體和圖片路徑
FONT_PATH = "font/tsuhsianti-proportional2.0.ttf"

QA_IMAGE_PATH = "image/QAUI2.png"
BACKGROUND_IMAGE_PATH = 'image/menuimage.png'
INSTRUCTION_IMAGE_PATH = 'image/instruction.png'
QA_IMAGE_PATH_OLD = 'image/QA.png'
RIGHT_IMAGE = 'image/right.png'
WRONG_IMAGE = 'image/wrong.png'
GAME_OVER = 'image/gameoverUI.png'
FIRST_IMAGE = 'image/first.png'
GLOD_IMAGE = 'image/gold.png'
HIGHT_IMAGE = 'image/hight.png'
CHAT_IMAGE = 'image/chatUI.png'
CHIIKAWA_IMAGE = 'image/chiikawaimage.png'
BACK_BUTTON_IMAGE = 'image/backbuttinUI.png'

# 初始化 Pygame 視窗
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("吉伊卡哇")

# 加載資源
background = load_image(BACKGROUND_IMAGE_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
qa_background = load_image(QA_IMAGE_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
instruction_image = load_image(INSTRUCTION_IMAGE_PATH, (260, 75))
game_over = load_image(GAME_OVER, (SCREEN_WIDTH, SCREEN_HEIGHT))
right_image = load_image(RIGHT_IMAGE, (227, 208))
wrong_image = load_image(WRONG_IMAGE, (180, 165))
chat_background = load_image(CHAT_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
chiikawa_image = load_image(CHIIKAWA_IMAGE, (316, 109))
back_button_image = load_image(BACK_BUTTON_IMAGE, (65, 63))

# 字體加載
title_font = load_font(FONT_PATH, 35)
button_font = load_font(FONT_PATH, 50)
instruction_font = load_font(FONT_PATH, 50)
anser_font = load_font(FONT_PATH, 35)
over_font = load_font(FONT_PATH, 40)

# 假設你有 0-9 的圖片，這裡是載入的過程
score_images = [load_image(f'image/images/{i}.png') for i in range(10)]

# 問題的介面
source_rect = pygame.Rect(10, 10, 50, 50)
