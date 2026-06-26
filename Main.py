import pygame
import pytmx  

pygame.init()

screen = pygame.display.set_mode((640, 480))
canvas = pygame.Surface((160, 120)) 
clock = pygame.time.Clock()


tmx_data = pytmx.load_pygame('runtime/spawn.tmx')

Player_img = pygame.image.load('C1.png').convert_alpha() 
Player_img = pygame.transform.scale(Player_img, (16, 16))
player_rect = Player_img.get_rect(topleft=(250, 80))
speed = 1    

# Load Collision Walls
walls = []
for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Collision":
        for obj in layer:
            walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() 
    
    
    dx = 0
    if keys[pygame.K_a]: dx -= speed            
    if keys[pygame.K_d]: dx += speed 
    player_rect.x += dx
    
    for wall in walls:
        if player_rect.colliderect(wall): 
            if dx > 0: # Moving right
                player_rect.right = wall.left
            if dx < 0: # Moving left
                player_rect.left = wall.right

    dy = 0
    if keys[pygame.K_w]: dy -= speed            
    if keys[pygame.K_s]: dy += speed 
    player_rect.y += dy

    for wall in walls:
        if player_rect.colliderect(wall): 
            if dy > 0: # Moving down
                player_rect.bottom = wall.top
            if dy < 0: # Moving up
                player_rect.top = wall.bottom

    # Camera Logic
    camera_x = player_rect.x - 80 
    camera_y = player_rect.y - 60 
    
    camera_x = max(0, min(camera_x, map_width - 160))
    camera_y = max(0, min(camera_y, map_height - 120))

    canvas.fill((0, 0, 0)) 
    
    # Draw Map
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for grid_x, grid_y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    draw_x = (grid_x * tmx_data.tilewidth) - camera_x
                    draw_y = (grid_y * tmx_data.tileheight) - camera_y
                    canvas.blit(tile, (draw_x, draw_y))

   

    # Draw Player
    canvas.blit(Player_img, (player_rect.x - camera_x, player_rect.y - camera_y)) 
    
    # Scale canvas to screen
    screen.blit(pygame.transform.scale(canvas, (640, 480)), (0, 0))
            
    pygame.display.flip()
    clock.tick(60) 
            
pygame.quit()