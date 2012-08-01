import pygame

class LifeMeter(object):
	"""The bar on the side

    Red: Life. 
    Orange: Bonus.
	"""
	border_offset = 5; # pixels
	w_bar = 10 # pixels
	def __init__(self, min_moves, bonus_moves, max_life):
		
		self.surface = pygame.Surface((50,300))
		self.min_moves = min_moves
		self.bonus_moves = bonus_moves
		self.total_moves = min_moves + bonus_moves
		self.max_life = max_life
		self.pix_per_move = (self.surface.get_height() - 2*self.border_offset) / self.total_moves
		#print self.pix_per_move

	def _get_height(a, b):
		""" a out of b"""
		pass

	#def _draw_rect(self)

	def _draw_column(self, value=None, color=None, max_value=None, offset=None):
		left_offset = offset

		h_s = self.surface.get_height()
		max_column_pix = h_s - 2*self.border_offset
		
		h = max_column_pix * value / max_value
		x = self.border_offset + left_offset
		y = self.border_offset + max_column_pix - h
		
		if h > 0:
			pygame.draw.rect(self.surface, color, pygame.Rect( x, y, self.w_bar, h ))


	# def _draw_bonus(self,used_moves):
	# 	c_bonus = 
	# 	left_offset = 15

	# 	w = 10
	# 	penalty = used_moves*self.pix_per_move #fixme

	# 	h_s = self.surface.get_height()
	# 	h_l = h_s-self.border_offset*2-penalty

	# 	pygame.draw.rect(self.surface,c_bonus, # Orange safety rect
	# 	 	pygame.Rect( self.border_offset + left_offset, self.border_offset+penalty, 
	# 	 		10, h_l ))


	def _draw_life(self,used_moves):
		c_life = (200,0,0)
		left_offset = 30
		w = 10
		penalty = used_moves*self.pix_per_move #fixme

		h_s = self.surface.get_height()
		h_l = h_s-self.border_offset*2-penalty

		pygame.draw.rect(self.surface,c_life, # Red life rect
		 	pygame.Rect( self.border_offset + left_offset, self.border_offset+penalty, 
		 		10, h_l ))

		pass


	def draw(self, target_surface, (life, bonus, safety)):
		self.surface.fill((0,0,0))

		#return

		#self._draw_life(life) # R
		#self._draw_bonus(bonus) # Y
		print "bonus", bonus
		self._draw_column(color=(0,150,0),    offset=0 , value=safety, max_value=self.min_moves  ) # Green = Safety
		self._draw_column(color=(255,102,51), offset=15, value=bonus , max_value=self.bonus_moves) # Yellow = Bonus
		self._draw_column(color=(150,0,0),    offset=30, value=life  , max_value=self.max_life   ) # Red = Life

		
		# w_s = self.surface.get_width()
		# h_s = self.surface.get_height()

		# penalty = used_moves*self.pix_per_move
		# h_l = h_s-self.border_offset*2-penalty
		
		# pygame.draw.rect(self.surface,c_life, # Red life rect
		# 	pygame.Rect( self.border_offset, self.border_offset+penalty, 
		# 		w_s-self.border_offset*2, h_l ))

		x_offset = target_surface.get_width() - 350
		y_offset = target_surface.get_height() / 2 - self.surface.get_height() / 2
		target_surface.blit(self.surface, pygame.Rect(x_offset,y_offset,0,0))
		pass

	def process(self):
		pass
		