import pygame
import sys
import config

def render_final_score_with_images(screen, final_score, score_images, x, y, size):
    """使用數字圖片顯示最終分數"""
    score_str = str(final_score)  # 將分數轉換為字串，方便逐個字符處理
    for i, digit in enumerate(score_str):
        # 假設你有 0-9 的圖片，這裡是載入的過程
        score_images = [pygame.image.load(f'image/images/{i}.png') for i in range(10)]
        # 根據數字選擇對應的圖片
        digit_image = score_images[int(digit)]

        # 使用 pygame.transform.scale() 將圖片縮放到指定大小
        scaled_digit_image = pygame.transform.scale(digit_image, (size, size))

        # 將數字圖片顯示在屏幕上的 (x, y) 位置，並根據每個數字圖片的寬度向右移動
        screen.blit(scaled_digit_image, (x + i * scaled_digit_image.get_width(), y))

def render_game_over(screen, font, restart_color, quit_color):
    """渲染遊戲結束畫面，帶有按鈕懸停效果"""
    
    # 使用變化的顏色渲染重新開始和退出遊戲按鈕
    restart_text = font.render("回主選單", True, restart_color)
    quit_text = font.render("退出遊戲", True, quit_color)

    # 背景
    screen.blit(config.game_over, (0, 0))  # 填充背景
    
    # 定義按鈕的區域，方便檢測點擊
    restart_rect = restart_text.get_rect(topleft=(40, 370))
    quit_rect = quit_text.get_rect(topleft=(200, 370))
    
    screen.blit(restart_text, restart_rect.topleft)
    screen.blit(quit_text, quit_rect.topleft)

    return restart_rect, quit_rect  # 返回矩形區域，方便點擊檢測

def handle_game_over_events(restart_rect, quit_rect, click_sound):
    """處理遊戲結束時的事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(event.pos):
                click_sound.play()  # 播放按鍵音效
                return 'restart'  # 返回重新開始
            elif quit_rect.collidepoint(event.pos):
                click_sound.play()  # 播放按鍵音效
                return 'quit'  # 返回退出
    return None

def game_over_run(screen, font, final_score, score_images):
    """
    將分數顯示、遊戲結束畫面渲染和事件處理結合在一起的主函數，支持按鈕懸停效果。
    """
    # 初始化按鈕顏色
    default_color = (0, 0, 0)  # 黑色
    hover_color = (255, 0, 0)  # 紅色，當滑鼠懸停時的顏色
    
    restart_color = default_color
    quit_color = default_color

    # 加載獎狀圖片，假設獎狀圖片位於 'image/certificate.png'
    certificate_image = config.load_image(config.FIRST_IMAGE, (180, 200))
    glod_image = config.load_image(config.GLOD_IMAGE, (180, 200))
    hight_image = config.load_image(config.HIGHT_IMAGE, (180, 200))
    
    # 加载音效
    hover_sound = pygame.mixer.Sound('sound/bubblesound.wav')  # 悬浮音效路径
    click_sound = pygame.mixer.Sound('sound\wusaqisound.wav')  # 按键音效路径

    hover_sound.set_volume(0.5)  # 设置悬浮音效音量
    click_sound.set_volume(0.5)  # 设置点击音效音量

    # 设置达标奖状显示的分数阈值
    certificate_threshold = 10
    glod_threshold = 20
    hight_threshold = 30

    running = True
    previous_hovered_button = None  # 用于记录上一次的悬浮按钮

    while running:

        # 檢測滑鼠移動
        mouse_pos = pygame.mouse.get_pos()  # 獲取滑鼠位置
        
        # 每次先填充背景，防止按鈕覆蓋分數
        screen.blit(config.game_over, (0, 0))  # 填充背景顏色
        
        # 根據滑鼠位置改變按鈕顏色
        restart_rect, quit_rect = render_game_over(screen, font, restart_color, quit_color)

        if restart_rect.collidepoint(mouse_pos):
            if previous_hovered_button != 'restart':
                hover_sound.play()  # 播放懸浮音效
                previous_hovered_button = 'restart'
            restart_color = hover_color  # 滑鼠懸停時變紅色
        else:
            restart_color = default_color  # 恢復默認顏色

        if quit_rect.collidepoint(mouse_pos):
            if previous_hovered_button != 'quit':
                hover_sound.play()  # 播放懸浮音效
                previous_hovered_button = 'quit'
            quit_color = hover_color  # 滑鼠懸停時變紅色
        else:
            quit_color = default_color  # 恢復默認顏色

        # 處理按鈕點擊事件
        action = handle_game_over_events(restart_rect, quit_rect, click_sound)
        if action == 'restart':
            return 'restart'  # 返回重新開始標誌，讓主程式重新開始遊戲
        elif action == 'quit':
            return 'quit'  # 返回退出標誌，讓主程式退出遊戲

        # 判斷是否達到獎狀顯示的分數
        if final_score >= hight_threshold:
            screen.blit(hight_image, (15, 420))
        elif final_score >= glod_threshold:
            screen.blit(glod_image, (15, 420))
        elif final_score >= certificate_threshold:
            screen.blit(certificate_image, (15, 420))

        # 渲染分數
        render_final_score_with_images(screen, final_score, score_images, x=30, y=500, size=70)

        pygame.display.flip()  # 保持畫面更新
