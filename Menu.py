import pygame
from defs import SCREEN_HEIGHT, SCREEN_WIDTH

class Menu:
    def __init__(self, screen, options) -> None:
        self.screen = screen
        self.options = options
        self.optionsRects = []
        self.FONT = pygame.font.Font(None, 36)

    def showMenu(self) -> None:
        self.screen.fill((0, 0, 0))
        self.optionsRects = []
        for i, text in enumerate(self.options):
            text_surface = self.FONT.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i*50))
            self.optionsRects.append(text_rect)
            self.screen.blit(text_surface, text_rect)
    
    def getClickedOption(self, position) -> None:
        for i, rect in enumerate(self.optionsRects):
            if rect.collidepoint(position):
                return self.options[i]
        return None