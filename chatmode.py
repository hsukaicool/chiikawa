import pygame
import openai
import sys
import os
import config
from dotenv import load_dotenv

# 加載 .env 文件中的環境變量
load_dotenv()

# 從環境變量中獲取 OpenAI API 金鑰
openai.api_key = os.getenv('OPENAI_API')
if openai.api_key:
    print("API 金鑰已成功加載")
else:
    print("未能加載 API 金鑰")

# 使用新的 ChatCompletion API
def get_ai_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一個幫助用戶解決問題的聊天助手。"},
            {"role": "user", "content": user_input},
        ]
    )
    return response['choices'][0]['message']['content'].strip()  # 返回 AI 的回應

# 定義聊天模式的輸入框處理，增加自動換行和行數限制
def draw_input_box(screen, user_text_lines, font, input_box_rect, input_box_color, border_color, text_color):
    # pygame.draw.rect(screen, input_box_color, input_box_rect)  # 輸入框背景色
    # pygame.draw.rect(screen, border_color, input_box_rect, 2)  # 輸入框邊框

    # 渲染每行用戶輸入的文本
    for i, line in enumerate(user_text_lines):
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (input_box_rect.x + 10, input_box_rect.y + 15 + i * font.get_height()))

# 檢查是否需要換行並限制最多三行
def wrap_text(user_text, font, max_width):
    wrapped_lines = []
    current_line = ""

    for char in user_text:
        # 檢查當前行加上這個字符的寬度是否超過最大寬度
        if font.size(current_line + char)[0] <= max_width:
            current_line += char  # 加入字符
        else:
            wrapped_lines.append(current_line)  # 如果超過寬度，先保存當前行
            current_line = char  # 開始新行
        
        # 如果行數已經超過三行，則不再添加更多行
        if len(wrapped_lines) == 3:
            break
    
    # 添加最後的行
    if len(wrapped_lines) < 3:
        wrapped_lines.append(current_line)
    
    return wrapped_lines[:3]  # 最多返回三行

# 自動換行並限制顯示行數的聊天記錄渲染函數
def display_chat_log(screen, chat_log, font, text_color, x_offset=50, y_start_offset=110, max_width=290, max_height=400, line_spacing=5, max_lines=5):
    """ 渲染聊天記錄在屏幕上，並進行自動換行和行數限制 """
    y_offset = y_start_offset  # 設定聊天記錄從上方的初始距離
    visible_lines = []  # 用來保存可以顯示的行

    # 遍歷每個聊天記錄進行換行處理
    for message in chat_log:
        current_line = ""
        for char in message:
            # 檢查當前行加上這個字符的寬度是否超過最大寬度
            if font.size(current_line + char)[0] <= max_width:
                current_line += char  # 加入字符
            else:
                visible_lines.append(current_line)  # 如果超過寬度，先保存當前行
                current_line = char  # 開始新行，從當前字符開始
        
        visible_lines.append(current_line)  # 保存最後一行

    # 限制顯示行數，避免超過對話框高度
    line_height = font.get_height() + line_spacing  # 加上行距
    visible_lines = visible_lines[-max_lines:]  # 只顯示最後的 max_lines 行

    # 渲染可見的聊天記錄
    for line in visible_lines:
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (x_offset, y_offset))
        y_offset += line_height  # 根據行高移動

def chat_mode(screen):
    clock = pygame.time.Clock()
    
    # 設置字體和顏色
    font = pygame.font.Font(config.FONT_PATH, 24)  # 使用 Pygame 字體
    text_color = (0, 55, 255)
    input_box_color = (50, 50, 50)
    border_color = (255, 255, 255)

    # 調整行距和行高
    line_spacing = 10  # 行距調整

    # 設置聊天輸入框的位置和尺寸
    input_box_rect = pygame.Rect(35, 503, 290, 100)  # x , y , 寬度 , 高度
    max_input_width = input_box_rect.width - 10  # 最大寬度減去左右邊距

    # 設置對話框的位置和尺寸
    chat_box_rect = pygame.Rect(35, 50, 250, 400)  # x, y, 寬度, 高度
    chat_box_color = (200, 200, 200)  # 設定對話框背景顏色
    chat_border_color = (255, 255, 255)  # 設定對話框邊框顏色

    chat_log = []  # 保存聊天記錄
    
    user_text = ""  # 保存用戶輸入的文字
    user_text_lines = []  # 保存分行的用戶輸入
    
    chat_log.append("有甚麼傷心事嗎")  # 初始化聊天記錄

    running = True
    while running:
        screen.blit(config.chat_background, (0, 0))

        # # 繪製對話框背景
        # pygame.draw.rect(screen, chat_box_color, chat_box_rect)  # 畫出對話框的背景
        # pygame.draw.rect(screen, chat_border_color, chat_box_rect, 2)  # 畫出對話框的邊框

        # 渲染聊天記錄
        display_chat_log(screen, chat_log, font, text_color, line_spacing=line_spacing, max_lines=5)
        
        # 設置最大輸入字元數
        MAX_INPUT_CHARS = 15
        back_button_rect = config.back_button_image.get_rect(topleft=(250, 400))  # 将按钮放置在 (10, 10)
        # 渲染返回主菜单按钮图片
        screen.blit(config.back_button_image,back_button_rect)
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检测是否点击了返回主菜单按钮
                if back_button_rect.collidepoint(event.pos):
                    running = False  # 停止当前聊天模式，退出到主菜单
                    return  # 退出 chat_mode 函数，回到主程序的状态管理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 如果按下回車鍵，提交消息
                    if user_text.strip():
                        chat_log.append(f"你: {user_text}")  # 添加用戶輸入到聊天記錄中
                        
                        # 呼叫 OpenAI API 獲取回應
                        ai_response = get_ai_response(user_text)
                        chat_log.append(f"烏薩其: {ai_response}")  # 顯示 AI 回應
                        
                        user_text = ""  # 清空輸入框
                        user_text_lines = []  # 清空已分行的輸入
                elif event.key == pygame.K_BACKSPACE:
                    # 刪除最後一個字符
                    user_text = user_text[:-1]
                elif len(user_text) < MAX_INPUT_CHARS:  # 限制輸入的字元數
                    if len(user_text_lines) < 3 or (len(user_text_lines) == 3 and font.size(user_text_lines[-1])[0] <= max_input_width):
                        user_text += event.unicode  # 添加鍵入的字符，支持中文字符輸入

                # 更新分行的用戶輸入
                user_text_lines = wrap_text(user_text, font, max_input_width)


        # 渲染聊天輸入框
        draw_input_box(screen, user_text_lines, font, input_box_rect, input_box_color, border_color, text_color)



        pygame.display.flip()
        clock.tick(30)  # 控制幀率

