import pygame
from pytmx.util_pygame import load_pygame
import pyscroll
import sys

pygame.init()
width=1920
height=1080
#parameters
screen=pygame.display.set_mode((width,height), pygame.FULLSCREEN)
pygame.display.set_caption("Upper Hand")
clock=pygame.time.Clock()
#map
data=load_pygame("runtime/spawn.tmx")
scroll=pyscroll.data.TiledMapData(data)
layer=pyscroll.BufferedRenderer(scroll, screen.get_size(), clamp_camera=True)
layer.zoom=6
grp=pyscroll.PyscrollGroup(map_layer=layer, default_layer=1)
#loop
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
    dta=clock.tick(60)/1000.0
    grp.update(dta)
    screen.fill((0,0,0))
    grp.draw(screen)
    pygame.display.flip()
#exit
pygame.quit()
sys.exit()