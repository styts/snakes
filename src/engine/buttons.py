import pygame
import operator # make offsetting work

class Button(object):
    shadow = None
    button = None
    hover = None

    def __init__(self,x,y,title):
        self.r = pygame.Rect(x, y, self.__class__.w, self.__class__.h)
        self.selected = False
        self.enabled = True
        self.title = title

    def _get_center(self,ox=0,oy=0):
        x = self.r.left + self.r.width / 2
        y = self.r.top + self.r.height / 2
        x += ox + 2 # offsets (used to render font e.g.)
        y += oy + 2
        return (x,y)

    def draw(self, surface, hover=False):
    	# optional shadow
        if not self.selected:
            surface.blit(self.shadow, self.r.move(5,5))

        # button face: shifted? highlighted?
        surface.blit(self.button if not hover else self.hover, self.r if not self.selected else self.r.move(5,5))


    @staticmethod
    def get_button_at(buttons,(x,y)):
        for b in buttons:
            if b.r.contains(pygame.Rect(x,y,1,1)) and b.enabled:
                return b
        return None

    @staticmethod
    def init(childclass):
        childclass.w = childclass.button.get_width()
        childclass.h = childclass.button.get_height()

        # create shadow surface
        childclass.shadow = pygame.Surface((childclass.w, childclass.h), pygame.SRCALPHA)
        # for each pixel in button glyph
        #print childclass.w, childclass.h
        for a in xrange(childclass.w):
            for b in xrange(childclass.h):
                # set corresponding value in shadow surface to be semi-transparent
                c = childclass.button.get_at((a,b))
                s = c if all(c) == 0 else (0,0,0,150)
                childclass.shadow.set_at((a,b),s)



class LevelButton(Button):
    """A Selectable Level Button (20+ of these on the left)"""
    def __init__(self, title, thumb, x, y, levelnr=0):
        super(LevelButton, self).__init__(x, y, title)

        self.thumb = thumb
        self.levelnr = levelnr
        
    def draw(self, surface, font=None, hover=False):
        super(LevelButton, self).draw(surface, hover)
        
        #o = (self.w/2-self.thumb.get_width()/2, self.h/2-self.thumb.get_height()/2) # o depends not on thumb, as thumb is always 80
        o = (10, 10)
        
        if self.selected:
        	o = tuple(map(operator.add, o, (5,5)))

        surface.blit(self.thumb, self.r.move(o))

    @staticmethod
    def init(resman):
        LevelButton.button = resman.get_surface("b_sq")
        LevelButton.hover = resman.get_surface("b_sq_hi")

        super(LevelButton, LevelButton).init(LevelButton)


class MenuButton(Button):    
    def __init__(self,x,y,title):
        super(MenuButton, self).__init__(x, y, title)
        self.text_color = (255,255,50)
        self.shadow_color = (135,135,0,50)

    def draw(self, surface, font, hover=False):
        super(MenuButton, self).draw(surface, hover)

        # draw font
        s_font = font.render(self.title,False,self.text_color)
        s_sh_font = font.render(self.title,False,self.shadow_color)
        o_x = -s_font.get_width()/2
        o_y = -s_font.get_height()/2
        if self.selected: o_x = o_x + 5
        if self.selected: o_y = o_y + 5
        o = 2 # font shadow offset
        surface.blit(s_sh_font, self._get_center(o_x+o,o_y+o))
        surface.blit(s_font, self._get_center(o_x,o_y))

        if not self.enabled:
            surface.blit(self.shadow, self.r.move(0,0))

    @staticmethod
    def init(resman):
        MenuButton.button = resman.get_surface("b_wide")
        MenuButton.hover = resman.get_surface("b_wide_hi")

        super(MenuButton, MenuButton).init(MenuButton)
