import pygame

def init_music():
    pygame.mixer.init()  # 初始化音效

    # 定义每个状态的音效
    global home_music, quiz_music, chat_music, gameover_music, menu_music

    home_music = pygame.mixer.Sound('music\\Homemusic.wav') # 主頁面音樂
    menu_music = pygame.mixer.Sound('music\\starmusicWAV.wav')
    quiz_music = pygame.mixer.Sound('music\\quizmusic.wav') # 問答模式音樂
    chat_music = pygame.mixer.Sound('music\\endingmusic.wav') # 聊天模式音樂
    gameover_music = pygame.mixer.Sound('music\\endingmusic.wav') # 結束畫面音樂

    # 设置每个音效的音量 (范围从 0.0 到 1.0)
    home_music.set_volume(0.8)  # 主頁面音樂，音量設置為 80%
    quiz_music.set_volume(0.5)  # 問答模式音樂，音量設置為 70%
    chat_music.set_volume(0.6)  # 聊天模式音樂，音量設置為 60%
    gameover_music.set_volume(0.9)  # 結束畫面音樂，音量設置為 90%
    menu_music.set_volume(0.8)

def play_music(state):
    # 停止当前所有音效
    pygame.mixer.stop()

    # 根据不同状态播放不同的音乐
    if state == 'home':
        home_music.play(-1)  # -1 表示循环播放
    elif state == 'menu':
        menu_music.play(-1)
    elif state == 'playing':
        quiz_music.play(-1)
    elif state == 'chat':
        chat_music.play(-1)
    elif state == 'game_over':
        gameover_music.play(-1)
