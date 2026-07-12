import pygame


enemyhealth  = 50
# We only ask for the player, the enemies, and the camera group (grp)
def handle_attack(player, enemies_group, grp):
    
    # 1. Check if the Left Mouse Button (index 0) is held down
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    if mouse_clicked:
        # 2. THE CHEAT CODE: Grab the mouse directly inside this file (Screen Coordinates)
        screen_mouse_x, screen_mouse_y = pygame.mouse.get_pos()
        
        # 3. Grab the camera's current offset from pyscroll
        camera_x = grp.view.x
        camera_y = grp.view.y
        
        # 4. TRUE AIM: Calculate actual world coordinates
        world_mouse_x = screen_mouse_x + camera_x
        world_mouse_y = screen_mouse_y + camera_y
        
        # 5. DIRECTION MATH: Find the distance between mouse and player
        dx = world_mouse_x - player.rect.centerx
        dy = world_mouse_y - player.rect.centery
        
        
        sword_rect = pygame.Rect(0, 0, 32, 32)
        
        # Compare horizontal vs vertical distance to find the main aiming direction
        if abs(dx) > abs(dy):
            # Aiming Horizontally (Left or Right)
            if dx > 0:
                # Mouse is to the Right
                sword_rect.left = player.rect.right
                sword_rect.centery = player.rect.centery
            else:
                # Mouse is to the Left
                sword_rect.right = player.rect.left
                sword_rect.centery = player.rect.centery
        else:
            # Aiming Vertically (Up or Down)
            if dy > 0:
                # Mouse is Below (Down)
                sword_rect.top = player.rect.bottom
                sword_rect.centerx = player.rect.centerx
            else:
                # Mouse is Above (Up)
                sword_rect.bottom = player.rect.top
                sword_rect.centerx = player.rect.centerx
        
        
                    
                
    
    
    