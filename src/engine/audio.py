class AudioManager:
	def __init__(self, app):
		self.app = app

	def sfx(self, name):
		sound = self.app.resman.get_sound(name)
		sound.play()