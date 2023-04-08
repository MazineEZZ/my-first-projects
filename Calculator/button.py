import pygame
from global_variables import *

class ButtonCal:
    def __init__(self, data, symbols, symbol_color, symbol_color_S, number_color=WHITE, C_color=GREY):
        self.symbol_color = symbol_color
        self.number_color = number_color
        self.C_color = C_color
        self.symbol_color_S = symbol_color_S
        self.number_color_S = WHITE_SHADOW
        self.C_color_S = GREY_SHADOW

        self.tile_list = []
        self.outline_list = []

        row_count = 0
        for row_index, row in enumerate(data):
            cell_count = 0
            for cell_index, cell in enumerate(row):
                if cell == 'X':
                    self.get_info((tile_size, tile_size), self.symbol_color, cell_count, row_count, symbols[row_index][cell_index])
                    self.get_info_outline((tile_size, tile_size), cell_count, row_count)
                if cell == 'N':
                    self.get_info((tile_size, tile_size), self.number_color, cell_count, row_count, symbols[row_index][cell_index])
                    self.get_info_outline((tile_size, tile_size), cell_count, row_count)
                if cell == 'n':
                    self.get_info((tile_size*2, tile_size), self.number_color, cell_count, row_count, symbols[row_index][cell_index])
                    self.get_info_outline((tile_size*2, tile_size), cell_count, row_count)
                if cell == 'C':
                    self.get_info((tile_size, tile_size), self.C_color, cell_count, row_count, symbols[row_index][cell_index])
                    self.get_info_outline((tile_size, tile_size), cell_count, row_count)
                if cell == '=':
                    self.get_info((tile_size, tile_size), self.symbol_color, cell_count, row_count, symbols[row_index][cell_index])
                    self.get_info_outline((tile_size, tile_size), cell_count, row_count)

                cell_count += 1
            row_count += 1

    def get_info(self, tile_size_w_h, color, cell, row, symbol):
        surface = pygame.Surface(tile_size_w_h)
        surface.fill(color)
        rect = surface.get_rect()
        rect.x = cell * tile_size
        rect.y = row * tile_size
        button = [surface, rect, symbol, color]
        self.tile_list.append(button)
    
    def get_info_outline(self, tile_size_w_h, cell, row):
        rect = pygame.Rect(cell * tile_size, row * tile_size, tile_size_w_h[0], tile_size_w_h[1])
        self.outline_list.append(rect)

    def show(self, screen, FONT):
        for i, tile in enumerate(self.tile_list):
            screen.blit(tile[0], tile[1])
            text = FONT.render(tile[2], True, BLACK)
            screen.blit(text, (tile[1].x + tile[1].w/2 - text.get_width()/2, tile[1].y + tile[1].h/2 - text.get_height()/2))
            pygame.draw.rect(screen, BLACK, self.outline_list[i], 2)

class ButtonInterface:
    def __init__(self, x, y, width, height, color, picture_path=None):
        self.picture_path = picture_path
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        if self.picture_path: self.surf = pygame.image.load(picture_path)
    
    def draw(self, screen, movex=2.5, movey=2.5):
        pygame.draw.rect(screen, self.color, self.rect, 0, 8)
        if self.picture_path: screen.blit(self.surf, (self.rect.x+movex, self.rect.y+movey))

class TextInput:
    color_active = pygame.Color("lightskyblue3")
    color_passive = pygame.Color('grey15')

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ''
        self.active = False
    
    def draw(self, screen):
        if self.active: pygame.draw.rect(screen, self.color_active, self.rect,2,3)
        else: pygame.draw.rect(screen, self.color_passive, self.rect, 2, 3)
    
    def update(self, screen, FONT):
        text = FONT.render(self.text, True, WHITE)
        screen.blit(text, (self.rect.x+5, self.rect.y+5))
        self.rect.w = max(50, text.get_width() + 10)