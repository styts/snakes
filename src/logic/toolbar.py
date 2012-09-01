from src.logic.misc import letter_to_color
from src.logic.state import State
import os
#import glob
#import weakref
import pygame
from src.utils.sort import sort_nicely

WIDTH_OF_BUTTON = 39

class ToolbarButton:
    def __init__(self,toolbar,value,action=None,label='',surface=None):
        self.value = value
        self.label = label
        self.action = action
        # self.toolbar = weakref.proxy(toolbar)
        self.toolbar = toolbar
        self.surface = None if not surface else surface
        self.color = None
        if not surface:
            if action in ['mapsize']: self.color = (10,40,50)
            else: self.color = letter_to_color(value)

    def click(self):
        if self.action == 'mapsize':
            self.toolbar.ingameState.clean_map(self.value)
        if self.action == 'mapload':
            self.toolbar.ingameState.reset_state(level_name=self.value)

class Toolbar:
    def __init__(self,ingameState,surface,x_offset,y_offset):
        self.dest_surface = surface
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.surface = pygame.Surface((233,350),pygame.SRCALPHA) # w x h
        self.ingameState = ingameState

        self.buttons = []
        self.reload_buttons()

        self.current_button = None
        self.hover_button = None

        self.font = ingameState.app.font #pygame.font.SysFont("Courier New",18)

    def reload_buttons(self):
        self.buttons = []
        self.buttons.append([])
        for v in ['G','B','Y','R','O','P']:
            b = ToolbarButton(self,v,action='setsnake')
            self.buttons[0].append(b)
        self.buttons.append([])
        for v in ['g','b', 'y', 'r', '0','1']:
            b = ToolbarButton(self,v,action='settile')
            self.buttons[1].append(b)

        ## NEW MAP button
        self.buttons.append([])
        v = 12; b = ToolbarButton(self,v,action='mapsize',label=str(v))
        self.buttons[2].append(b)
        """
        # we don't need so many NEW MAP buttons #
        for v in xrange(3,11):
            b = ToolbarButton(self,v,action='mapsize',label=str(v))
            self.buttons[2].append(b)
        self.buttons.append([])
        for v in xrange(11,19): # second row of map buttons
            b = ToolbarButton(self,v,action='mapsize',label=str(v))
            self.buttons[3].append(b)
        """

        # add buttons for loading map with screenshots
        self.buttons.append([])
        # maps = glob.glob(os.path.join(os.getcwd(),'data','maps')+"/*.png")
        # maps += glob.glob(os.path.join(os.getcwd(),'data','maps')+"/*.json")
        # sort_nicely(maps) # sort (natural order) by first integer - state graph size
        maps = self.ingameState.app.resman.get_levels()
        row = 3 
        for fn in maps:
            fn = os.path.basename(fn)
            state = State(None,None)
            if fn.endswith("png"):
                state.load_from_file(fn)
            else:
                state.load_from_json_file(os.path.join(os.getcwd(),'data','maps',fn))
            thumb = state.get_thumbnail(a=60,resman=self.ingameState.app.resman)
            #t_w, t_h = thumb.get_size()
            #thumb = pygame.transform.scale(thumb,(t_w/2,t_h/2))
            b = ToolbarButton(self,fn,action='mapload',surface=thumb)
            if len(self.buttons[row]) > self.surface.get_width() / WIDTH_OF_BUTTON:
                self.buttons.append([])
                row = row + 1
            self.buttons[row].append(b)
        self.current_button = None
        self.hover_button = None

    def _get_button_at(self,(x,y)):
        x = x - self.x_offset
        y = y - self.y_offset
        i = int(x / WIDTH_OF_BUTTON)
        j = int(y / WIDTH_OF_BUTTON)
        if j < len(self.buttons):
            if i < len(self.buttons[j]):
                return (self.buttons[j][i])
            else:
                return None
        else:
            return None

    def _get_button_pos(self,butt):
        for j in xrange(len(self.buttons)):
            for i in xrange(len(self.buttons[j])):
                b = self.buttons[j][i]
                if b == butt:
                    return (i,j)
        return None


    def process(self,event):
        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN] or event.pos[0] < self.x_offset or event.pos[1] < self.y_offset:
            return None

        if event.type == pygame.MOUSEMOTION:
            b = self._get_button_at(event.pos)
            if b != None:
                self.hover_button = b
            else:
                self.hover_button = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            b = self._get_button_at(event.pos)
            if b:   
                if b.action in ['mapsize','mapload']:    
                    b.click()
                else:
                    self.current_button = b
            else:
                self.current_button = None

        # add debug info
        if self.hover_button:
            self.ingameState.debug_info.attach_var("toolbar_action","%s %s" % (self.hover_button.action, self.hover_button.value))
        else:
            self.ingameState.debug_info.del_var("toolbar_action")

    def draw(self):
        # clear
        self.surface.fill((10,10,10,150))

        # draw buttons
        for j in xrange(len(self.buttons)):
            for i in xrange(len(self.buttons[j])):
                b = self.buttons[j][i]
                l = i*WIDTH_OF_BUTTON
                t = j*WIDTH_OF_BUTTON
                w = WIDTH_OF_BUTTON
                h = WIDTH_OF_BUTTON
                if b.color:
                    pygame.draw.rect(self.surface,b.color,(l,t,w,h))
                ren = self.font.render(b.label,1,(255,255,255))
                self.surface.blit(ren,(l,t))
                if b.surface:
                    self.surface.blit(b.surface,(l,t))


        # draw hover button
        if self.hover_button:
            #i = self.buttons.index(self.hover_button)
            #i = 2
            i,j = self._get_button_pos(self.hover_button)
            pygame.draw.rect(self.surface,(255,255,155),(i*WIDTH_OF_BUTTON,j*WIDTH_OF_BUTTON,WIDTH_OF_BUTTON,WIDTH_OF_BUTTON),1)

        if self.current_button:
            #i = self.buttons.index(self.current_button)
            #i = 2
            i,j = self._get_button_pos(self.current_button)
            pygame.draw.rect(self.surface,(255,155,155),(i*WIDTH_OF_BUTTON,j*WIDTH_OF_BUTTON,WIDTH_OF_BUTTON,WIDTH_OF_BUTTON),1)

        self.dest_surface.blit(self.surface,(self.x_offset,self.y_offset))
