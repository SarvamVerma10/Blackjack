import pygame
import sys
from Level import map_draw
from entities import Player, Enemy
from combat import handle_attack

pygame.init()
width = 1920
height = 1080

# parameters
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Upper Hand")
clock = pygame.time.Clock()

# map and data loading
# Notice we are now catching the walls and spawns returned by map_draw
grp, walls, player_spawn, enemy_spawns = map_draw("Spawn/Spawn.tmx", screen.get_size())

# Setup Images
player_img = pygame.image.load('C1.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (16, 16))
enemy_img = pygame.image.load('C1.png').convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (16, 16))

# Setup Entities
player = Player(player_spawn[0], player_spawn[1], player_img, walls)
grp.add(player) # Add to pyscroll to be drawn

enemies_group = pygame.sprite.Group() # Group for collision checking
for spawn in enemy_spawns:
    enemy = Enemy(spawn[0], spawn[1], enemy_img, walls, player)
    enemies_group.add(enemy)
    grp.add(enemy) # Add to pyscroll to be drawn

# loop
running = True
while running:
    # delta time
    dt = clock.tick(60) / 1000.0

    keys = pygame.key.get_pressed()

    
    player.update(dt, keys, enemies_group)
    enemies_group.update(dt)

    
    handle_attack(player, enemies_group, grp)

    # Tell pyscroll to center the camera on the player
    grp.center(player.rect.center)
    # display
    screen.fill((0, 0, 0))
    
    mx, my = pygame.mouse.get_pos()
    target_x = (player.rect.centerx + (mx + grp.view.x)) / 2
    target_y = (player.rect.centery + (my + grp.view.y)) / 2

# Tell pyscroll to follow that halfway point
    grp.center((target_x, target_y))

    grp.draw(screen)
    
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    # Update logic manually (keeps it clean)
    player.update(dt, keys, enemies_group)
    enemies_group.update(dt)

    # Tell pyscroll to center the camera on the player
    grp.center(player.rect.center)

    # display
    screen.fill((0, 0, 0))
    grp.draw(screen) # Pyscroll draws the map, player, and enemies automatically!
    
    # Draw Health Bar over the game
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 20))
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, max(0, player.health), 20))

    pygame.display.flip()

# exit
pygame.quit()
sys.exit()