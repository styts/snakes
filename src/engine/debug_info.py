from pygame.font import SysFont
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
        
    def __init__(self,ingameState):
        self.font = SysFont("Courier",16)
        self.ingameState = ingameState
        self.app = self.ingameState.app
        self.color     = 200,200,200
        self.color_map = 0,255,255#255,200,200
        self.on = True
        self.strings = DBG_STRINGS
        self.x_offset = 0 # will be set with map init
        self.y_offset = 30

    def draw(self):
        if self.on:
            # scrolling over the map prints debug info for the current block
            cb = self.ingameState.current_block
            if cb:
                di = cb.get_debug_infos()
                for i in range(len(di)):
                    d = di[i]
                    ren = self.font.render(d,0,self.color_map)
                    try:
                        r = (cb.map.x_offset + cb.x*BLOCK_SIZE,
                            cb.map.y_offset + cb.y*BLOCK_SIZE+i*(self.font.get_height()-5))
                        self.app.screen.blit(ren, r)
                    except ReferenceError:
                        pass
                    
            # the debug strings themselves
            i = 0
            
            items = self.strings.items()
            items.sort()
            for k,v in items: #@UnusedVariable #IGNORE:W0612
                ren = self.font.render(v, False,self.color,(0, 0, 0))
                r = (self.x_offset,self.y_offset+i*(self.font.get_height()-5))
                self.app.screen.blit(ren, r)

                i = i + 1
            #self.app.dirty(Rect())

        self.strings = DBG_STRINGS
