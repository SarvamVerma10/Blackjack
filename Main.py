import pygame
import pytmx  

pygame.init()

screen = pygame.display.set_mode((640, 640))
canvas = pygame.Surface((320, 320)) 
clock = pygame.time.Clock()

tmx_data = pytmx.load_pygame('sampleMap.tmx') 


Player_img = pygame.image.load('C1.png').convert_alpha() 
Player_img = pygame.transform.scale(Player_img, (16, 16))
player_rect = Player_img.get_rect(topleft=(100, 100))
speed = 3    


walls = []
for layer in tmx_data.visible_layers:
    # We specifically look for the layer you named "Collision" in your screenshot!
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Collision":
        for obj in layer:
            walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))



map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

running = True
while running:
    
    
    keys = pygame.key.get_pressed() 
    
    
    dx = 0
    if keys[pygame.K_a]: dx -= speed            
    if keys[pygame.K_d]: dx += speed 
    player_rect.x += dx
    
    # B. Check X Collisions
    for wall in walls:
        if player_rect.colliderect(wall): 
            if dx > 0: 
                player_rect.right = wall.left
            if dx < 0: 
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

    
    camera_x = player_rect.x - 160 
    camera_y = player_rect.y - 160 
    
    camera_x = max(0, min(camera_x, map_width - 320))
    camera_y = max(0, min(camera_y, map_height - 320))

    canvas.fill((0, 0, 0)) 
    
    
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for grid_x, grid_y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    draw_x = (grid_x * tmx_data.tilewidth) - camera_x
                    draw_y = (grid_y * tmx_data.tileheight) - camera_y
                    canvas.blit(tile, (draw_x, draw_y))

    
    for wall in walls:
        
        pygame.draw.rect(canvas, (255, 0, 0), (wall.x - camera_x, wall.y - camera_y, wall.width, wall.height), 1)

    
    pygame.draw.rect(canvas, (0, 255, 0), (player_rect.x - camera_x, player_rect.y - camera_y, player_rect.width, player_rect.height), 1)

    canvas.blit(Player_img, (player_rect.x - camera_x, player_rect.y - camera_y)) 
    
   
    screen.blit(pygame.transform.scale(canvas, (640, 640)), (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()
    clock.tick(60) 
            
pygame.quit()