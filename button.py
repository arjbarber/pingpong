import pygame
import config
import os

def get_download_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(os.path.join('Assets','font.ttf'), size)

def getFont(name,size):
    return pygame.font.SysFont(name,size)

class Button():
    def __init__(self, image, x_pos, y_pos, text_input, win):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        if config.BUTTON_FONT_NAME == 'Press-Start-2P':
            self.text = get_download_font(config.BUTTON_FONT_SIZE).render(self.text_input, True, config.BUTTON_FONT_COLOR)
        else:
            self.text = getFont(config.BUTTON_FONT_NAME,config.BUTTON_FONT_SIZE).render(self.text_input, True, config.BUTTON_FONT_COLOR)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.win = win
        

    def update(self):
        self.win.blit(self.image, self.rect)
        self.win.blit(self.text, self.text_rect)
    
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            if config.BUTTON_FONT_NAME == 'Press-Start-2P':
                self.text = get_download_font(config.BUTTON_FONT_SIZE).render(self.text_input, True, config.BUTTON_FONT_HOVER_COLOR)
            else:
                self.text = getFont(config.BUTTON_FONT_NAME,config.BUTTON_FONT_SIZE).render(self.text_input, True, config.BUTTON_FONT_HOVER_COLOR)
        else:
            if config.BUTTON_FONT_NAME == 'Press-Start-2P':
                self.text = get_download_font(config.BUTTON_FONT_SIZE).render(self.text_input, True, config.BUTTON_FONT_COLOR)
            else:
                self.text = getFont(config.BUTTON_FONT_NAME,config.BUTTON_FONT_SIZE).render(self.text_input, True, config.BUTTON_FONT_COLOR)