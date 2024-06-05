import pygame
import json

save_key = 'ky'
end_key = 'kz'
cancel_key = 'kA'
font = pygame.font.Font('assets/fonts/static/Montserrat-Medium.ttf', 18)
header_font = pygame.font.Font('assets/fonts/static/Montserrat-Medium.ttf', 54)
W = 800
H = 600
config_file = 'config.json'
current_screen = None
screen = pygame.display.set_mode((W, H))
speedup_list = [1, 2, 3, 4, 5, 10, 1000]


def update_colors():
    global button_color, button_selected, button_hover, button_hover_selected, button_push, button_push_selected,\
        add_button_color, delete_button_color, button_group_color, background, text_color, screenshot_handle, editing_color
    if theme == 'light':
        button_color = (240, 240, 240)  # #F0F0F0
        button_selected = (70, 130, 180)  # #4682B4
        button_hover = (220, 220, 220)  # #DCDCDC
        button_hover_selected = (100, 149, 237)  # #6495ED
        button_push = (211, 211, 211)  # #D3D3D3
        button_push_selected = (30, 144, 255)  # #1E90FF
        add_button_color = (50, 205, 50)  # #32CD32
        delete_button_color = (255, 69, 0)  # #FF4500
        button_group_color = (192, 192, 192)  # #C0C0C0
        background = (255, 255, 255)  # #FFFFFF
        text_color = (0, 0, 0)  # #000000
        screenshot_handle = (70, 130, 180)  # #4682B4
        editing_color = (255, 255, 255)  # #FFFFFF
    elif theme == 'dark':
        button_color = (50, 50, 50)  # #323232
        button_selected = (70, 130, 180)  # #4682B4
        button_hover = (80, 80, 80)  # #505050
        button_hover_selected = (100, 149, 237)  # #6495ED
        button_push = (60, 60, 60)  # #3C3C3C
        button_push_selected = (30, 144, 255)  # #1E90FF
        add_button_color = (50, 205, 50)  # #32CD32
        delete_button_color = (255, 69, 0)  # #FF4500
        button_group_color = (70, 70, 70)  # #464646
        background = (30, 30, 30)  # #1E1E1E
        text_color = (224, 224, 224)  # #E0E0E0
        screenshot_handle = (70, 130, 180)  # #4682B4
        editing_color = (50, 50, 50)  # #323232


# colors
theme = 'dark'
update_colors()

with open(config_file, 'r') as file:
    config = json.load(file)


def save_config():
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)
