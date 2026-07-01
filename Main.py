import pygame
import pytmx  

pygame.init()

screen = pygame.display.set_mode((640, 480))
canvas = pygame.Surface((320, 320)) 
clock = pygame.time.Clock()

tmx_data = pytmx.load_pygame('Spawn/Spawn.tmx')

# --- PLAYER SETUP ---
Player_img = pygame.image.load('C1.png').convert_alpha() 
Player_img = pygame.transform.scale(Player_img, (16, 16))

# NEW: Load the enemy image ONCE at the start of the game
Enemy_img = pygame.image.load('C1.png').convert_alpha() 
Enemy_img = pygame.transform.scale(Enemy_img, (16, 16))

player_x, player_y = 250.0, 80.0 
speed = 180 

# NEW: Player Health and I-Frames
player_health = 100
invincibility_timer = 0.0 # Prevents taking damage 60 times a second

# --- ENEMY FUNCTIONS (No more classes!) ---
def move_enemy(enemy_data, target_rect, walls, dt):
    # STEP 1: Check distance. If the player is too far away, do nothing (Sleep Mode)
    distance_to_player_x = abs(enemy_data["x"] - target_rect.x)
    distance_to_player_y = abs(enemy_data["y"] - target_rect.y)
    
    if distance_to_player_x > 400 or distance_to_player_y > 400:
        return 

    # STEP 2: Decide which way to walk based on where the player is
    move_x = 0
    move_y = 0
    
    if enemy_data["x"] < target_rect.x: 
        move_x = enemy_data["speed"] * dt  # Player is to the right -> Walk Right
    if enemy_data["x"] > target_rect.x: 
        move_x = -enemy_data["speed"] * dt # Player is to the left -> Walk Left
        
    if enemy_data["y"] < target_rect.y: 
        move_y = enemy_data["speed"] * dt  # Player is below -> Walk Down
    if enemy_data["y"] > target_rect.y: 
        move_y = -enemy_data["speed"] * dt # Player is above -> Walk Up

    # STEP 3: Move horizontally (Left/Right) and check for walls
    enemy_data["x"] = enemy_data["x"] + move_x
    enemy_data["rect"].x = round(enemy_data["x"]) # Update the physical hitbox
    
    # 'collidelistall' is a fast Pygame tool that gives us a list of walls we hit
    hit_walls_list = enemy_data["rect"].collidelistall(walls)
    for index in hit_walls_list:
        wall = walls[index]
        if move_x > 0: # If walking right, stop at the left side of the wall
            enemy_data["rect"].right = wall.left
        if move_x < 0: # If walking left, stop at the right side of the wall
            enemy_data["rect"].left = wall.right
        
        enemy_data["x"] = enemy_data["rect"].x # Save the corrected position

    # STEP 4: Move vertically (Up/Down) and check for walls
    enemy_data["y"] = enemy_data["y"] + move_y
    enemy_data["rect"].y = round(enemy_data["y"]) # Update the physical hitbox
    
    hit_walls_list = enemy_data["rect"].collidelistall(walls)
    for index in hit_walls_list:
        wall = walls[index]
        if move_y > 0: # If walking down, stop at the top of the wall
            enemy_data["rect"].bottom = wall.top
        if move_y < 0: # If walking up, stop at the bottom of the wall
            enemy_data["rect"].top = wall.bottom
            
        enemy_data["y"] = enemy_data["rect"].y # Save the corrected position

def draw_enemy(enemy_data, surface, cam_x, cam_y):
    # Only draw if they are on screen
    if -16 <= enemy_data["rect"].x - cam_x <= 320 and -16 <= enemy_data["rect"].y - cam_y <= 320:
        # NEW: Blit the pre-loaded image instead of drawing a red square
        surface.blit(Enemy_img, (enemy_data["rect"].x - cam_x, enemy_data["rect"].y - cam_y))

# --- LOAD SPAWNS ---
enemies = [] # List to hold all our active enemies

for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Spawns":
        for obj in layer:
            if obj.name == "PlayerSpawn":
                player_x = float(obj.x)
                player_y = float(obj.y)
            elif obj.name == "EnemySpawn":
                # Store enemy as a simple dictionary instead of a class
                new_enemy = {
                    "x": float(obj.x),
                    "y": float(obj.y),
                    "speed": 90,
                    "rect": pygame.Rect(int(obj.x), int(obj.y), 16, 16)
                }
                enemies.append(new_enemy)

player_rect = Player_img.get_rect(topleft=(int(player_x), int(player_y)))


walls = []
solid_tile_layers = ["Fences", "House", "tree", "water", "wood"]

for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Collision":
        for obj in layer:
            walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
    elif isinstance(layer, pytmx.TiledTileLayer) and layer.name in solid_tile_layers:
        for grid_x, grid_y, gid in layer:
            if gid: 
                walls.append(pygame.Rect(grid_x * tmx_data.tilewidth, grid_y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight))

map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight


running = True
while running:
    
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() 
    
    
    dx = 0
    if keys[pygame.K_a]: dx -= speed * dt            
    if keys[pygame.K_d]: dx += speed * dt 
    
    player_x += dx
    player_rect.x = round(player_x)
    
    for index in player_rect.collidelistall(walls):
        wall = walls[index]
        if dx > 0: player_rect.right = wall.left
        if dx < 0: player_rect.left = wall.right
        player_x = player_rect.x 

    
    dy = 0
    if keys[pygame.K_w]: dy -= speed * dt            
    if keys[pygame.K_s]: dy += speed * dt 
    
    player_y += dy
    player_rect.y = round(player_y)
    for index in player_rect.collidelistall(walls):
        wall = walls[index]
        if dy > 0: player_rect.bottom = wall.top
        if dy < 0: player_rect.top = wall.bottom
        player_y = player_rect.y 

    
    for enemy in enemies:
        move_enemy(enemy, player_rect, walls, dt)

    
    if invincibility_timer > 0:
        invincibility_timer -= dt 
    else:
        for enemy in enemies:
            if player_rect.colliderect(enemy["rect"]): 
                player_health -= 20
                invincibility_timer = 1.0 
                print(f"Ouch! Health is now {player_health}")
                
                # Optional: Add Game Over logic here later
                if player_health <= 0:
                    print("GAME OVER")
                
                break # Only take damage from one enemy at a time

    # Camera Logic
    camera_x = player_rect.x - 160 
    camera_y = player_rect.y - 160 
    camera_x = max(0, min(camera_x, map_width - 320))
    camera_y = max(0, min(camera_y, map_height - 320))

    canvas.fill((0, 0, 0)) 
    
    min_x, max_x = camera_x // tmx_data.tilewidth, (camera_x + 320) // tmx_data.tilewidth
    min_y, max_y = camera_y // tmx_data.tileheight, (camera_y + 320) // tmx_data.tileheight

    # Draw Map
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for grid_x, grid_y, gid in layer:
                if grid_x < min_x or grid_x > max_x or grid_y < min_y or grid_y > max_y:
                    continue
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    draw_x = (grid_x * tmx_data.tilewidth) - camera_x
                    draw_y = (grid_y * tmx_data.tileheight) - camera_y
                    canvas.blit(tile, (draw_x, draw_y))

    # Draw Enemies
    for enemy in enemies:
        draw_enemy(enemy, canvas, camera_x, camera_y)

    # Draw Player
    canvas.blit(Player_img, (player_rect.x - camera_x, player_rect.y - camera_y)) 
    
    # Scale canvas to screen
    screen.blit(pygame.transform.scale(canvas, (640, 640)), (0, 0))
            
    # NEW: Draw a simple Health Bar on top of everything
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 20)) # Red background
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, max(0, player_health), 20)) # Green health bar
            
    pygame.display.flip()
            
pygame.quit()