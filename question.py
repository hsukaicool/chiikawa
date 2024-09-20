import pygame
import json
import random  # 引入随机模块
import config

# 初始化 Pygame，注意在主程序中调用pygame.init()
pygame.mixer.init()  # 初始化音效

# 加载音效
# bubble_sound = pygame.mixer.Sound('sound\wusaqisound.wav')  # 替换为你的點擊音效路径
hover_sound = pygame.mixer.Sound('sound/bubblesound.wav')  # 替换为你的懸停音效路径
correct_sound = pygame.mixer.Sound('sound/right.wav')  # 替换为你的正確答案音效路径
wrong_sound = pygame.mixer.Sound('sound/wrong.wav')  # 替换为你的錯誤答案音效路径

# 设置音效音量，0.0 为最小音量，1.0 为最大音量
# bubble_sound.set_volume(0.5)  # 设置为 50% 的音量
hover_sound.set_volume(0.5)  # 设置为 50% 的音量
correct_sound.set_volume(0.7)  # 设置正确答案音效为 70%
wrong_sound.set_volume(0.7)  # 设置错误答案音效为 70%

# 定义加载 JSON 文件的函数
def load_questions_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def render_text_with_outline(font, text, position, text_color, outline_color, outline_width, screen, letter_spacing=2):
    """渲染带有描边效果的文字，并在字母之间增加间距"""
    x, y = position

    for char in text:
        # 渲染描边
        for dx in [-outline_width, 0, outline_width]:
            for dy in [-outline_width, 0, outline_width]:
                if dx != 0 or dy != 0:
                    outline_surface = font.render(char, True, outline_color)
                    screen.blit(outline_surface, (x + dx, y + dy))
        # 渲染字符
        text_surface = font.render(char, True, text_color)
        screen.blit(text_surface, (x, y))
        # 增加 x 坐标，以便下一个字符显示在后面，加上字距
        x += text_surface.get_width() + letter_spacing  # 增加字母间距

def render_question_and_options(screen, question_data, title_font, option_font, selected_option, hovered_option):
    """渲染问题和选项，带有悬停和点击效果"""
    # screen.blit(config.screen.blit(config.qa_background, (0, 0))  # 背景图像, (0, 0))  # 背景图像

    # 渲染问题部分，支持多行
    y_position = 105  # 问题的初始 y 坐标
    line_spacing_question = 5  # 控制问题部分的行间距

    for line in question_data['question']:
        render_text_with_outline(title_font, line, (75, y_position), (255, 255, 255), (0, 0, 0), 2, screen, letter_spacing=5)
        y_position += title_font.get_height() + line_spacing_question  # 每行的间距

    # 渲染选项部分
    y_position1 = 300  # 初始化选项部分的 y 坐标
    line_spacing_option = 10  # 控制选项部分的行间距

    for i, option in enumerate(question_data['options']):
        if i == selected_option:
            color = (255, 255, 0)  # 点击后选项变黄
        elif i == hovered_option:
            color = (0, 255, 0)  # 悬停时选项变绿
        else:
            color = (255, 255, 255)  # 默认选项颜色为白色

        # 使用 y_position1 来控制每个选项的 y 坐标
        render_text_with_outline(config.anser_font, f"{i + 1}. {option}", (75, y_position1), color, (0, 0, 0), 2, screen, letter_spacing=3)
        y_position1 += config.anser_font.get_height() + line_spacing_option  # 每行选项的间距

    pygame.display.flip()


# 处理鼠标点击事件
def handle_mouse_click(pos, options_count):
    """检测鼠标点击的选项，并返回选项的索引"""
    x, y = pos
    y_position1 = 300
    for i in range(options_count):
        option_rect = pygame.Rect(100, y_position1 + i * 45, 200, 30)  # 选项矩形
        if option_rect.collidepoint(x, y):
            return i
    return None

# 检查答案是否正确
def check_answer(question_data, selected_option):
    # 从选项列表中取出用户选择的答案
    selected_answer = question_data['options'][selected_option]

    # 打印调试信息，检查用户选择的选项和正确答案
    print(f"Selected Answer: {selected_answer}")
    print(f"Correct Answer: {question_data['correct_answer']}")

    # 返回比较结果，比较选项和正确答案
    return selected_answer == question_data['correct_answer']

def render_score(screen, score, x, y, score_images, size):
    """顯示分數在指定的 x, y 位置，使用圖片來表示數字，並根據 size 進行縮放"""
    score_str = str(score)  # 將分數轉換為字串，方便逐個字符處理
    for i, digit in enumerate(score_str):
        digit_image = score_images[int(digit)]  # 根據數字選擇對應的圖片

        # 使用 pygame.transform.scale() 將圖片縮放到指定大小
        scaled_digit_image = pygame.transform.scale(digit_image, (size, size))

        # 按照位置逐個顯示數字圖片
        screen.blit(scaled_digit_image, (x + i * scaled_digit_image.get_width(), y))


def questionRun(screen, questions_data, title_font, option_font):
    random.shuffle(questions_data)  # 隨機打亂問題順序
    
    current_question_index = 0
    selected_option = -1  # 初始化選中的選項
    total_questions = len(questions_data)
    running = True
    hovered_option = None  # 初始化懸停選項
    answer_submitted = False  # 是否已提交答案
    show_feedback = False  # 是否顯示反饋
    feedback_message = ""  # 存儲反饋信息（答對了或錯誤）
    back_button_rect = config.back_button_image.get_rect(topleft=(250, 400))  # 将按钮放置在 (10, 10)
    # 渲染返回主菜单按钮图片
    screen.blit(config.back_button_image,back_button_rect)

    # 初始化分數
    score = 0

    previous_hovered_option = None  # 用于记录上一次的悬停选项

    while running:
        
        back_button_rect = config.back_button_image.get_rect(topleft=(250, 550))  # 将按钮放置在 (10, 10)
        screen.blit(config.qa_background,(0, 0))
        # 渲染返回主菜单按钮图片
        screen.blit(config.back_button_image,back_button_rect)
        render_score(screen, score, 125, 40, config.score_images, 50)  # 假設分數顯示在左上角
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检测是否点击了返回主菜单按钮
                if back_button_rect.collidepoint(event.pos):
                    running = False  # 停止当前聊天模式，退出到主菜单
                    return False, score # 退出 chat_mode 函数，回到主程序的状态管理

            if not answer_submitted:  # 只有在未提交答案時才處理事件
                if event.type == pygame.MOUSEMOTION:
                    hovered_option = handle_mouse_click(pygame.mouse.get_pos(), len(questions_data[current_question_index]['options']))

                    # 当 hovered_option 改变时，播放悬停音效
                    if hovered_option is not None and hovered_option != previous_hovered_option:
                        hover_sound.play()
                        previous_hovered_option = hovered_option  # 更新上次的悬停选项

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and hovered_option is not None:
                        selected_option = hovered_option
                        answer_submitted = True
                        
                        # # 播放点击气泡声
                        # bubble_sound.play()

                        # 判斷答案是否正確，並顯示反饋
                        if check_answer(questions_data[current_question_index], selected_option):
                            feedback_message = "correct"
                            score += 1  # 答對後增加分數
                            correct_sound.play()  # 播放正确答案音效
                        else:
                            feedback_message = "wrong"
                            wrong_sound.play()  # 播放错误答案音效
                        
                        show_feedback = True  # 觸發顯示反饋

        # 先渲染背景
        # screen.blit(config.qa_background, (0, 0))  # 重新繪製背景

        # 渲染問題和選項
        render_question_and_options(screen, questions_data[current_question_index], config.title_font, option_font, selected_option, hovered_option)

        # 使用自己的數字圖片顯示分數
        # render_score(screen, score, 125, 40, config.score_images, 50)  # 假設分數顯示在左上角
        pygame.display.flip()
        
        # 如果已提交答案，顯示反饋
        if show_feedback:
            if feedback_message == "correct":
                screen.blit(config.right_image, (30, 300))  # 顯示答對的圖片
            elif feedback_message == "wrong":
                screen.blit(config.wrong_image, (30, 300))  # 顯示答錯的圖片

            pygame.display.flip()  # 更新顯示
            
            pygame.time.wait(1000)

            current_question_index += 1  # 進入下一個問題
            if current_question_index < total_questions:
                selected_option = -1  # 重置選項
                answer_submitted = False  # 重置提交狀態
                show_feedback = False  # 關閉反饋顯示
                previous_hovered_option = None  # 重置上次的悬停选项
            else:
                print("所有問題已回答完畢!")
                return True, score  # 返回 True 和當前的分數，通知主程式進入結尾狀態

        pygame.display.flip()  # 更新顯示

    pygame.quit()
    return False, score  # 如果遊戲在中途退出，返回 False 和當前分數
