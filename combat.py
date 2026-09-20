import pygame

attack_cooldown = 0.0

def handle_attack(player, enemies_group, grp, dt=0.0):
    global attack_cooldown
    if attack_cooldown > 0:
        attack_cooldown -= dt

    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    if mouse_clicked and attack_cooldown <= 0:
        attack_cooldown = 0.4  # Attack cooldown in seconds

        screen_mouse_x, screen_mouse_y = pygame.mouse.get_pos()
        
        camera_x = grp.view.x
        camera_y = grp.view.y
        
        world_mouse_x = screen_mouse_x + camera_x
        world_mouse_y = screen_mouse_y + camera_y
        
        dx = world_mouse_x - player.rect.centerx
        dy = world_mouse_y - player.rect.centery
        
        sword_rect = pygame.Rect(0, 0, 32, 32)
        
        if abs(dx) > abs(dy):
            if dx > 0:
                sword_rect.left = player.rect.right
                sword_rect.centery = player.rect.centery
            else:
                sword_rect.right = player.rect.left
                sword_rect.centery = player.rect.centery
        else:
            if dy > 0:
                sword_rect.top = player.rect.bottom
                sword_rect.centerx = player.rect.centerx
            else:
                sword_rect.bottom = player.rect.top
                sword_rect.centerx = player.rect.centerx

        # Check collision with enemies and damage them
        for enemy in enemies_group.copy():
            if sword_rect.colliderect(enemy.rect):
                enemy.take_damage(25)
    