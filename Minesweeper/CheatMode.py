from pygame import surface, display, constants
from pygame.font import SysFont
from pygame.locals import Color

class CheatMode:

	def __init__(self):
		self.gameSurf = display.get_surface().copy()
		self.drawWindow = display.get_surface()
		self.transparentSurf = surface.Surface(display.get_surface().get_size(), constants.SRCALPHA)

		color = (0,2, 0, 127)
		text = "Cheat Mode!"
		backgroundColor = 'blue'
		title = SysFont('lucidaconsole', 25)
		subtitle = SysFont('lucidaconsole', 15)

	def render(self):
		self.drawWindow.blit(self.gameSurf, (0,0))
		self.drawWindow.blit(self.transparentSurf, (0,0), None, constants.BLEND_RGBA_MULT)
		display.flip()
