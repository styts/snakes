from pygame.font import SysFont #@UnresolvedImport
from logic.tile import BLOCK_SIZE

DBG_STRINGS = {'d1' : "DEBUG INFO:",
               'd2' : "===========",}
class DebugInfo:
    
    def del_var(self,key):
        if key in self.strings:
            del self.strings[key]
    
    def attach_var(self,key,val):
        #s = str(var)
        #### BUG: This may cause a bug when same value is not shown twice
        #print self.strings
        #if self.on and key not in self.strings:
        self.strings[key] = val
        
    def __init__(self,app):
        self.font = SysFont("Courier",12)
        self.app = app
        self.color     = 200,200,200
        self.color_map = 100,100,100
        self.on = True
        self.strings = DBG_STRINGS
        self.x_offset = 0 # will be set with map init
        self.y_offset = 30

    def draw(self):
        if self.on:
            # scrolling over the map prints debug info for the current block
            cb = self.app.input.current_block
            if cb:
                di = cb.get_debug_infos()
                for i in range(len(di)):
                    d = di[i]
                    ren = self.font.render(d,1,self.color_map)
                    try:
                        self.app.screen.blit(ren, (cb.map.x_offset + cb.x*BLOCK_SIZE,
                                                   cb.map.y_offset + cb.y*BLOCK_SIZE+i*(self.font.get_height()-5)))
                    except ReferenceError:
                        pass
                    
            # the debug strings themselves
            i = 0
            
            items = self.strings.items()
            items.sort()
            for k,v in items: #@UnusedVariable #IGNORE:W0612
                ren = self.font.render(v,1,self.color)
                self.app.screen.blit(ren, (self.x_offset,self.y_offset+i*(self.font.get_height()-5)))
                i = i + 1

        self.strings = DBG_STRINGS
