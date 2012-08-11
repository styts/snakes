
import os, glob, pygame

class ResourceManager():
    LOCATION_SPRITES = os.path.join("data", "sprites")
    LOCATION_SOUNDS = os.path.join("data", "sounds")

    def __init__(self, app):
        self.app = app
        self._surfaces = {}
        self._sounds = {}
        self._load_all()

    def _load_all(self):
        ## load sprites
        ext = ".png"
        for fn in glob.glob(ResourceManager.LOCATION_SPRITES+"/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            surf = pygame.image.load(fn)
            surf = surf.convert_alpha()
            self._surfaces[bn] = {}
            self._surfaces[bn]["default"] = surf

        ## load sfx
        ext = ".wav"
        for fn in glob.glob(ResourceManager.LOCATION_SOUNDS+"/*%s" % ext):
            bn = os.path.basename(fn).replace(ext, "")
            sound = pygame.mixer.Sound(fn)
            self._sounds[bn] = sound

    def fill_me(self, surf, color, alpha):
        s = surf.copy()
        col = color + (alpha,)
        s.fill(col, None, pygame.BLEND_RGBA_MULT)
        return s

    def get_surface(self, name, color=None, alpha=255):
        color_str = str(color)
        if name not in self._surfaces.keys():
            return None

        if color:
            if color_str not in self._surfaces[name].keys():
                self._surfaces[name][color_str] = self.fill_me(self._surfaces[name]['default'], color, alpha)
            return self._surfaces[name][color_str]
        else:
            return self._surfaces[name]["default"]

    def get_sound(self, name):
        return self._sounds[name]