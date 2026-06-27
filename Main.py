import pygame
import pytmx  

pygame.init()

screen = pygame.display.set_mode((640, 480))
canvas = pygame.Surface((320, 320)) 
clock = pygame.time.Clock()

tmx_data = pytmx.load_pygame('Spawn/Spawn.tmx')

Player_img = pygame.image.load('C1.png').convert_alpha() 
Player_img = pygame.transform.scale(Player_img, (16, 16))
player_rect = Player_img.get_rect(topleft=(250, 80))

# NEW: Delta time requires float values for smooth movement, as rects only hold integers.
player_x, player_y = 250.0, 80.0 
# NEW: Speed is now in pixels per second, rather than pixels per frame.
speed = 180 

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
    
    # NEW: Calculate delta time (dt) in seconds.
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() 
    
    dx = 0
    # NEW: Multiply speed by dt
    if keys[pygame.K_a]: dx -= speed * dt            
    if keys[pygame.K_d]: dx += speed * dt 
    
    # NEW: Update the float position first, then assign it to the integer rect
    player_x += dx
    player_rect.x = round(player_x)
    
    for wall in walls:
        if player_rect.colliderect(wall): 
            if dx > 0: # Moving right
                player_rect.right = wall.left
                player_x = player_rect.x # NEW: Sync float back to rect
            if dx < 0: # Moving left
                player_rect.left = wall.right
                player_x = player_rect.x # NEW: Sync float back to rect

    dy = 0
    # NEW: Multiply speed by dt
    if keys[pygame.K_w]: dy -= speed * dt            
    if keys[pygame.K_s]: dy += speed * dt 
    
    # NEW: Update the float position first, then assign it to the integer rect
    player_y += dy
    player_rect.y = round(player_y)

    for wall in walls:
        if player_rect.colliderect(wall): 
            if dy > 0: # Moving down
                player_rect.bottom = wall.top
                player_y = player_rect.y # NEW: Sync float back to rect
            if dy < 0: # Moving up
                player_rect.top = wall.bottom
                player_y = player_rect.y # NEW: Sync float back to rect

    # Camera Logic
    camera_x = player_rect.x - 160 
    camera_y = player_rect.y - 160 
    
    camera_x = max(0, min(camera_x, map_width - 320))
    camera_y = max(0, min(camera_y, map_height - 320))

    canvas.fill((0, 0, 0)) 
    
    # NEW: Calculate which tiles are actually on the screen to prevent drawing 10,000 tiles a frame.
    min_x = camera_x // tmx_data.tilewidth
    max_x = (camera_x + 320) // tmx_data.tilewidth
    min_y = camera_y // tmx_data.tileheight
    max_y = (camera_y + 320) // tmx_data.tileheight

    # Draw Map
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for grid_x, grid_y, gid in layer:
                # NEW: Skip blitting if the tile is outside the camera's view (Fixes the lag)
                if grid_x < min_x or grid_x > max_x or grid_y < min_y or grid_y > max_y:
                    continue
                
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    draw_x = (grid_x * tmx_data.tilewidth) - camera_x
                    draw_y = (grid_y * tmx_data.tileheight) - camera_y
                    canvas.blit(tile, (draw_x, draw_y))

    # Draw Player
    canvas.blit(Player_img, (player_rect.x - camera_x, player_rect.y - camera_y)) 
    
    # Scale canvas to screen
    screen.blit(pygame.transform.scale(canvas, (640, 640)), (0, 0))
            
    pygame.display.flip()
            
pygame.quit()