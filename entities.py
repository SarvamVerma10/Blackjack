import pygame
import pyscroll

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, walls):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.position = [x, y] # Use list for float precision
        self.walls = walls
        self.speed = 180
        self.health = 100
        self.invincibility_timer = 0.0

    def update(self, dt, keys, enemies):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt

        # X Movement & Collision
        dx = 0
        if keys[pygame.K_a]: dx -= self.speed * dt
        if keys[pygame.K_d]: dx += self.speed * dt
        
        self.position[0] += dx
        self.rect.x = round(self.position[0])
        for index in self.rect.collidelistall(self.walls):
            wall = self.walls[index]
            if dx > 0: self.rect.right = wall.left
            if dx < 0: self.rect.left = wall.right
            self.position[0] = self.rect.x

        # Y Movement & Collision
        dy = 0
        if keys[pygame.K_w]: dy -= self.speed * dt
        if keys[pygame.K_s]: dy += self.speed * dt
        
        self.position[1] += dy
        self.rect.y = round(self.position[1])
        for index in self.rect.collidelistall(self.walls):
            wall = self.walls[index]
            if dy > 0: self.rect.bottom = wall.top
            if dy < 0: self.rect.top = wall.bottom
            self.position[1] = self.rect.y

        # Damage Logic
        if self.invincibility_timer <= 0:
            # Check collision with the enemy sprite group
            if pygame.sprite.spritecollideany(self, enemies):
                self.health -= 20
                self.invincibility_timer = 1.0
                print(f"Ouch! Health is now {self.health}")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, walls, player):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.position = [float(x), float(y)]
        self.speed = 90
        self.walls = walls
        self.player = player

    def update(self, dt):
        distance_to_player_x = abs(self.position[0] - self.player.rect.x)
        distance_to_player_y = abs(self.position[1] - self.player.rect.y)
        
        if distance_to_player_x > 400 or distance_to_player_y > 400:
            return 

        move_x = 0
        move_y = 0
        
        if self.position[0] < self.player.rect.x: move_x = self.speed * dt
        if self.position[0] > self.player.rect.x: move_x = -self.speed * dt
        if self.position[1] < self.player.rect.y: move_y = self.speed * dt
        if self.position[1] > self.player.rect.y: move_y = -self.speed * dt

        # X Movement
        self.position[0] += move_x
        self.rect.x = round(self.position[0])
        for index in self.rect.collidelistall(self.walls):
            wall = self.walls[index]
            if move_x > 0: self.rect.right = wall.left
            if move_x < 0: self.rect.left = wall.right
            self.position[0] = self.rect.x

        # Y Movement
        self.position[1] += move_y
        self.rect.y = round(self.position[1])
        for index in self.rect.collidelistall(self.walls):
            wall = self.walls[index]
            if move_y > 0: self.rect.bottom = wall.top
            if move_y < 0: self.rect.top = wall.bottom
            self.position[1] = self.rect.y