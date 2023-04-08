import pygame, sys
from debug import debug
from pygame.locals import *
import os
from tkinter import filedialog
import tkinter as tk

# Pygame setup
pygame.init()
SIZE = WIDTH, HEIGHT = (800, 600)
FPS = 120
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Paint")

# Color GUI
colors = [
    (255, 0, 0),      # red
    (255, 127, 0),    # orange
    (255, 255, 0),    # yellow
    (0, 255, 0),      # green
    (0, 255, 255),    # blue-green
    (0, 0, 255),      # blue
    (127, 0, 255),    # indigo
    (255, 0, 255),    # violet
    "black",
    (255, 63, 63),    # light red
    (255, 159, 63),   # light orange
    (255, 255, 63),   # light yellow
    (63, 255, 63),    # light green
    (63, 255, 255),   # light blue-green
    (63, 63, 255),    # light blue
    (159, 63, 255),   # light indigo
    (255, 63, 255),    # light violet
    "white"
]

color_list = []
color_size = 20
color_y = HEIGHT/8-5 # Y = 70
color_y_placement = 4 # If we draw the first three colors then we should move on to the next row and draw the other colors
count = 1
for i in range(len(colors)):
    rect = pygame.Rect(WIDTH-color_size*count-15, color_y/color_y_placement, color_size, color_size)
    if count >= len(colors)/2:
        count = 0
        color_y_placement = 2
    count += 1
    color_list.append((rect, colors[i]))

# Brush size gui
brush_size = 40
brushes = [[pygame.Rect(10 +(10 + brush_size) * i, (HEIGHT/8-5)/2-brush_size/2, brush_size, brush_size), 2.5*(i+1), False] for i in range(4)]
brushes[1][2] = True
# brushes = [Rect, circle radius, Is the brush active or not]

def bresenham_line(x0, y0, x1, y1):
    """Return a list of points on the line from (x0, y0) to (x1, y1)."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    points.append((x, y))
    return points

def paint(prev_pos, pos, B_size, color):
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if prev_pos: # If prev_pos isn't False
            line_points = bresenham_line(*prev_pos, *pos)
            for point in line_points:
                pygame.draw.circle(screen, color, point, B_size, 0)
        else:
            pygame.draw.circle(screen, color, pos, B_size, 0)
        prev_pos = pos
    else:
        if prev_pos:
            pygame.draw.circle(screen, color, prev_pos, B_size, 0)
        prev_pos = None

    return prev_pos

def draw_menu(color1):
    passif_color = pygame.Color("black")
    active_color = pygame.Color("lightskyblue2")

    pygame.draw.rect(screen, "#939393", [0,0, WIDTH, HEIGHT/8+5])
    pygame.draw.rect(screen, "#A8A8A8", [0,0, WIDTH, HEIGHT/8-5])

    # Color gui
    for color in color_list:
        pygame.draw.rect(screen, color[1], color[0])
        pygame.draw.rect(screen, "black", color[0],2)
    
    # Brush gui
    for i, brush in enumerate(brushes):
        pygame.draw.rect(screen, "black", brush[0],0, 2)
        pygame.draw.circle(screen, "white", (brush[0].x+brush[0].w/2, brush[0].y+brush[0].h/2), brush[1])
        if brush[2]:
            pygame.draw.rect(screen, active_color, brush[0],2, 2)
        else:
            pygame.draw.rect(screen, passif_color, brush[0],2, 2)

    pygame.draw.circle(screen, "black", (WIDTH/2, (HEIGHT/8+5)/2), 25)    
    pygame.draw.circle(screen, color1, (WIDTH/2, (HEIGHT/8+5)/2), 20)

def main():
    pos = (0,0)
    prev_pos = None  # track previous position
    color = "black"
    B_size = 5
    undo_stack = []
    in_contact = False

    # get the file name and path from the user
    root = tk.Tk()
    root.withdraw()


    white_rect = pygame.Rect(0, HEIGHT/8+5, WIDTH, HEIGHT-(HEIGHT/8+5))
    white_screen = screen.subsurface(white_rect)
    pygame.draw.rect(screen, "white", white_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if white_rect.collidepoint(event.pos):
                    in_contact = True
                else:
                    in_contact = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for color_rect in color_list:
                    if color_rect[0].collidepoint(event.pos):
                        color = color_rect[1]
                for brush in brushes:
                    if brush[0].collidepoint(event.pos):
                        B_size = brush[1]
                        for brus in brushes:
                            brus[2] = False
                        brush[2] = True
                if in_contact:
                    undo_stack.append(screen.copy())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.draw.rect(screen, "white", white_rect)
                if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if undo_stack:
                        screen.blit(undo_stack.pop(), (0, 0))
                if event.key == pygame.K_s:
                    file_path = filedialog.asksaveasfilename(defaultextension='.png')
                    if file_path:
                        pygame.image.save(white_screen, file_path)
                    

        if in_contact:
            prev_pos = paint(prev_pos, pos, B_size, color)
        draw_menu(color)

        pygame.display.update()
        clock.tick(FPS)

main()
