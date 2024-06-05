import pygame
import config


class Button:
    def __init__(self, x, y, width, height, text, callback, x_offset=0, y_offset=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.name = text
        self.callback = callback
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.on = False


    def update_name(self, new_name=None):
        if new_name is None:
            new_name = self.name
        self.text = new_name
        self.name = new_name

    def draw(self, screen, selected=False, x_offset=0, y_offset=0):
        text = config.font.render(self.text, True, config.text_color)
        text_pos = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        if self.on:
            color = config.button_hover_selected if selected else config.button_hover
        else:
            color = config.button_selected if selected else config.button_color
        pygame.draw.rect(screen, color, (self.x + x_offset, self.y + y_offset, self.width, self.height), 0, 3)
        screen.blit(text, text_pos.move(x_offset, y_offset))

    def update(self, events, x_offset=0, y_offset=0):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if self.x + x_offset < x < self.x + x_offset + self.width and self.y + y_offset < y < self.y + y_offset + self.height:
                    self.callback()
            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                if self.x + x_offset < x < self.x + x_offset + self.width and self.y + y_offset < y < self.y + y_offset + self.height:
                    self.on = True
                else:
                    self.on = False


class IconButton(Button):
    def __init__(self, x, y, width, height, callback, icon, x_offset=0, y_offset=0):
        super().__init__(x, y, width, height, '', callback, x_offset, y_offset)
        self.icon = pygame.image.load(icon)
        self.icon = pygame.transform.scale(self.icon, (self.height, self.height))
        self.icon_pos = self.icon.get_rect(center=(self.x + self.height // 2, self.y + self.height // 2)).move(0, 0)

    def draw(self, screen, selected=False, x_offset=0, y_offset=0):
        if self.on:
            color = config.button_hover_selected if selected else config.button_hover
        else:
            color = config.button_selected if selected else config.button_color
        pygame.draw.rect(screen, color, (self.x + x_offset, self.y + y_offset, self.width, self.height), 0, 5)
        screen.blit(self.icon, self.icon_pos.move(x_offset, y_offset))

class AddButton(Button):
    def draw(self, screen, selected=False, x_offset=0, y_offset=0):
        if self.on:
            color = config.button_hover_selected if selected else config.button_hover
        else:
            color = config.button_selected if selected else config.button_color
        rect = pygame.Rect(self.x + x_offset, self.y + y_offset, self.width, self.height)
        pygame.draw.rect(screen, color, rect)
        plus_width = 10
        plus_length = 30
        pygame.draw.rect(screen, config.add_button_color, (rect.centerx - plus_width // 2, rect.centery - plus_length // 2, plus_width, plus_length))
        pygame.draw.rect(screen, config.add_button_color, (rect.centerx - plus_length // 2, rect.centery - plus_width // 2, plus_length, plus_width))

class DeleteButton(Button):
    def draw(self, screen, selected=False, x_offset=0, y_offset=0):
        if self.on:
            color = config.button_hover_selected if selected else config.button_hover
        else:
            color = config.button_selected if selected else config.button_color
        rect = pygame.Rect(self.x + x_offset, self.y + y_offset, self.width, self.height)
        pygame.draw.rect(screen, color, rect)
        plus_width = 10
        plus_length = 30
        # pygame.draw.rect(screen, (255, 0, 0), (rect.centerx - plus_width // 2, rect.centery - plus_length // 2, plus_width, plus_length))
        pygame.draw.rect(screen, config.delete_button_color, (rect.centerx - plus_length // 2, rect.centery - plus_width // 2, plus_length, plus_width))


class ButtonGroup:
    def __init__(self, name, x, y, width, height, callback, buttons=None, is_addbutton=True):
        if buttons is None:
            buttons = []
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.surface = pygame.Surface((self.width, self.height-75))
        self.is_addbutton = is_addbutton

        self.buttons = []
        self.background_color = config.button_group_color
        self.scroll = 0
        self.scroll_speed = 0

        self.text = config.font.render(self.name, True, config.text_color)
        self.text_pos = self.text.get_rect(center=(self.width // 2, 30)).move(self.x, self.y)

        for button in buttons:
            self.add_button(button)

        self.selected = -1

        self.addbutton = AddButton(80, self.height-65, self.width - 95, 50, "Add",
                                   lambda: self.callback("add_new_item"))

        self.deletebutton = DeleteButton(15, self.height-65, 50, 50, "Delete",
                                   lambda: self.callback("delete_item"))

    def get_callback(self, i):
        def cb():
            self.selected = i
            self.callback(i)
        return cb

    def add_button(self, button):
        i = len(self.buttons)
        self.buttons.append(Button(15, len(self.buttons) * 60, self.width - 30, 50, button,
                                   self.get_callback(i)))
        self.selected = i

    def remove_button(self, button):
        self.buttons.pop(button)
        for i, button in enumerate(self.buttons):
            button.y = i * 60
            button.callback = self.get_callback(i)
            button.update_name()

    def update_button_name(self, new_name):
        self.buttons[self.selected].update_name(new_name)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL and self.x < pygame.mouse.get_pos()[0] < self.x + self.width and self.y < pygame.mouse.get_pos()[1] < self.y + self.height:
                self.scroll_speed += event.y * 10
        for button in self.buttons:
            button.update(events, self.x, self.y + 60 + self.scroll)
        if self.is_addbutton:
            self.addbutton.update(events, self.x, self.y)
            self.deletebutton.update(events, self.x, self.y)
        self.scroll += self.scroll_speed
        self.scroll_speed *= 0.9

        if self.scroll > 0:
            self.scroll *= 0.5
        max_limit = min(0, -60 * len(self.buttons) + self.height - 75 - 65)
        if self.scroll < max_limit:
            self.scroll = self.scroll + (max_limit - self.scroll)*0.5

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, (self.x, self.y, self.width, self.height), 0, 10)
        pygame.draw.rect(self.surface, self.background_color, (0, 0, self.width, self.height-75))
        screen.blit(self.text, self.text_pos)

        for i, button in enumerate(self.buttons):
            button.draw(self.surface, i == self.selected, y_offset=self.scroll)

        screen.blit(self.surface, (self.x, self.y+60))
        if self.is_addbutton:
            self.addbutton.draw(screen, x_offset=self.x, y_offset=self.y)
            self.deletebutton.draw(screen, x_offset=self.x, y_offset=self.y)


class EditButtonGroup(ButtonGroup):
    def __init__(self, name, x, y, width, height, callback, buttons=[], on_edit=lambda x: None, is_addbutton=True):
        super().__init__(name, x, y, width, height, callback, buttons, is_addbutton)
        self.on_edit = on_edit
        self.edit_active = True

    def update(self, events):
        super().update(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if self.x < x < self.x + self.width and self.y < y < self.y + 50:
                    self.edit_active = True
                else:
                    self.edit_active = False
            if self.edit_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.name:
                        self.name = self.name[:-1]
                    self.update_header_name()
                else:
                    self.name += event.unicode
                    self.update_header_name()

    def update_header_name(self):
        self.on_edit(self.name)
        self.text = config.font.render(self.name, True, config.text_color)
        self.text_pos = self.text.get_rect(center=(self.width // 2, 30)).move(self.x, self.y)

    def draw(self, screen):
        super().draw(screen)
        if self.edit_active:
            pygame.draw.rect(screen, config.editing_color, (self.x+10, self.y+50, self.width-20, 3))
            pygame.draw.rect(screen, config.editing_color, (self.text_pos.right, self.y + 15, 3, 30))
