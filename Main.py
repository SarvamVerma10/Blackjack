import pygame
from level import map_draw
import sys

pygame.init()
width=1920
height=1080
#parameters
screen=pygame.display.set_mode((width,height), pygame.FULLSCREEN)
pygame.display.set_caption("Upper Hand")
clock=pygame.time.Clock()
#map
grp=map_draw("runtime/spawn.tmx", screen.get_size())
#loop
running=True
while running:
    #control
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
    #delta time
    dta=clock.tick(60)/1000.0
    grp.update(dta)
    #display
    screen.fill((0,0,0))
    grp.draw(screen)
    pygame.display.flip()
#exit
pygame.quit()
sys.exit()