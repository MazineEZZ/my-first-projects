import pygame, sys

# Pygame setup
pygame.init()
SIZE = WIDTH, HEIGHT = (400, 475)
FPS = 60
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("BMI calculator")

# Fonts
XB_FONT = pygame.font.SysFont("bahnschrift", 150) # X Big font
B_FONT = pygame.font.SysFont("bahnschrift", 80) # Big font
S_FONT = pygame.font.SysFont("bahnschrift", 25) # Small font
weight_text = S_FONT.render("Weight: (kg)", True, "white")
height_text = S_FONT.render("Height: (cm)", True, "white")
BMI_text = B_FONT.render("BMI", True, "white")

class Button():
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = S_FONT.render(text, True, "black")
    
    def draw(self):
        pygame.draw.rect(screen, "white", self.rect, 0, 8)
        screen.blit(self.text, (self.rect.x+5, self.rect.y + (self.text.get_height()/2)-7.5))

class TextInput():
    color_active = pygame.Color("lightskyblue3")
    color_passive = pygame.Color("gray15")

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ''
        self.active = False

    def reset(self):
        self.text = ''
        self.active = False

    def update(self):
        if self.active: pygame.draw.rect(screen, self.color_active, self.rect, 2,2)
        else: pygame.draw.rect(screen, self.color_passive, self.rect, 2,2)

    def draw(self):
        text_surface = S_FONT.render(self.text, True, "white")
        screen.blit(text_surface, (self.rect.x +5, self.rect.y + 5))
        self.rect.w = max(100, text_surface.get_width() + 10)

def calculate_BMI(weight, height):
    return int(weight)/((int(height)/100)**2)

def BodyMass(BMI):
    if BMI == 0:
        return ("Type your weight and height", 'white')
    elif BMI < 18.5:
        return ("Underweight", "#87B1D9")
    elif 18.5 <= BMI < 25:
        return ("Normal weight", "#3DD365")
    elif 25 <= BMI < 30:
        return ("Overweight", "#EEE133")
    elif 30 <= BMI < 35:
        return ("Obese", "#FD802E")
    elif 35 <= BMI or BMI > 40:
        return ("Extremely obese", "#F95353")


def main():
    # Text input functions
    box_width, box_height = 140, 32
    box_w = TextInput(WIDTH/4-weight_text.get_width()/2, (HEIGHT/2-weight_text.get_height()/2+140/4)-75, box_width, box_height)
    box_h = TextInput(WIDTH/2+height_text.get_width()/2, (HEIGHT/2-height_text.get_height()/2+140/4)-75, box_width, box_height)
    boxes = [box_w, box_h]

    # Button functions
    calculate_button_text = Button(WIDTH/2-160/2, HEIGHT-80,160,32, "Calculate BMI")
    buttons = [calculate_button_text]

    BMI_value = 00.0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in boxes:
                    if box.rect.collidepoint(event.pos): box.active = True; box.text = ''
                    else: box.active = False
                for button in buttons:
                    if button.rect.collidepoint(event.pos) and boxes[0].text and boxes[1].text:
                        BMI_list = []
                        for box in boxes:
                            BMI_list.append(box.text)
                        BMI_value = calculate_BMI(BMI_list[0], BMI_list[1])
                    else: 0 
            if event.type == pygame.KEYDOWN:
                for box in boxes:
                    if box.active:
                        if event.key == pygame.K_BACKSPACE:
                            box.text = box.text[:-1]
                        else:
                            if len(box.text) < 3:
                                if event.unicode.isdigit():
                                    box.text += event.unicode

        # Text
        bodymass = BodyMass(BMI_value)
        BMI = XB_FONT.render(f"{round(BMI_value,1)}", True, "white")
        BodyMass_comment = S_FONT.render(bodymass[0], True, bodymass[1])

        screen.fill("black")

        screen.blit(BMI_text, (WIDTH/2-BMI_text.get_width()/2,10))
        screen.blit(weight_text, (WIDTH/4-(weight_text.get_width()/2)-10,HEIGHT/2-(weight_text.get_height()/2)-75))
        screen.blit(height_text, (WIDTH/2+(height_text.get_width()/2)-10,(HEIGHT/2-height_text.get_height()/2)-75))
        screen.blit(BMI, (WIDTH/2-(BMI.get_width()/2),(HEIGHT/2)-15))
        screen.blit(BodyMass_comment, (WIDTH/2-(BodyMass_comment.get_width()/2), HEIGHT-40))
        
        for box in boxes:
            box.update()
            box.draw()
        
        # Button
        calculate_button_text.draw()

        pygame.display.update()

main()