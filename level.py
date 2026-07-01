import pyscroll
from pytmx.util_pygame import load_pygame

def map_draw(path, size):
    #data-generation
    tmxd=load_pygame(path)
    mapd=pyscroll.data.TiledMapData(tmxd)
    #map-generation
    layer=pyscroll.BufferedRenderer(mapd, size, clamp_camera=True)
    layer.zoom=6
    grpd=pyscroll.PyscrollGroup(map_layer=layer, default_layer=1)
    return grpd