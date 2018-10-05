from pygame import font, display, time, event, constants, init
from pygame.locals import Rect, Color
import math

class Window:
	"""
		Window class controls interactions with the pygame surfaces of the parent window and subsurfaces of the various game elements

		**Class Variables**:
			*self.x_dim*: number of game tiles, x dimension

			*self.y_dim*: number of game tiles, y dimension

			*self.SPACE_PIXELS*: const, size of single square size

			*self.MARGIN*: const, width of margin

			*self.HEADER_BAR*: const, header bar height

			*self.WIDTH*: const, window width

			*self.HEIGHT*: const, window height

			*self.BUTTON_WIDTH*: const, width of reset and cheat mode button element

			*self.TIMER_WIDTH*: const, width of timer text

			*self.FLAG_COUNTER_HEIGHT*: const, height of flag counter text

			*self.FLAG_COUNTER_WIDTH*: const, width of flag counter text

			*self.GAME_SCREEN_LEFT*: const, left-most pixel value of game screen

			*self._screen*: Surface object, parent window

			*self._gameScreen*: Surface object, game grid element

			*self._reset*: Surface object, reset button element

			*self._timer*: Surface object, timer text element

			*self._flagCounter*: Surface object, flag counter text element

	"""
	def __init__(self, x_dim, y_dim):

		init()

		# Dimensions Game Screen (grid)
		self.x_dim = x_dim
		self.y_dim = y_dim
		self.MARGIN = 8
		self.HEADER_BAR = 70
		self.SPACE_PIXELS = 32

		if (self.SPACE_PIXELS*self.x_dim + 2 * self.MARGIN) < 550 :
			self.WIDTH = 550
		else:
			self.WIDTH = self.SPACE_PIXELS*self.x_dim + 2 * self.MARGIN

		self.HEIGHT = self.SPACE_PIXELS*self.y_dim + 2 * self.MARGIN + self.HEADER_BAR
		self._screen = display.set_mode((self.WIDTH, self.HEIGHT))
		display.set_caption("BitSweeper")

		if (self.x_dim*self.SPACE_PIXELS) < self.WIDTH :
			self.GAME_SCREEN_LEFT = (self.WIDTH / 2) - ((self.x_dim* self.SPACE_PIXELS) / 2)
		else :
			self.GAME_SCREEN_LEFT = self.MARGIN

		# Dimensions buttons
		self.BUTTON_WIDTH = math.floor(self.WIDTH/3)

		# Dimensions timer and flag counter
		self.TIMER_WIDTH = 150
		self.FLAG_COUNTER_HEIGHT = 20
		self.FLAG_COUNTER_WIDTH = 150


		# Game Screen (grid)
		self._gameScreen = self._screen.subsurface(
				Rect(self.GAME_SCREEN_LEFT, self.HEADER_BAR + self.MARGIN, self.SPACE_PIXELS*self.x_dim, self.SPACE_PIXELS*self.y_dim)
			)

		# Reset button
		self._reset = self._screen.subsurface(
				Rect(self.MARGIN, self.MARGIN, self.BUTTON_WIDTH, self.HEADER_BAR-self.MARGIN)
			)

		# Timer and flag counter
		self._timer = self._screen.subsurface(
				Rect(self.MARGIN + self.BUTTON_WIDTH + self.MARGIN, self.MARGIN, self.TIMER_WIDTH, self.FLAG_COUNTER_HEIGHT)
			)
		self._flagCounter = self._screen.subsurface(
				Rect(self.MARGIN + self.BUTTON_WIDTH + self.MARGIN, self.MARGIN + self.FLAG_COUNTER_HEIGHT, self.FLAG_COUNTER_WIDTH, self.FLAG_COUNTER_HEIGHT)
			)

		self._screen.fill(Color('light grey'))

        # Cheat Mode button
		self.CHEATMODE_WIDTH = math.floor(self.WIDTH/3)
		self._cheatMode = self._screen.subsurface(
				Rect(self.MARGIN + self.BUTTON_WIDTH + self.MARGIN + self.TIMER_WIDTH + self.MARGIN, self.MARGIN, self.CHEATMODE_WIDTH, self.HEADER_BAR-self.MARGIN)
			)

		display.flip()

	def onClick(self, newEvent):
		"""
		On click handler for window

		**Args**:
				*newEvent*: pygame Event object, newEvent.pos: pixel location of click, newEvent.button: mouse button clicked

		**Preconditions**:
				None.

		**Postconditions**:
				None.

		**Returns**:
				pygame Event object, with same button and gid location if on grid, else button=-1 if on reset button, else None
		"""
		x,y = newEvent.pos
		x_game, y_game = (math.floor((x-self.GAME_SCREEN_LEFT)/self.SPACE_PIXELS), math.floor((y-self.MARGIN-self.HEADER_BAR)/self.SPACE_PIXELS))

		if not (0 <= x_game <= self.x_dim-1 and 0 <= y_game <= self.y_dim-1):
			# reset button
			if (self.MARGIN<=x<self.BUTTON_WIDTH and self.MARGIN<=y<self.HEADER_BAR-self.MARGIN ):
				x_min,y_min = self._reset.get_abs_offset()
				x_reset_size, y_reset_size = self._reset.get_size()
				(x_max, y_max) = (x_min + x_reset_size, y_min + y_reset_size)
				if (x_min <= x <= x_max) and (y_min <= y <= y_max):
					return event.Event(constants.MOUSEBUTTONDOWN, {'pos': newEvent.pos, 'button': -1})
				return None
			# cheat mode button
			else:
				x_min,y_min = self._cheatMode.get_abs_offset()
				x_cheatMode_size, y_cheatMode_size = self._cheatMode.get_size()
				(x_max, y_max) = (x_min + x_cheatMode_size, y_min + y_cheatMode_size)
				if (x_min <= x <= x_max) and (y_min <= y <= y_max):
					return event.Event(constants.MOUSEBUTTONDOWN, {'pos': newEvent.pos, 'button': -2})
				return None
		return event.Event(constants.MOUSEBUTTONDOWN, {'pos': (x_game, y_game), 'button': newEvent.button})
