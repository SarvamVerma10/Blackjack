import pyscroll
import pygame
import pytmx
from pytmx.util_pygame import load_pygame

def map_draw(path, size):
    # data-generation
    tmxd = load_pygame(path)
    mapd = pyscroll.data.TiledMapData(tmxd)
    
    # map-generation
    layer = pyscroll.BufferedRenderer(mapd, size, clamp_camera=True)
    layer.zoom = 6
    grpd = pyscroll.PyscrollGroup(map_layer=layer, default_layer=1)

    # --- EXTRACT DATA FOR GAME LOGIC ---
    walls = []
    solid_tile_layers = ["Fences", "House", "tree", "water", "wood","Random"]
    player_spawn = (250.0, 80.0) # Default fallback
    enemy_spawns = []

    for layer_obj in tmxd.visible_layers:
        # 1. Get Walls
        if isinstance(layer_obj, pytmx.TiledObjectGroup) and layer_obj.name == "Collision":
            for obj in layer_obj:
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        elif isinstance(layer_obj, pytmx.TiledTileLayer) and layer_obj.name in solid_tile_layers:
            for grid_x, grid_y, gid in layer_obj:
                if gid: 
                    walls.append(pygame.Rect(grid_x * tmxd.tilewidth, grid_y * tmxd.tileheight, tmxd.tilewidth, tmxd.tileheight))
        
        # 2. Get Spawns
        if isinstance(layer_obj, pytmx.TiledObjectGroup) and layer_obj.name == "Spawns":
            for obj in layer_obj:
                if obj.name == "PlayerSpawn":
                    player_spawn = (float(obj.x), float(obj.y))
                elif obj.name == "EnemySpawn":
                    enemy_spawns.append((float(obj.x), float(obj.y)))

    # Return the drawing group PLUS the data the game needs
    return grpd, walls, player_spawn, enemy_spawns