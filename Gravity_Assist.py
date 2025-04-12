import pygame
from random import randint
pygame.init()
from math import sin, cos, sqrt, pi
canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
canvas_rect = canvas.get_rect()
w_canvas = canvas_rect.right
h_canvas = canvas_rect.bottom
clock = pygame.time.Clock()
pygame.display.set_caption("Gravity Assist")
page_scroll = 0
can = True
def window(background=False):
    global keys, mouse, mousepos, page_scroll
    if background: canvas.fill(background)
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()[0]
    mousepos = pygame.mouse.get_pos()
    if keys[pygame.K_ESCAPE]: pygame.quit()
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
back_arrow = pygame.image.load("images/arrow.png").convert_alpha()
back_rect = pygame.Rect(0,0,100,100)
class UFO():
    def __init__(self, x, y, r):
        self.r = r
        self.image = pygame.transform.scale(pygame.image.load(f"images/ufo_{skins['UFO'][0]}.png").convert_alpha(), (r, r))
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
class Goal():
    def __init__(self, x, y ,r):
        self.rect = pygame.Rect(x, y, r, r)
        self.image = pygame.transform.scale(pygame.image.load(f"images/spaceship_{skins['Spaceship'][0]}.png").convert_alpha(), (r, r))
class Opening_icons():
    def __init__(self, name, pos):
        self.name = name
        self.rect = pygame.Rect(pos[0], pos[1], 150, 150)
        self.img = pygame.image.load(f"images/{name}_icon.png")
        self.selection = False
open_icons = [Opening_icons("Skins", [w_canvas/2+250, h_canvas/2-75]), Opening_icons("Levels", [w_canvas/2-400, h_canvas/2-75]), Opening_icons("Designer", [w_canvas-300, h_canvas-300])]
for i in range(40):
        window()
        text("Monkey Games™", w_canvas/2, 50, 200, "white")
        pygame.draw.line(canvas, "red", (w_canvas/2, h_canvas/2), (w_canvas/2 + 200*cos(i/(2*pi)), h_canvas/2 - 200*sin(i/(2*pi))))
        pygame.display.update()
        clock.tick(40)
play = False
level = 1
levels = [
    [(50,150,150), (w_canvas-200,h_canvas-200,150), [(w_canvas/2-200, h_canvas/2-200, 400)]],
    [(50,150,100), (w_canvas-200,200,100), [(w_canvas/2-300, 50, 600), (w_canvas-300, h_canvas-300, 150)]],
    [(50,h_canvas-200,50), (w_canvas-500, h_canvas-150, 100), [(500, 500, 500), (50, 50, 300), (w_canvas-400, 250, 250)]],
    [(w_canvas-150,50,50), (300, h_canvas/2+175, 75), [(400, 500, 200), (150, 50, 500), (w_canvas-800, 250, 800)]]
    ]
d_levels = []
skins = {"UFO":[1,5],"Spaceship":[1,1], "Space":[1,3]}
space = pygame.transform.scale(pygame.image.load(f"images/space_{skins['Space'][0]}.png").convert_alpha(), (w_canvas, h_canvas))
cc = "UFO"
while True:
    window()
    canvas.blit(space, (0,0))
    text("Gravity Assist", w_canvas/2, 50, 300, "white", shadow=True)
    play_rect = pygame.Rect(w_canvas/2 -125, h_canvas/2 - 125, 250, 250)
    pygame.draw.rect(canvas, "green", play_rect)
    pygame.draw.polygon(canvas, "black",[(w_canvas/2 + 100,h_canvas/2),(w_canvas/2 - 100, h_canvas/2 - 100),(w_canvas/2 - 100, h_canvas/2 + 100)])
    pygame.draw.rect(canvas, "black", play_rect, width=5)
    for i in open_icons:
        canvas.blit(i.img, i.rect)
        text(i.name, i.rect.x+75, i.rect.bottom+10, 50, "white")
    if mouse or keys[pygame.K_RETURN]:
        if play_rect.collidepoint(mousepos) or keys[pygame.K_RETURN]:
            play = True
            elvle = level-1
            slevel = levels
    if mouse:
        page_scroll = 0
        can = False
        if open_icons[0].rect.collidepoint(mousepos):
            while True:
                window("grey")
                canvas.blit(back_arrow, back_rect)
                sc = 0
                for skin in skins:
                    skin_rect = pygame.Rect(0,250+200*sc,150,150)
                    canvas.blit(pygame.transform.scale(pygame.image.load(f"images/{skin}_{skins[skin][0]}.png").convert_alpha(), (150,150)), skin_rect)
                    if skin == cc:
                        pygame.draw.rect(canvas, "green", skin_rect, width=5)
                    if mouse:
                        if skin_rect.collidepoint(mousepos) and can:
                            cc = skin
                            can = False
                    else: can = True
                    sc += 1
                for skin in range(skins[cc][1]):
                    skin_rect = pygame.Rect(w_canvas/5*((skin%4)+1)-75,250+200*int(skin/4)-page_scroll,150,150)
                    if skin+1 == skins[cc][0]:
                        pygame.draw.rect(canvas, "green", skin_rect)
                    else:
                        pygame.draw.rect(canvas, "orange", skin_rect)
                    canvas.blit(pygame.transform.scale(pygame.image.load(f"images/{cc}_{skin+1}.png").convert_alpha(), (150,150)), skin_rect)
                    if skin+1 == skins[cc][0]:
                        pygame.draw.rect(canvas, "green", skin_rect, width=5)
                    if mouse:
                        if skin_rect.collidepoint(mousepos) and can:
                            skins[cc][0] = skin+1
                            can = False
                            space = pygame.transform.scale(pygame.image.load(f"images/space_{skins['Space'][0]}.png").convert_alpha(), (w_canvas, h_canvas))
                    else:
                        can = True
                text("Skin Selection", w_canvas/2, 50, 200, "white", shadow=True)
                text(cc, w_canvas/2, 175, 100, "white", shadow=True)
                if mouse:
                    if back_rect.collidepoint(mousepos) and can:
                        break
                else: can = True
                pygame.display.update()
                clock.tick(60)
        if open_icons[1].rect.collidepoint(mousepos):
            eve = True
            while eve:
                window("grey")
                canvas.blit(back_arrow, back_rect)
                for elvle in range(len(levels)):
                    elvle_rect = pygame.Rect(w_canvas/5*((elvle%4)+1)-75,250+200*int(elvle/4)-page_scroll,150,150)
                    if level > elvle:
                        pygame.draw.rect(canvas, "blue", elvle_rect)
                        if mouse:
                            if elvle_rect.collidepoint(mousepos) and can:
                                play = True
                                eve = False
                                can = False
                                slevel = levels
                                break
                        else:
                            can = True
                    pygame.draw.rect(canvas, "black", elvle_rect, width=5)
                    text(str(elvle+1), elvle_rect.x+75, elvle_rect.y+25, 150, "black")
                text("Level Selection", w_canvas/2, 50, 200, "white", shadow=True)
                if mouse:
                    if back_rect.collidepoint(mousepos):
                        break
                pygame.display.update()
                clock.tick(60)
        if open_icons[2].rect.collidepoint(mousepos):
            eve = True
            while eve:
                window("grey")
                canvas.blit(back_arrow, back_rect)
                add_rect = pygame.Rect(w_canvas/5-75,250-page_scroll,150,150)
                pygame.draw.rect(canvas, "green", add_rect)
                pygame.draw.rect(canvas, "black", add_rect, width=5)
                text("+", add_rect.x+75, add_rect.y+12.5, 150, "black")
                for elvle in range(len(d_levels)):
                    dl_rect = pygame.Rect(w_canvas/5*(((elvle+1)%4)+1)-75,250+200*int((elvle+1)/4)-page_scroll,150,150)
                    pygame.draw.rect(canvas, "green", dl_rect)
                    if mouse:
                        if dl_rect.collidepoint(mousepos) and can:
                            play = True
                            eve = False
                            can = False
                            slevel = d_levels
                            break
                    else:
                        can = True
                    pygame.draw.rect(canvas, "black", dl_rect, width=5)
                    text(str(elvle+1), dl_rect.x+75, dl_rect.y+25, 150, "black")
                text("Level Designer", w_canvas/2, 50, 200, "white", shadow=True)
                if mouse:
                    if back_rect.collidepoint(mousepos):
                        break
                pygame.display.update()
                clock.tick(60)
    if play:
        playing = True
        launch = False
        p = UFO(slevel[elvle][0][0], slevel[elvle][0][1], slevel[elvle][0][2])
        goal = Goal(slevel[elvle][1][0], slevel[elvle][1][1], slevel[elvle][1][2])
        planets = []
        for i in range(len(slevel[elvle][2])):
            planets.append(Planet(slevel[elvle][2][i][0], slevel[elvle][2][i][1], slevel[elvle][2][i][2], i+1))
        while playing:
            window()
            canvas.blit(space, (0,0))
            for planet in planets:
                canvas.blit(planet.image, planet.rect)
                if pygame.Rect.colliderect(p.smallrect, planet.smallrect) or keys[pygame.K_r]:
                    playing = False
            if launch: 
                    p.launch()
            if not launch and can: p.line()
            if pygame.Rect.colliderect(goal.rect, p.rect):
                playing = False
                play = False
                if level == elvle+1 != len(levels) and slevel == levels:
                    level += 1
            if keys[pygame.K_q]:
                playing = False
                play = False
            canvas.blit(goal.image, goal.rect)
            canvas.blit(p.image, p.rect)
            if mouse: 
                if can: launch = True
            else: can = True
            pygame.display.update()
            clock.tick(60)
    pygame.display.update()
    clock.tick(60)