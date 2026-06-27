import pygame
import pytmx  

pygame.init()

# 1. Define resolutions and scale factors clearly
SCALE_FACTOR = 6
CANVAS_WIDTH, CANVAS_HEIGHT = 320, 180
SCREEN_WIDTH, SCREEN_HEIGHT = CANVAS_WIDTH * SCALE_FACTOR, CANVAS_HEIGHT * SCALE_FACTOR

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT)) 
clock = pygame.time.Clock()

tmx_data = pytmx.load_pygame('runtime/spawn.tmx')

Player_img = pygame.image.load('C1.png').convert_alpha() 
Player_img = pygame.transform.scale(Player_img, (16, 16))

# Adjusted spawn so the player starts within reasonable bounds of the 160x120 view
player_rect = Player_img.get_rect(topleft=(50, 50))
speed = 5    

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
    
    # X Movement & Collision
    dx = 0
    if keys[pygame.K_a]: dx -= speed            
    if keys[pygame.K_d]: dx += speed 
    player_rect.x += dx
    
    for wall in walls:
        if player_rect.colliderect(wall): 
            if dx > 0: player_rect.right = wall.left
            if dx < 0: player_rect.left = wall.right

    # Y Movement & Collision
    dy = 0
    if keys[pygame.K_w]: dy -= speed            
    if keys[pygame.K_s]: dy += speed 
    player_rect.y += dy

    for wall in walls:
        if player_rect.colliderect(wall): 
            if dy > 0: player_rect.bottom = wall.top
            if dy < 0: player_rect.top = wall.bottom

    # --- CAMERA LOGIC ---
    # Center the camera on the player using the unscaled canvas dimensions
    camera_x = player_rect.centerx - (CANVAS_WIDTH // 2)
    camera_y = player_rect.centery - (CANVAS_HEIGHT // 2)
    
    # Clamp camera to map boundaries so it doesn't show black edges
    camera_x = max(0, min(camera_x, map_width - CANVAS_WIDTH))
    camera_y = max(0, min(camera_y, map_height - CANVAS_HEIGHT))

    # --- RENDERING ---
    canvas.fill((0, 0, 0)) 
    
    # Draw Map relative to camera
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for grid_x, grid_y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    draw_x = (grid_x * tmx_data.tilewidth) - camera_x
                    draw_y = (grid_y * tmx_data.tileheight) - camera_y
                    canvas.blit(tile, (draw_x, draw_y))

    # Draw Player relative to camera
    canvas.blit(Player_img, (player_rect.x - camera_x, player_rect.y - camera_y)) 
    
    # Scale the low-res canvas up to fill the high-res screen
    screen.blit(pygame.transform.scale(canvas, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            
    pygame.display.flip()
    clock.tick(60) 
            
pygame.quit()