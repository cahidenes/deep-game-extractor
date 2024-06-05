import pygame
from button import *
from record import *
import threading
from PIL import ImageGrab


class EditSettingsScreen:
    def __init__(self, save_record: list):
        self.record_string = ''
        self.record_active = False
        self.record_button = Button(600, 200, 150, 50, "Record", self.record)
        self.test_button = Button(600, 350, 150, 50, "Test", self.test)
        self.save = save_record
        self.back_button = Button(10, 10, 150, 50, "Back", self.back)

        self.settings_screens_group = ButtonGroup("Settings Screens", 15, 100, 250, 450,
                                                  self.settings_screens_button_press,
                                                  [x['name'] for x in self.save])

        self.settings_groups = []
        for item in self.save:
            self.settings_groups.append(EditButtonGroup(item['name'], 275, 100, 250, 450,
                                                       self.setting_button_press,
                                                       [x['name'] for x in item['settings']],
                                                       self.first_button_group_update_name))
            self.settings_groups[-1].selected = -1

        self.record_group = EditButtonGroup("Setting", 535, 100, 250, 450,
                                            self.record_button_press, ['Record', 'Test', 'Speedup', 'Mouse', 'Save'],
                                            self.update_setting_name, is_addbutton=False)

        self.current_recording = None
        self.speedup = 1
        self.include_mouse = True

        self.logo = pygame.image.load('assets/logo.png')
        self.logo = pygame.transform.scale(self.logo, (int(self.logo.get_width() * 0.05), int(self.logo.get_height() * 0.05)))

    def back(self):
        config.current_screen = MainMenuScreen()
        config.save_config()

    def update_setting_name(self, new_name):
        if self.record_active:
            self.settings_groups[self.settings_screens_group.selected].update_button_name(new_name)
            self.save[self.settings_screens_group.selected]['settings'][self.settings_groups[self.settings_screens_group.selected].selected]['name'] = new_name

    def record_wrapper(self):
        self.current_recording = record(True, True)

    def record_button_press(self, button):
        if button == 0:
            threading.Thread(target=self.record_wrapper, daemon=True).start()
        elif button == 1:
            threading.Thread(target=simulate, args=(self.current_recording, self.speedup, self.include_mouse), daemon=True).start()
        elif button == 2:
            index = config.speedup_list.index(self.speedup)
            index = (index + 1) % len(config.speedup_list)
            self.speedup = config.speedup_list[index]
            self.record_group.update_button_name('Speedup [' + str(self.speedup) + ']')
        elif button == 3:
            self.include_mouse = not self.include_mouse
            self.record_group.update_button_name('Mouse [' + ('ON' if self.include_mouse else 'OFF') + ']')
        elif button == 4:
            if self.record_active:
                self.save[self.settings_screens_group.selected]['settings'][self.settings_groups[self.settings_screens_group.selected].selected]['recording'] = self.current_recording
                self.save[self.settings_screens_group.selected]['settings'][self.settings_groups[self.settings_screens_group.selected].selected]['speedup'] = self.speedup
                self.save[self.settings_screens_group.selected]['settings'][self.settings_groups[self.settings_screens_group.selected].selected]['mouse'] = self.include_mouse
            else:
                self.save[self.settings_screens_group.selected]['enter'] = self.current_recording
                self.save[self.settings_screens_group.selected]['speedup'] = self.speedup
                self.save[self.settings_screens_group.selected]['mouse'] = self.include_mouse
            config.save_config()

    def first_button_group_update_name(self, new_name):
        self.settings_screens_group.update_button_name(new_name)
        self.save[self.settings_screens_group.selected]['name'] = new_name

    def settings_screens_button_press(self, button):
        if button == 'add_new_item':
            self.save.append({'name': 'New Settings', 'enter': '', 'settings': [], 'speedup': '1', 'mouse': True})
            self.settings_screens_group.add_button('New Settings')

            self.settings_groups.append(
                EditButtonGroup('New Settings', 275, 100, 250, 450, self.setting_button_press,
                                [], self.first_button_group_update_name)
            )
            self.settings_screens_group.selected = len(self.settings_groups) - 1
            self.settings_groups[self.settings_screens_group.selected].selected = -1

            self.current_recording = ''

            self.record_active = False
            self.record_group.name = 'New Settings'
            self.record_group.update_header_name()

            self.speedup = int(self.save[self.settings_screens_group.selected]['speedup'])
            self.record_group.selected = 2
            self.record_group.update_button_name('Speedup [' + str(self.speedup) + ']')

            self.include_mouse = bool(self.save[self.settings_screens_group.selected]['mouse'])
            self.record_group.selected = 3
            self.record_group.update_button_name('Mouse [' + ('ON' if self.include_mouse else 'OFF') + ']')

            self.record_group.selected = -1

        elif button == 'delete_item':
            del self.save[self.settings_screens_group.selected]
            del self.settings_groups[self.settings_screens_group.selected]
            self.settings_screens_group.remove_button(self.settings_screens_group.selected)
            self.settings_screens_group.selected = -1
            self.record_active = False
            self.record_group.name = ''
            self.record_group.update_header_name()
        else:
            self.settings_groups[button].edit_active = False
            self.settings_groups[button].selected = -1
            self.record_active = False
            self.record_group.name = self.settings_screens_group.buttons[button].name
            self.record_group.update_header_name()

            self.current_recording = self.save[button]['enter']

            self.speedup = int(self.save[button]['speedup'])
            self.record_group.selected = 2
            self.record_group.update_button_name('Speedup [' + str(self.speedup) + ']')

            self.include_mouse = bool(self.save[button]['mouse'])
            self.record_group.selected = 3
            self.record_group.update_button_name('Mouse [' + ('ON' if self.include_mouse else 'OFF') + ']')

            self.record_group.selected = -1

    def setting_button_press(self, button):
        if button == 'add_new_item':
            self.save[self.settings_screens_group.selected]['settings'].append({'name': 'New Setting', 'recording': '', 'speedup': '1', 'mouse': True})
            self.settings_groups[self.settings_screens_group.selected].add_button('New Setting')
            self.settings_groups[self.settings_screens_group.selected].selected = len(
                self.settings_groups[self.settings_screens_group.selected].buttons) - 1
            self.record_active = True
            self.record_group.name = 'New Setting'
            self.record_group.update_header_name()

            self.current_recording = ''

            self.speedup = int(self.save[self.settings_screens_group.selected]['speedup'])
            self.record_group.selected = 2
            self.record_group.update_button_name('Speedup [' + str(self.speedup) + ']')

            self.include_mouse = bool(self.save[self.settings_screens_group.selected]['mouse'])
            self.record_group.selected = 3
            self.record_group.update_button_name('Mouse [' + ('ON' if self.include_mouse else 'OFF') + ']')

            self.record_group.selected = -1

        elif button == 'delete_item':
            del self.save[self.settings_screens_group.selected]['settings'][self.settings_groups[self.settings_screens_group.selected].selected]
            self.settings_groups[self.settings_screens_group.selected].remove_button(self.settings_groups[self.settings_screens_group.selected].selected)
            self.settings_groups[self.settings_screens_group.selected].selected = -1
            self.record_active = False
            self.record_group.name = self.settings_screens_group.buttons[self.settings_screens_group.selected].name
            self.record_group.update_header_name()
        else:
            self.record_active = True
            self.record_group.name = self.settings_groups[self.settings_screens_group.selected].buttons[button].name
            self.record_group.update_header_name()
            self.current_recording = self.save[self.settings_screens_group.selected]['settings'][button]['recording']

            self.speedup = int(self.save[self.settings_screens_group.selected]['speedup'])
            self.record_group.selected = 2
            self.record_group.update_button_name('Speedup [' + str(self.speedup) + ']')

            self.include_mouse = bool(self.save[self.settings_screens_group.selected]['mouse'])
            self.record_group.selected = 3
            self.record_group.update_button_name('Mouse [' + ('ON' if self.include_mouse else 'OFF') + ']')

            self.record_group.selected = -1

    def record(self):
        pygame.display.set_mode((config.W, config.H), flags=pygame.HIDDEN)
        self.save_record.clear()
        self.save_record += record(include_time=False).split('0,p' + config.save_key + '0,r' + config.save_key)
        pygame.display.set_mode((config.W, config.H), flags=pygame.SHOWN)

    def test(self):
        pygame.display.set_mode((config.W, config.H), flags=pygame.HIDDEN)
        import time
        for i in self.save_record:
            simulate(i, self.speedup, self.include_mouse)
            time.sleep(2)
        pygame.display.set_mode((config.W, config.H), flags=pygame.SHOWN)

    def update(self, events):
        if self.settings_screens_group.selected != -1:
            self.record_group.update(events)
        self.settings_screens_group.update(events)
        if self.settings_screens_group.selected != -1:
            self.settings_groups[self.settings_screens_group.selected].update(events)
        self.back_button.update(events)

    def draw(self):
        config.screen.blit(self.logo, self.logo.get_rect(center=(config.W - 70, 50)))
        if self.settings_screens_group.selected != -1:
            self.record_group.draw(config.screen)
        self.settings_screens_group.draw(config.screen)
        if self.settings_screens_group.selected != -1:
            self.settings_groups[self.settings_screens_group.selected].draw(config.screen)
        self.back_button.draw(config.screen)


class MainMenuScreen:
    def __init__(self):
        self.count = 0
        self.back_button = Button(10, 10, 150, 50, "Back", self.back)
        self.configs_button = ButtonGroup("Configs", 15, 100, 250, 450,
                                          self.configs_button_press, [item['name'] for item in config.config])

        self.configs_groups = []
        self.current_recording = ''
        for item in config.config:
            self.configs_groups.append(EditButtonGroup(item['name'], 275, 100, 250, 450,
                                                       self.second_button_press,
                                                       ['Settings', 'Game Flow', 'Parameters', 'Start'],
                                                       is_addbutton=False, on_edit=self.update_first_button_group_button_name))

        self.include_mouse_move = True
        self.speedup = 1
        self.record_group = ButtonGroup("Setting", 535, 100, 250, 450,
                                        self.record_button_press, ['Record', 'Test', 'Speedup [1]', 'Mouse [ON]', 'Save'], is_addbutton=False)

        self.parameters_group = ButtonGroup("Parameters", 535, 100, 250, 450,
                                            self.parameters_button_press,
                                            ['Split Button', 'Terminate Button', 'Cancel Button', 'SS Region'], is_addbutton=False)
        self.logo = pygame.image.load('assets/logo.png')
        self.logo = pygame.transform.scale(self.logo, (int(self.logo.get_width() * 0.05), int(self.logo.get_height() * 0.05)))

    def back(self):
        config.current_screen = IntroScreen()
        config.save_config()

    def parameters_button_press(self, button):
        if button == 3:
            config.current_screen = ScreenshotParametersScreen(config.config[self.configs_button.selected]['config']['ss_bbox'])
        else:
            threading.Thread(target=self.get_key_wrapper, daemon=True, args=(button,)).start()

    def update_first_button_group_button_name(self, new_name):
        self.configs_button.update_button_name(new_name)
        config.config[self.configs_button.selected]['name'] = new_name

    def record_wrapper(self):
        self.current_recording = record(True, True)

    def get_key_wrapper(self, button):
        self.parameters_group.update_button_name('Waiting Key...')
        key = record_key()
        if button == 0:
            s = 'Split'
            config.config[self.configs_button.selected]['config']['parameters']['split'] = key
        elif button == 1:
            s = 'Terminate'
            config.config[self.configs_button.selected]['config']['parameters']['terminate'] = key
        elif button == 2:
            s = 'Cancel'
            config.config[self.configs_button.selected]['config']['parameters']['ss'] = key
        self.parameters_group.update_button_name(s + ' (' + get_key_name(key) + ')')
        self.parameters_group.selected = -1

    def record_button_press(self, button):
        if button == 0:
            threading.Thread(target=self.record_wrapper, daemon=True).start()
        elif button == 1:
            threading.Thread(target=simulate, args=(self.current_recording, self.speedup, self.include_mouse_move), daemon=True).start()
        elif button == 2:
            index = config.speedup_list.index(self.speedup)
            index = (index+1) % len(config.speedup_list)
            self.speedup = config.speedup_list[index]
            self.record_group.update_button_name('Speedup [' + str(self.speedup) + ']')
        elif button == 3:
            if self.include_mouse_move:
                self.include_mouse_move = False
                self.record_group.update_button_name('Mouse [OFF]')
            else:
                self.include_mouse_move = True
                self.record_group.update_button_name('Mouse [ON]')
        elif button == 4:
            print(self.current_recording)
            config.config[self.configs_button.selected]['config']['game_flow'] = self.current_recording
            config.config[self.configs_button.selected]['config']['speedup'] = self.speedup
            config.config[self.configs_button.selected]['config']['mouse'] = self.include_mouse_move

    def configs_button_press(self, button):
        if button == 'add_new_item':
            self.configs_groups.append(EditButtonGroup('New Config', 275, 100, 250, 450,
                                                       self.second_button_press,
                                                       ['Settings', 'Game Flow', 'Parameters', 'Start'],
                                                       is_addbutton=False, on_edit=self.update_first_button_group_button_name))
            self.configs_button.add_button('New Config')
            config.config.append({'name': 'New Config', 'config': {'game_flow': '', 'speedup': '1', 'mouse': True, 'ss_bbox': [0.0, 1.0, 0.0, 1.0], 'settings': [], 'parameters': {'split': 'ky', 'terminate': 'kz', 'ss': 'kA'}}})
        elif button == 'delete_item':
            del config.config[self.configs_button.selected]
            del self.configs_groups[self.configs_button.selected]
            self.configs_button.remove_button(self.configs_button.selected)
            self.configs_button.selected = -1
        else:
            self.current_recording = config.config[button]['config']['game_flow']
        config.save_key = config.config[self.configs_button.selected]['config']['parameters']['split']
        config.end_key = config.config[self.configs_button.selected]['config']['parameters']['terminate']
        config.ss_key = config.config[self.configs_button.selected]['config']['parameters']['ss']

    def second_button_press(self, button):
        if button == 0:
            config.current_screen = EditSettingsScreen(config.config[self.configs_button.selected]['config']['settings'])
        elif button == 1:
            self.current_recording = config.config[self.configs_button.selected]['config']['game_flow']

            self.speedup = int(config.config[self.configs_button.selected]['config']['speedup'])
            self.record_group.selected = 2
            self.record_group.update_button_name('Speedup [' + str(self.speedup) + ']')

            self.include_mouse_move = bool(config.config[self.configs_button.selected]['config']['mouse'])
            self.record_group.selected = 3
            self.record_group.update_button_name('Mouse [' + ('ON' if self.include_mouse_move else 'OFF') + ']')

            self.record_group.selected = -1
        elif button == 2:
            self.parameters_group.selected = 0
            self.parameters_group.update_button_name('Split (' + get_key_name(config.config[self.configs_button.selected]['config']['parameters']['split']) + ')')
            self.parameters_group.selected = 1
            self.parameters_group.update_button_name('Terminate (' + get_key_name(config.config[self.configs_button.selected]['config']['parameters']['terminate']) + ')')
            self.parameters_group.selected = 2
            self.parameters_group.update_button_name('Cancel (' + get_key_name(config.config[self.configs_button.selected]['config']['parameters']['ss']) + ')')
            self.parameters_group.selected = -1
        elif button == 3:
            pygame.display.iconify()
            c = config.config[self.configs_button.selected]['config']
            settings_list = []
            flow = split_recording(c['game_flow'], config.save_key)
            for settings_item in c['settings']:
                enter, exit = split_recording(settings_item['enter'], config.save_key)
                for setting in settings_item['settings']:
                    settings_list.append([merge_recordings(
                        enter, x, exit,
                        speedups=[settings_item['speedup'], setting['speedup'], settings_item['speedup']],
                        mouses=[settings_item['mouse'], setting['mouse'], settings_item['mouse']],
                    ) for x in split_recording(setting['recording'], config.save_key)])
            import os, datetime
            save_name = f'{config.config[self.configs_button.selected]["name"]}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
            os.mkdir('screenshots/' + save_name)
            sample = ImageGrab.grab()
            w, h = sample.size
            bbox = [int(w*x) for x in c['ss_bbox'][:2]] + [int(h*x) for x in c['ss_bbox'][2:]]
            bbox[1], bbox[2] = bbox[2], bbox[1]
            self.count = 0
            time.sleep(1)
            self.execute_flow((flow, c['speedup'], c['mouse']), settings_list, save_name, bbox)

    def execute_flow(self, flows, settings_list, filename, bbox):
        if not settings_list:
            for i in range(len(flows[0])):
                if simulate(flows[0][i], flows[1], flows[2], include_sound=False):
                    return True
                if i != len(flows)-1:
                    image = ImageGrab.grab(bbox=bbox)
                    image.save(f'screenshots/{filename}/image{self.count}.png')
                    self.count += 1
        else:
            for setting in settings_list[0]:
                if self.execute_flow(flows, settings_list[1:], filename, bbox):
                    return True
                print('simulating:', setting)
                if simulate(setting, include_sound=False):
                    return True
        return False

    def update(self, events):
        self.configs_button.update(events)
        self.back_button.update(events)
        if self.configs_button.selected != -1:
            self.configs_groups[self.configs_button.selected].update(events)

        if self.configs_button.selected != -1 and self.configs_groups[self.configs_button.selected].selected == 1:
            self.record_group.update(events)

        if self.configs_button.selected != -1 and self.configs_groups[self.configs_button.selected].selected == 2:
            self.parameters_group.update(events)

    def draw(self):
        # title = config.header_font.render("Deep Game Extractor", True, config.text_color)
        # config.screen.blit(title, title.get_rect(center=(config.W // 2, 100)))
        config.screen.blit(self.logo, self.logo.get_rect(center=(config.W - 70, 50)))
        self.configs_button.draw(config.screen)
        self.back_button.draw(config.screen)

        if self.configs_button.selected != -1:
            self.configs_groups[self.configs_button.selected].draw(config.screen)

        if self.configs_button.selected != -1 and self.configs_groups[self.configs_button.selected].selected == 1:
            self.record_group.draw(config.screen)

        if self.configs_button.selected != -1 and self.configs_groups[self.configs_button.selected].selected == 2:
            self.parameters_group.draw(config.screen)


class ScreenshotParametersScreen:
    def __init__(self, save):
        from PIL import ImageGrab
        ss = ImageGrab.grab()
        self.save = save
        print(self.save)
        self.ss_surface = pygame.image.fromstring(ss.tobytes(), ss.size, ss.mode).convert()

        self.width = self.ss_surface.get_width()
        self.height = self.ss_surface.get_height()
        scale = min((config.W-100) / self.width, (config.H-100) / self.height)
        self.width *= scale
        self.height *= scale
        self.ss_surface = pygame.transform.scale(self.ss_surface, (int(self.width), int(self.height)))
        self.ss_x = (config.W - self.width) // 2
        self.ss_y = (config.H - self.height) // 2
        self.selection_x1 = self.ss_x + self.width*self.save[0]
        self.selection_x2 = self.ss_x + self.width*self.save[1]
        self.selection_y1 = self.ss_y + self.height*self.save[2]
        self.selection_y2 = self.ss_y + self.height*self.save[3]
        self.holding = -1

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.save[0] = (self.selection_x1 - self.ss_x) / self.width
                    self.save[1] = (self.selection_x2 - self.ss_x) / self.width
                    self.save[2] = (self.selection_y1 - self.ss_y) / self.height
                    self.save[3] = (self.selection_y2 - self.ss_y) / self.height
                    config.current_screen = MainMenuScreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                d1 = (x - self.selection_x1) ** 2 + (y - self.selection_y1) ** 2
                d2 = (x - self.selection_x2) ** 2 + (y - self.selection_y1) ** 2
                d3 = (x - self.selection_x1) ** 2 + (y - self.selection_y2) ** 2
                d4 = (x - self.selection_x2) ** 2 + (y - self.selection_y2) ** 2
                if min(d1, d2, d3, d4) < 100:
                    self.holding = [d1, d2, d3, d4].index(min(d1, d2, d3, d4))
            elif event.type == pygame.MOUSEBUTTONUP:
                self.holding = -1
            elif event.type == pygame.MOUSEMOTION:
                if self.holding != -1:
                    x, y = pygame.mouse.get_pos()
                    if self.holding == 0:
                        self.selection_x1 = max(self.ss_x, min(x, self.selection_x2-3))
                        self.selection_y1 = max(self.ss_y, min(y, self.selection_y2-3))
                    elif self.holding == 1:
                        self.selection_x2 = min(self.ss_x+self.width, max(x, self.selection_x1+3))
                        self.selection_y1 = max(self.ss_y, min(y, self.selection_y2-3))
                    elif self.holding == 2:
                        self.selection_x1 = max(self.ss_x, min(x, self.selection_x2-3))
                        self.selection_y2 = min(self.ss_y+self.height, max(y, self.selection_y1+3))
                    elif self.holding == 3:
                        self.selection_x2 = min(self.ss_x+self.width, max(x, self.selection_x1+3))
                        self.selection_y2 = min(self.ss_y+self.height, max(y, self.selection_y1+3))

    def draw(self):
        config.screen.blit(self.ss_surface, (self.ss_x, self.ss_y))
        text = config.font.render("Press Enter to confirm", True, config.text_color)
        config.screen.blit(text, text.get_rect(center=(config.W // 2, config.H - 50)))

        pygame.draw.rect(config.screen, config.screenshot_handle, (self.selection_x1, self.selection_y1, self.selection_x2 - self.selection_x1, self.selection_y2 - self.selection_y1), 2)
        pygame.draw.circle(config.screen, config.screenshot_handle, (self.selection_x1, self.selection_y1), 10)
        pygame.draw.circle(config.screen, config.screenshot_handle, (self.selection_x2, self.selection_y1), 10)
        pygame.draw.circle(config.screen, config.screenshot_handle, (self.selection_x1, self.selection_y2), 10)
        pygame.draw.circle(config.screen, config.screenshot_handle, (self.selection_x2, self.selection_y2), 10)

class IntroScreen:
    def __init__(self):
        self.logo = pygame.image.load('assets/logo.png')
        self.logo = pygame.transform.scale(self.logo, (int(self.logo.get_width() * 0.2), int(self.logo.get_height() * 0.2)))

        self.start_button = Button(config.W//3 - 100, 400, 200, 100, "Start", self.start)
        self.github_button = Button(config.W//3*2 -100, 400, 200, 100, "GitHub", self.github)
        self.theme_button = IconButton(10, 10, 50, 50, self.theme, 'assets/theme.png')

    def theme(self):
        if config.theme == 'light':
            config.theme = 'dark'
        else:
            config.theme = 'light'
        config.update_colors()

    def start(self):
        config.current_screen = MainMenuScreen()

    def github(self):
        import webbrowser
        webbrowser.open('www.github.com')

    def update(self, events):
        self.start_button.update(events)
        self.github_button.update(events)
        self.theme_button.update(events)

    def draw(self):
        config.screen.blit(self.logo, self.logo.get_rect(center=(config.W // 2, 200)))
        self.start_button.draw(config.screen)
        self.github_button.draw(config.screen)
        self.theme_button.draw(config.screen)
