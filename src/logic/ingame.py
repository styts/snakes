
class AppState:
    pass

class InGame(AppState):
    def __init__(self,app):
        self.state = None
        self.debug_info = DebugInfo(self)
        self.toolbar = Toolbar(self, self.screen, self.screen_w-300, 200) # 300 px off the right edge
        
        self.n_moves = 0 
        self.time_began = time()
        self.level_name = ""
        
        reset_state(self,"tempstate.json")
        
        # TODO: toggle edit mode from command line
        self.edit_mode = True
        self.state_complete = False

        #ingame
        self.inputProcessor = InGameInputProcessor()

    def process_input_event(self,event):
        self.inputProcessor.process(event)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.state.map.draw()
        for s in self.state.snakes:
            s.draw()
        self.debug_info.draw()
                
        # number of moves
        moves_str = "Moves: %s" % self.n_moves
        ren_n_moves = self.font.render(moves_str,1,(255,255,0))
        ren_n_moves_shadow = self.font.render(moves_str,1,(155,155,0))
        self.screen.blit(ren_n_moves_shadow, (12,12))
        self.screen.blit(ren_n_moves, (10,10))
        
        #time
        delta = time()-self.time_began
        min = int(delta / 60)#IGNORE:W0622
        sec = int(delta % 60)
        str_time = "%02d:%02d" % (min,sec)
        ren_time = self.font.render(str_time,1,(255,255,0))
        ren_time_shadow = self.font.render(str_time,1,(155,155,0))
        # don't show time
        ###self.screen.blit(ren_time_shadow, (482,12))
        ###self.screen.blit(ren_time, (480,10))
        
        #completion
        if self.state_complete:
            ren_complete = self.font.render("COMPLETE",1,(155,255,0))
            self.screen.blit(ren_complete, (250,10))
        
        if self.edit_mode:
            self.toolbar.draw()
    