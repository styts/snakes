import pygame

class LifeMeter(object):
	"""The bar on the side
	Green: Safety.
    Orange: Bonus.
    Red: Life.
	"""
	border_offset = 5; # pixels
	w_bar = 10 # pixels
	def __init__(self, min_moves, bonus_moves, max_life):
		self._surface = pygame.Surface((self.w_bar+2*self.border_offset,300))
		self.min_moves = min_moves
		self.bonus_moves = bonus_moves
		self.max_life = max_life

	def _draw_column(self, value=None, color=None, max_value=None, offset=None):
		left_offset = offset

		h_s = self._surface.get_height()
		max_column_pix = h_s - 2*self.border_offset
		
		h = max_column_pix * value / max_value
		x = self.border_offset + left_offset
		y = self.border_offset + max_column_pix - h
		
		if h > 0:
			pygame.draw.rect(self._surface, color, pygame.Rect( x, y, self.w_bar, h ))

	def draw(self, target_surface, (life, bonus, safety)):
		self._surface.fill((0,0,0))

		self._draw_column(color=(0,150,0),    offset=0 , value=safety, max_value=self.min_moves  ) # Green = Safety
		self._draw_column(color=(255,102,51), offset=15, value=bonus , max_value=self.bonus_moves) # Yellow = Bonus
		self._draw_column(color=(150,0,0),    offset=30, value=life  , max_value=self.max_life   ) # Red = Life

		x_offset = target_surface.get_width() - 350
		y_offset = target_surface.get_height() / 2 - self._surface.get_height() / 2
		target_surface.blit(self._surface, pygame.Rect(x_offset,y_offset,0,0))
		pass