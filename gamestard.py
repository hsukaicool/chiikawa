import pygame
import sys
import question
import gameover
import chatmode
from moviepy.editor import VideoFileClip
from music import *
from config import *

# 定义问题文件路径
JSON_PATH = 'Q&A\chiikawa_quiz1_formatted.json'

# 加载问题数据
questions_data = question.load_questions_from_json(JSON_PATH)

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((360, 640))
pygame.display.set_caption("問答遊戲")

# 初始化音效并播放主页音乐
init_music()


# 定义游戏状态
STATE_HOME = 'home'      # 首頁狀態
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_CHAT = 'chat'      # 新增聊天模式
STATE_PAUSED = 'paused'
STATE_GAME_OVER = 'game_over'
current_state = STATE_HOME  # 初始化为首頁

# 設置字體
font = pygame.font.Font(FONT_PATH, 50)
home_font = pygame.font.Font(FONT_PATH, 60)  # 首頁用的字體
button_font = pygame.font.Font(FONT_PATH, 40)  # 按钮文字的字體

# 定义按钮的矩形区域
quiz_button_rect = pygame.Rect(30, 430, 130, 50)  # 问答模式按钮区域
chat_button_rect = pygame.Rect(200, 430, 130, 50)  # 聊天模式按钮区域
# 設定影片並縮小到窗口大小
video_clip = VideoFileClip('video\homevideo.mp4').resize((360, 640))  # 調整影片大小

def stop_music():
    pygame.mixer.music.stop()  # 停止目前播放的音樂


# 設置時鐘來同步幀率
clock = pygame.time.Clock()

def play_video(screen, video_clip):
    global current_state  # 访问全局变量 current_state
    for frame in video_clip.iter_frames(fps=30, dtype="uint8"):
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(surface, (0, 0))
        pygame.display.update()

        # 控制播放速度，與影片的 fps 同步
        clock.tick(30)  # 使用影片的 fps 設定幀率

        # 檢查退出事件和滑鼠按鈕點擊
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 如果偵測到滑鼠按下，直接改變遊戲狀態進入選單模式並停止音樂
                stop_music()  # 停止首頁音樂
                current_state = STATE_MENU
                return  # 結束影片播放並返回主循環

# 加载视频剪辑
video_clip_menu = VideoFileClip('video\menu.mp4').resize((360, 202))  # 将视频调整到屏幕大小

def play_video_loop(screen, video_clip_menu):
    """
    播放视频并同时检测鼠标点击，进行按钮响应。
    返回当前状态:
    - STATE_MENU: 继续播放视频
    - STATE_PLAYING: 进入问答模式
    - STATE_CHAT: 进入聊天模式
    """
    for frame in video_clip_menu.iter_frames(fps=30, dtype="uint8"):
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(surface, (0, 220))
        pygame.display.update()

        # 控制帧速率，匹配视频的fps
        clock.tick(30)  # 这里我们使用的是30fps

        # 检查退出事件和其他事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 检测鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 如果点击了问答模式按钮
                if quiz_button_rect.collidepoint(event.pos):
                    play_music('playing')  # 播放问答模式音乐
                    return STATE_PLAYING  # 返回状态为问答模式

                # 如果点击了聊天模式按钮
                elif chat_button_rect.collidepoint(event.pos):
                    play_music('chat')  # 播放聊天模式音乐
                    return STATE_CHAT  # 返回状态为聊天模式

    return STATE_MENU  # 如果没有切换状态，继续保持菜单状态

def loop_video_in_menu():
    global current_state
    video_clip_menu.set_position(0)  # 确保视频从头播放
    while current_state == STATE_MENU:  # 在菜单状态中进行循环播放
        # 根据 play_video_loop 返回的状态更新 current_state
        current_state = play_video_loop(screen, video_clip_menu)  # 播放视频并获取当前状态

        # 如果状态不再是菜单状态，跳出循环
        if current_state != STATE_MENU:
            break

    # 此处处理退出菜单状态后的逻辑


def render_text_with_outline(font, text, position, text_color, outline_color, outline_thickness, surface, letter_spacing=0):
    # 渲染外邊框
    x, y = position
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0:
                # 獲取文字的每一個字母並渲染外框
                temp_x = x
                for letter in text:
                    outline_surface = font.render(letter, True, outline_color)
                    surface.blit(outline_surface, (temp_x + dx, y + dy))
                    temp_x += font.size(letter)[0] + letter_spacing  # 字母之間的距離保持一致
    
    # 渲染內部文字
    temp_x = x
    for letter in text:
        letter_surface = font.render(letter, True, text_color)
        surface.blit(letter_surface, (temp_x, y))
        temp_x += font.size(letter)[0] + letter_spacing  # 字母之間的距離





# 主循环
while True:
    current_time = pygame.time.get_ticks()  # 获取当前时间

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 根据当前状态处理事件
        if current_state == STATE_HOME:
            play_music('home')  # 播放首頁音樂
            play_video(screen, video_clip)  # 播放影片
            
            current_state = STATE_MENU  # 播放结束后进入菜单
            play_music('menu')  # 播放菜单音乐

        elif current_state == STATE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quiz_button_rect.collidepoint(event.pos):
                    current_state = STATE_PLAYING  # 进入问答模式
                    play_music('playing')  # 播放问答模式音乐
                elif chat_button_rect.collidepoint(event.pos):
                    current_state = STATE_CHAT  # 进入聊天模式
                    play_music('chat')  # 播放聊天模式音乐

        elif current_state == STATE_PLAYING:
            # 当问题全部回答完毕，返回 True，然后进入游戏结束状态
            finished, final_score = question.questionRun(screen, questions_data, font, font)
            if finished == True:
                current_state = STATE_GAME_OVER
                play_music('game_over')  # 播放游戏结束音乐
            else :
                current_state = STATE_MENU

        elif current_state == STATE_CHAT:
            # 在聊天模式下調用 chatmode.py 中的 chat_mode 函數
            chatmode.chat_mode(screen)  # 調用聊天模式
            current_state = STATE_MENU  # 聊天模式結束後返回菜单
            play_music('menu')  # 返回菜单音乐

        elif current_state == STATE_PAUSED:
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_state = STATE_PLAYING  # 继续游戏
                play_music('playing')  # 继续问答模式音乐

        elif current_state == STATE_GAME_OVER:
            action = gameover.game_over_run(screen, over_font, final_score, score_images)
            if action == 'restart':
                current_state = STATE_MENU  # 重启游戏逻辑
                play_music('playing')  # 重启问答模式音乐
            elif action == 'quit':
                pygame.quit()
                sys.exit()

    # 根据当前状态渲染不同内容
    if current_state == STATE_MENU:
        screen.blit(background,(0, 0))  # menu背景
        

        # 渲染首页内容，包含游戏标题
        screen.blit(chiikawa_image,(20, 0))  # menu背景


        # 渲染“问答模式”按钮
        # pygame.draw.rect(screen, (0, 0, 255), quiz_button_rect)  # 蓝色背景
        render_text_with_outline(button_font, "問答模式", quiz_button_rect.topleft, (255, 255, 255), (0, 0, 0), 2, screen, letter_spacing=2)

        # 渲染“聊天模式”按钮
        # pygame.draw.rect(screen, (0, 0, 255), chat_button_rect)  # 蓝色背景
        render_text_with_outline(button_font, "聊天模式", chat_button_rect.topleft, (255, 255, 255), (0, 0, 0), 2, screen, letter_spacing=2)


        loop_video_in_menu()
        

    pygame.display.flip()  # 更新显示
