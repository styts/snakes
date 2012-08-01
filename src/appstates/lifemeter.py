import pygame

class LifeMeter(object):
	"""The bar on the side

    Red: Life. 
    Orange: Bonus.
	"""
	border_offset = 5; # pixels
	def __init__(self, min_moves, extra_moves):
		self.surface = pygame.Surface((50,300))
		self.min_moves = min_moves
		self.extra_moves = extra_moves
		self.total_moves = min_moves + extra_moves
		self.pix_per_move = (self.surface.get_height() - 2*self.border_offset) / self.total_moves
		#print self.pix_per_move

	def draw(self, target_surface, used_moves):
		self.surface.fill((0,0,0))
		c_life = (200,0,0)
		c_bonus = (255,102,51)

		w_s = self.surface.get_width()
		h_s = self.surface.get_height()
		penalty = used_moves*self.pix_per_move
		h_l = h_s-self.border_offset*2-penalty
		
		pygame.draw.rect(self.surface,c_life, # Red life rect
			pygame.Rect( self.border_offset, self.border_offset+penalty, 
				w_s-self.border_offset*2, h_l ))

		x_offset = target_surface.get_width() - 350
		y_offset = target_surface.get_height() / 2 - self.surface.get_height() / 2
		target_surface.blit(self.surface, pygame.Rect(x_offset,y_offset,0,0))
		pass

	def process(self):
		pass
		