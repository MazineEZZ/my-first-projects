import pygame, sys
from global_variables import *
from button import *

# Initialize
pygame.init()
FPS = 60
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
logo = pygame.image.load("images/Calculator logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Calculator")

# Sounds
sound1 = pygame.mixer.Sound("sounds/Calculator click.mp3")
sound2 = pygame.mixer.Sound("sounds/Calculator sound2.wav")

# Font
S_FONT = pygame.font.SysFont("Mono", 30) # Small Font
FONT = pygame.font.SysFont("Mono", 40) # Normal Font
B_FONT = pygame.font.SysFont("mono", 55) # Big Font
XB_FONT = pygame.font.SysFont("mono", 80) # X Big Font

# Button
symbol_color = ORANGE
symbol_color_S = ORANGE_SHADOW

# Background color variants
Orange_variant = ButtonInterface(10, WIDTH/4+50, 100, 50, ORANGE_SHADOW)
Green_Variant = ButtonInterface(WIDTH-110, WIDTH/4+50, 100, 50, GREEN_SHADOW)
Blue_Variant = ButtonInterface(WIDTH/2-100/2, WIDTH/4+50, 100, 50, BLUE_SHADOW)

def draw_gride():
    for line in range(0, 7):
        pygame.draw.line(screen, GREY, (0, line * tile_size), (WIDTH, line * tile_size))
        pygame.draw.line(screen, GREY, (line * tile_size,0), (line * tile_size,HEIGHT))

def settings_screen(button_layout, variant, text_box):
    # Back button
    Back_button = ButtonInterface(10, HEIGHT-(HEIGHT-10), 50,50, GREY, "images/BackButton.png")

    # Checkmark
    checkmark_img = pygame.image.load("images/Checkmark.png")

    # Text
    text = S_FONT.render("Background color : ", True, WHITE)
    box = TextInput(WIDTH/4+200,WIDTH/4+112.5, 50, 50)
    text_inside_box = S_FONT.render("Decimal places : ", True, WHITE)
    box.text = text_box

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Orange_variant.rect.collidepoint(event.pos):
                    sound1.play()
                    button_layout = ButtonCal(app_map, app_symbols, ORANGE, ORANGE_SHADOW)
                    variant = Orange_variant

                elif Green_Variant.rect.collidepoint(event.pos):
                    sound1.play()
                    button_layout = ButtonCal(app_map, app_symbols, GREEN, GREEN_SHADOW)
                    variant = Green_Variant

                elif Blue_Variant.rect.collidepoint(event.pos):
                    sound1.play()
                    button_layout = ButtonCal(app_map, app_symbols, BLUE, BLUE_SHADOW)
                    variant = Blue_Variant
                
                if box.rect.collidepoint(event.pos):
                    box.active = True
                else:
                    box.active = False

                if Back_button.rect.collidepoint(event.pos):
                    sound1.play()
                    return button_layout, variant, box.text

            if event.type == pygame.KEYDOWN:
                if box.active:
                    if event.key == pygame.K_BACKSPACE:
                        box.text = box.text[:-1]
                    else:
                        if len(box.text) < 1:
                            if event.unicode.isdigit() and 1 <= int(event.unicode) <= 6:
                                box.text += event.unicode

        if not box.active and not box.text:
            box.text = '4'
        screen.fill(BLACK)
        screen.blit(text, (10,WIDTH/4))
        screen.blit(text_inside_box, (10, WIDTH/4+125))
        Back_button.draw(screen, -2.5, +0.75)

        Orange_variant.draw(screen)
        Blue_Variant.draw(screen)
        Green_Variant.draw(screen)

        box.draw(screen)
        box.update(screen, FONT)
        
        screen.blit(checkmark_img, (variant.rect.x+100-40, variant.rect.y+17.5))
        pygame.display.update()

def Main_screen():
    button_layout = ButtonCal(app_map, app_symbols, symbol_color, symbol_color_S)
    variant = Orange_variant

    # text
    user_input = '0'
    solution = '0'

    # Boolean values
    first_time = True
    error = False

    # Buttons Interface
    Gear_button = ButtonInterface(WIDTH-60, HEIGHT-(HEIGHT-10), 50,50, GREY, "images/GearIcon.png")

    text_box = '4'

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if Gear_button.rect.collidepoint(event.pos):
                    Gear_button.color = GREY_SHADOW
                else:
                    Gear_button.color = GREY

                for rect in button_layout.tile_list:
                    if rect[1].collidepoint(event.pos):
                        if rect[3] == button_layout.symbol_color:
                            rect[0].fill(button_layout.symbol_color_S); rect[3] = button_layout.symbol_color_S
                        if rect[3] == button_layout.number_color:
                            rect[0].fill(button_layout.number_color_S); rect[3] = button_layout.number_color_S
                        if rect[3] == button_layout.C_color:
                            rect[0].fill(button_layout.C_color_S); rect[3] = button_layout.C_color_S

                    else:
                        if rect[3] == button_layout.symbol_color_S:
                            rect[0].fill(button_layout.symbol_color); rect[3] = button_layout.symbol_color
                        if rect[3] == button_layout.number_color_S:
                            rect[0].fill(button_layout.number_color); rect[3] = button_layout.number_color
                        if rect[3] == button_layout.C_color_S:
                            rect[0].fill(button_layout.C_color); rect[3] = button_layout.C_color

            if event.type == pygame.MOUSEBUTTONDOWN:
                if Gear_button.rect.collidepoint(event.pos):
                    sound1.play()
                    button_layout, variant, text_box = settings_screen(button_layout, variant, text_box) # change screens
                for rect in button_layout.tile_list:
                    if rect[1].collidepoint(event.pos):
                        sound2.play()
                        if rect[2] == "C":
                            user_input = '0'
                            solution = '0'
                            error = False
                            first_time = True
                        elif rect[2] == "=":
                            error = False
                            try:
                                new_x = user_input
                                new_x = new_x.replace("x", "*")
                                solution = eval(new_x)
                            except:
                                user_input = ''
                                error = True
                        else:
                            if first_time: user_input = ''; first_time = False
                            if len(user_input) < 15:
                                user_input += rect[2]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                    if len(user_input) == 0:
                        user_input = '0'
                        first_time = True
        screen.fill(BLACK)

        # Text
        numbers = B_FONT.render(user_input, True, WHITE)
        screen.blit(numbers, (20,20))

        # Error check
        if not error:
            results = XB_FONT.render(str(round(float(solution),int(text_box))), True, WHITE)
        else:
            results = XB_FONT.render("Error", True, WHITE)
        screen.blit(results, (WIDTH-20-results.get_width(), 100))

        # Button Interface draw
        Gear_button.draw(screen)

        # Buttons
        button_layout.show(screen, FONT)

        pygame.display.update() 
Main_screen()

