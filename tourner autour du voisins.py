import pygame as pg
from math import sqrt
import math
from random import randrange,seed
from colorsys import hsv_to_rgb
# Constantes :
FPS = 60  # les fps tabernak
WIND = 750 # dimentions de la fentere
seed() #planter la graine d'aletaioire
""" Rappels:
.---------------- + x
|
|
|
|
|
|
|
+ y
"""

pg.init()
f = pg.display.set_mode(size=(WIND, WIND))
pg.display.set_caption("Gravitation autour du plus fat")
fpsClock = pg.time.Clock()
font = pg.font.SysFont('consolas', 30) #police//roxane
depx,depy=0,0#la caméra
mouv=10#sa vtesse de mouvement
zoom=1
vitesse_grossiment=1#vitesse d'expantion des nouvelles planètes
b = True
lutins=[]
defa= False
rayon=0
centr=()
WantKiss=False

class distance:
    def __init__(self,a,b):
        self.a=a
        self.z=b
    def deltax(self):
        return self.a.x-self.z.x
    def deltay(self):
        return self.a.y-self.z.y
    def dist(self):  # Distance entre a et b
        return math.sqrt(((self.a.x - self.z.x) ** 2 )+ (self.a.y - self.z.y) ** 2)



class lutin:  # Les météorites
    def __init__(self):
        self.rad=0
        self.x,self.y=0,0
        self.pos=len(lutins)

        if lutins:
            self.prec=lutins[-1]
            d=distance(self,self.prec)
            self.angl=math.acos((self.x-self.prec.x)/d.dist())
            if self.prec.y > self.y :
                self.angl = -(self.angl+2*math.pi)
        else:
            self.prec=self
            self.angl=0

    def find_angl(self):
        if lutins:
            dista=math.sqrt((self.x-self.prec.x)**2+(self.y-self.prec.y)**2)
            if dista!=0:
                d=distance(self,self.prec)
                self.angl=math.acos(d.deltax()/dista)
                if self.prec.y > self.y :
                    self.angl = -(self.angl+2*math.pi)
        else:
            self.angl=0
    def fd(self):  # Suivre son instinct
        global centr
        if self==lutins[0]:
            self.c=(255,255,255)
            centr=(self.x,self.y)

        else:
            self.c=hsv_to_rgb(self.pos/len(lutins), 1.0, 255)

            self.find_angl()
            dista=math.sqrt((self.x-self.prec.x)**2+(self.y-self.prec.y)**2)

            self.angl+=math.pi/(dista+1)

            self.x=math.cos(self.angl)*dista+self.prec.x
            self.y=math.sin(self.angl)*dista+self.prec.y




try:
    while b:
        # Actualiser:
        pg.display.flip()

        # Appliquer les images de fond sur la fenetre
        s = pg.Surface((WIND, WIND))  # piqué sur stackoverflow pour avoir un fond avec un alpha

        text = font.render(str(len(lutins)), True, (0,0,0))
        textRect = text.get_rect()

        p = pg.key.get_pressed()  # SI la touche est appuyée
        antdep=(depx,depy)
        if p[pg.K_d]:depx-=mouv
        if p[pg.K_q]:depx+=mouv
        if p[pg.K_z]:depy+=mouv
        if p[pg.K_s]:depy-=mouv

        if lutins:
            ecart=(WIND/2 - lutins[0].x)+(WIND/2 - lutins[0].y)
            cam=depx+depy
            if int(ecart)==0 and int(cam)==0 :
                WantKiss=False
            else:
                if WantKiss:
                    lutins[0].x+=(WIND/2 - lutins[0].x)/50
                    lutins[0].y+=(WIND/2 - lutins[0].y)/50
                    depx-= depx/50
                    depy-= depy/50
        """ if antdep==(depx,depy):
            s.set_alpha(10)
        else:
            s.set_alpha(500)""" # Pour avoir un tracé
        s.set_alpha()
        s.fill((0, 0, 0))
        f.blit(s, (0, 0))
        pointer=pg.mouse
        if pointer.get_pressed()[0]:
            if defa:
                rayon=10
                defa=False
            else:
                rayon+=vitesse_grossiment/zoom
                pg.draw.circle(f,(randrange(100),randrange(100),randrange(100)),pointer.get_pos(),rayon*zoom)

        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False
                print(" Fin du jeu  babe")
            elif event.type == pg.KEYUP:
                if event.dict['key']==pg.K_SPACE:
                    WantKiss=True
                if event.dict['key']==pg.K_a:
                    for i in range(50):
                        m=lutin()
                        m.x=randrange(WIND)
                        m.y=randrange(WIND)
                        m.find_angl()
                        m.rad=randrange(50)
                        for ind,lut in enumerate(lutins):
                            if lut.rad<rayon:
                                lutins.insert(ind,m)
                                break
                        if not m in lutins:
                            lutins.append(m)
            elif event.type==pg.MOUSEBUTTONUP:
                if event.button==1: #click gauche
                    defa=True
                    m=lutin()
                    m.x,m.y=(event.pos[0]-depx)/zoom,(event.pos[1]-depy)/zoom
                    m.find_angl()
                    m.rad=rayon
                    for ind,lut in enumerate(lutins):
                        if lut.rad<rayon:
                            lutins.insert(ind,m)
                            break
                    if not m in lutins:
                        lutins.append(m)


                    #on trie selon la taille

                if event.button==3:
                    if lutins:
                        lutins.pop(0)
                elif event.button==4: #vers le haut
                    zoom+=0.01
                elif event.button==5: #vers le bas
                    zoom-=0.01

        for bubu in lutins:
            bubu.fd()
            pg.draw.circle(f,bubu.c,(depx+bubu.x*zoom, depy+bubu.y*zoom),bubu.rad*zoom)
        if len(centr)==2:
            f.blit(text, (depx+centr[0]*zoom-textRect[2]/2,depy+centr[1]*zoom-textRect[3]/2))

        else:
            f.blit(text, (0,0))


        fpsClock.tick(FPS)
except :
    pg.quit()
    raise
pg.quit()
