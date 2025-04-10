import pygame
from random import randint
pygame.init()
from math import sin, cos, atan, sqrt, pi
canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
canvas_rect = canvas.get_rect()
w_canvas = canvas_rect.right
h_canvas = canvas_rect.bottom
clock = pygame.time.Clock()
pygame.display.set_caption("Gravity Assist")
cah = True
page_scroll = 0
def window(background=False):
    global keys, mouse, mousepos, cah, page_scroll
    if background: canvas.fill(background)
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()[0]
    mousepos = pygame.mouse.get_pos()
    if keys[pygame.K_ESCAPE] and keys[pygame.K_0]: pygame.quit()
    if page_scroll < 0: page_scroll = 0
    up_track = False
    down_track = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                down_track = True
            if event.button == 5:
                up_track = True
    if keys[pygame.K_DOWN] or up_track: page_scroll += 20
    if keys[pygame.K_UP] or down_track: page_scroll -= 20
    if page_scroll < 0: page_scroll = 0
window()
def text(text, x, y, si, col, font="jungle adventurer", shadow=False):
    font = pygame.font.SysFont(font,si) 
    if shadow:
        texting = font.render(text, True, "black")
        canvas.blit(texting, (x-texting.get_width()/2+si/30,y+si/30))
    texting = font.render(text, True, col)
    canvas.blit(texting, (x-texting.get_width()/2,y))
space = pygame.transform.scale(pygame.image.load(f"images/space.jpg").convert_alpha(), (w_canvas, h_canvas))
class UFO():
    def __init__(self, x, y, r):
        self.r = r
        self.image = pygame.transform.scale(pygame.image.load(f"images/ufo_1.png").convert_alpha(), (r, r))
        self.rect = pygame.Rect(x, y, r, r)
        self.velx = 0
        self.vely = 0
        self.s = self.r/2-self.r/sqrt(8)
        self.smallrect = pygame.Rect(self.rect.x+self.s, self.rect.y+self.s, self.r/sqrt(2), self.r/sqrt(2))
    def line(self):
        pygame.draw.line(canvas, "white", (self.rect.x+self.r/2,self.rect.y+self.r/2), mousepos, 2)
        self.velx = int(mousepos[0] - (self.rect.x+self.r/2))//50
        self.vely = int(mousepos[1] - (self.rect.y+self.r/2))//50
    def launch(self):
        for planet in planets:
            dx = (planet.rect.centerx - self.rect.centerx)/50
            dy = (planet.rect.centery - self.rect.centery)/50
            c = dx**2 + dy**2
            G = planet.r*6.67/2500
            self.velx += dx*G/c
            self.vely += dy*G/c
        self.rect.x += self.velx
        self.rect.y += self.vely
        self.smallrect = pygame.Rect(self.rect.x+self.s, self.rect.y+self.s, self.r/sqrt(2), self.r/sqrt(2))
class Planet():
    def __init__(self, x, y, r, img):
        self.r = r
        self.image = pygame.transform.scale(pygame.image.load(f"images/planet_{img}.png").convert_alpha(), (r, r))
        self.rect = pygame.Rect(x, y, r, r)
        s = r/2 - r*sqrt((sqrt(2)-1)/8)
        self.smallrect = pygame.Rect(self.rect.x+s, self.rect.y+s, r*sqrt((sqrt(2)-1)/2), r*sqrt((sqrt(2)-1)/2))
for i in range(40):
        window()
        text("Monkey Games™", w_canvas/2, 50, 200, "white")
        pygame.draw.line(canvas, "red", (w_canvas/2, h_canvas/2), (w_canvas/2 + 200*cos(i/(2*pi)), h_canvas/2 - 200*sin(i/(2*pi))))
        pygame.display.update()
        clock.tick(40)
while True:
    window()
    if True:
        playing = True
        launch = False
        p = UFO(50,h_canvas-200,50)
        planets = [Planet(500, 500, 500, 1), Planet(50, 50, 300, 2), Planet(w_canvas-400, 250, 250, 3)]
        while playing:
            window()
            canvas.blit(space, (0,0))
            for planet in planets:
                canvas.blit(planet.image, planet.rect)
                if pygame.Rect.colliderect(p.smallrect, planet.smallrect) or not pygame.Rect.colliderect(canvas_rect, p.rect):
                    playing = False
            if launch: 
                    p.launch()
            if not launch: p.line()
            canvas.blit(p.image, p.rect)
            if mouse: launch = True
            pygame.display.update()
            clock.tick(60)
    pygame.display.update()
    clock.tick(60)