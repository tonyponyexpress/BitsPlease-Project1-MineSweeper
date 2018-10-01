import pygame
from pygame import display, time, font, draw, init
from pygame.locals import Rect, Color
from Minesweeper.Graphics.Drawer import Drawer

pygame.init()
pygame.mixer.init()

class StartScreen:
	"""StartScreen manages user imput for the variables needed to make a minesweeper game, such as size and mine count

	**Class Variables**:
		*min_size*: Integer The minimum board size to be allowed by the game

		*max_y*: Integer The maximum board height to be allowed by the game

		*max_x*: Integer The maximum board width to be allowed by the game

		*x_size*: Integer Keeps track of the selected board width

		*y_size*: Integer Keeps track of the selected board height

		*numMines*: Integer The currently selected number of mines

		*window*: Surface The render surface that all other screen items will be drawn onto

		*window_margin*: Integer Number of Pixels to use between screen elements

		*sizeSurface*: Surface Subsurface of window. Used to hold board size menu

		*mineSurface*: Surface Subsurface of window. Used to hold mine count menu

		*startSurface*: Surface subsurface of window. Holds the "start" button

		*title*: Font Stored font and font size for more emphasized text

		*subtitle*:	Font Stored font and font size for less emphasized text

		*drawer*: Drawer used to draw the buttons on the menu screen
	"""
	def __init__(self, x_size_init = 9, y_size_init = 9, numMines_init = 10):
		init()

		#limits on board size selections
		self.min_size = 2
		self.max_y = 20
		self.max_x = 40

		#initialize member variables with initial values
		self.x_size = x_size_init
		self.y_size = y_size_init
		self.numMines = numMines_init

		#create a new display window of size (x, y)
		self.window = display.set_mode((600, 500))

		self.window_margin = 20

		#define subsurfaces for rendering different menu components
		self.sizeSurface = self.window.subsurface(Rect(self.window_margin, self.window_margin, self.window.get_width() / 2 - 1.5*self.window_margin - 1, self.window.get_height() - 2 * self.window_margin - 100))
		self.mineSurface = self.window.subsurface(Rect((self.window.get_width() / 2) + .5*self.window_margin, self.window_margin, self.window.get_width() / 2 - 1.5*self.window_margin, self.window.get_height() - 2 * self.window_margin - 100))
		self.startSurface = self.window.subsurface(Rect(self.window_margin, 400, self.window.get_width() - 2*self.window_margin, 100 - self.window_margin))

		#initialize colors of the surfaces
		self.window.fill(Color('light grey'))
		self.sizeSurface.fill(Color('dark grey'))
		self.mineSurface.fill(Color('dark gray'))

		#intialize different font sizes
		self.title = font.SysFont('lucidaconsole', 30)
		self.subtitle = font.SysFont('lucidaconsole', 25)

		#initialize the Drawer
		self.drawer = Drawer()

		#initialize the ready flag
		self.gameReady = False

	def render(self):
		"""
		Renders labels, buttons, and live counts of selected board size and mine count.

		**Args**:
				None.

		**Preconditions**:
				None.

		**Postconditions**:
				Menu elements will be drawn to StartScreen's surface

		**Returns**:
				None.
		"""
		#render texts for the labels
		sizeLabel = self.title.render("Size:", True, Color('black'))
		sizeLabel_x = self.subtitle.render("Width:", True, Color('black'))
		sizeLabel_y = self.subtitle.render("Height:", True, Color('black'))
		mineLabel = self.title.render("Mines:", True, Color('black'))

		currSize_x = self.subtitle.render(str(self.x_size), True, Color('white'))
		currSize_y = self.subtitle.render(str(self.y_size), True, Color('white'))
		currMines = self.subtitle.render(str(self.numMines), True, Color('white'))

		#find the positions of these labels
		sizeLabelPos = (self.sizeSurface.get_width() / 2 - sizeLabel.get_width() / 2, 20)
		sizeLabelPos_x = (self.sizeSurface.get_width() / 4 - sizeLabel.get_width() / 2, 60)
		sizeLabelPos_y = (3 * self.sizeSurface.get_width() / 4 - sizeLabel.get_width() / 2, 60)
		mineLabelPos = (self.mineSurface.get_width() / 2 - mineLabel.get_width() / 2, 30)

		#define common vars for the buttons
		buttonWidth_x = sizeLabel_x.get_width()
		buttonWidth_mine = mineLabel.get_width()
		buttonLeft_x = self.sizeSurface.get_width() / 4 - sizeLabel.get_width() / 2
		buttonLeft_y = 3 * self.sizeSurface.get_width() / 4 - sizeLabel.get_width() / 2
		buttonLeft_mine = self.mineSurface.get_width() / 2 - mineLabel.get_width() / 2

		buttonTop = sizeLabel_x.get_height() + 80

		#seperate colors for the start button
		startButtonColors = ( (0, 180, 0), (0, 156, 0) )
		buttonSize_size = (sizeLabel_x.get_width(), 60)
		buttonHeight= 60
		buttonColors = ( (128,128,128), (96,96,96) )
		#  Inc Width Button
		incButtonSizeX_pos = (self.sizeSurface.get_width() / 4 - sizeLabel.get_width() / 2, buttonTop)
		self.drawer.drawButton(self.sizeSurface, incButtonSizeX_pos, buttonSize_size, buttonColors, "+", 25, self.incWidth)

		#  Dec Width Button
		decButtonSizeX_pos = (incButtonSizeX_pos[0], buttonTop + 2*buttonSize_size[1])
		self.drawer.drawButton(self.sizeSurface, decButtonSizeX_pos, buttonSize_size, buttonColors, "-", 25, self.decWidth)

		#  Inc Height Button
		incButtonSizeY_pos = (3 * self.sizeSurface.get_width() / 4 - sizeLabel.get_width() / 2, buttonTop)
		self.drawer.drawButton(self.sizeSurface, incButtonSizeY_pos, buttonSize_size, buttonColors, "+", 25, self.incHeight)

		#  Dec Height Button
		decButtonSizeY_pos = (incButtonSizeY_pos[0], buttonTop + 2*buttonSize_size[1])
		self.drawer.drawButton(self.sizeSurface, decButtonSizeY_pos, buttonSize_size, buttonColors, "-", 25, self.decHeight)

		#  Inc Mines Button
		incButtonMines_pos = (self.mineSurface.get_width() / 2 - mineLabel.get_width() / 2, buttonTop)
		buttonMines_size = (mineLabel.get_width(), 60)
		self.drawer.drawButton(self.mineSurface, incButtonMines_pos, buttonMines_size, buttonColors, "+", 25, self.incMines)

		#  Dec Mines Button
		decButtonMines_pos = (incButtonMines_pos[0], buttonTop + 2*buttonMines_size[1])
		self.drawer.drawButton(self.mineSurface, decButtonMines_pos, buttonMines_size, buttonColors, "-", 25, self.decMines)

		#  Start Button
		self.drawer.drawButton(self.startSurface, (0, 0), self.startSurface.get_size(), startButtonColors, "Start!", 30, self.start)

		draw.rect(self.sizeSurface, Color('black'), (buttonLeft_x, buttonTop + buttonHeight, buttonWidth_x, buttonHeight))
		draw.rect(self.sizeSurface, Color('black'), (buttonLeft_y, buttonTop + buttonHeight, buttonWidth_x, buttonHeight))
		draw.rect(self.mineSurface, Color('black'), (buttonLeft_mine, buttonTop + buttonHeight, buttonWidth_mine, buttonHeight))

		currSizePos_x = (self.sizeSurface.get_width() / 4 - currSize_x.get_width() / 2, buttonTop + buttonHeight * 1.5 - currSize_x.get_height() / 2)
		currSizePos_y = (3 * self.sizeSurface.get_width() / 4 - currSize_y.get_width() / 2, buttonTop + buttonHeight * 1.5 - currSize_y.get_height() / 2)
		currMinesPos = (self.mineSurface.get_width() / 2 - currMines.get_width() / 2, buttonTop + buttonHeight * 1.5 - currMines.get_height() / 2)

		#draw the labels to the screen
		self.sizeSurface.blits([
			(sizeLabel, sizeLabelPos),
			(sizeLabel_x, sizeLabelPos_x),
			(sizeLabel_y, sizeLabelPos_y),
			(currSize_x, currSizePos_x),
			(currSize_y, currSizePos_y)
		])
		self.mineSurface.blits([
			(mineLabel, mineLabelPos),
			(currMines, currMinesPos)
		])


		display.flip()

	def incWidth(self):
		"""
		Helper function to increment the selected width of the board

		**Args**:
				None.

		**Preconditions**:
				Current x_size must be a number

		**Postconditions**:
				x_size will be less than or equal to the max x size specified

		**Returns**:
				None.
		"""
		if self.x_size < self.max_x:
			self.x_size += 1

	def decWidth(self):
		"""
		Helper function to decrement the selected width of the board

		**Args**:
				None.

		**Preconditions**:
				Current x_size must be a number

		**Postconditions**:
				x_size will be greater than or equal to the minimum x size specified.
				Also, the selected number of mines will be less than the area of the board.

		**Returns**:
				None.
		"""
		if self.x_size > self.min_size:
			self.x_size -= 1
		if self.numMines >= self.x_size * self.y_size:
			self.numMines = self.x_size * self.y_size - 1

	def incHeight(self):
		"""
		Helper function to increment the selected height of the board

		**Args**:
				None.

		**Preconditions**:
				Current y_size must be a number

		**Postconditions**:
				y_size will be less than or equal to the max y size specified

		**Returns**:
				None.
		"""
		if self.y_size < self.max_y:
			self.y_size += 1

	def decHeight(self):
		"""
		Helper function to decrement the selected height of the board

		**Args**:
				None.

		**Preconditions**:
				Current y_size must be a number

		**Postconditions**:
				y_size will be greater than or equal to the minimum x size specified.
				Also, the selected number of mines will be less than the area of the board.

		**Returns**:
				None.
		"""
		if self.y_size > self.min_size:
			self.y_size -= 1
		if self.numMines >= self.x_size * self.y_size:
			self.numMines = self.x_size * self.y_size - 1

	def incMines(self):
		"""
		Helper function to increment the selected number of mines on the board

		**Args**:
				None.

		**Preconditions**:
				Current numMines must be a number

		**Postconditions**:
				numMines will be less than the total number of spaces available on the board

		**Returns**:
				None.
		"""
		if self.numMines < self.x_size * self.y_size - 1:
			self.numMines += 1

	def decMines(self):
		"""
		Helper function to decrement the selected number of mines on the board

		**Args**:
				None.

		**Preconditions**:
				Current numMines must be a number

		**Postconditions**:
				numMines will be at least 1

		**Returns**:
				None.
		"""
		if self.numMines > 1:
			self.numMines -= 1

	def start(self):
		"""
		Sets the gameReady flag to True. This is the signal for a top level class to move on to the game

		**Args**:
				None.

		**Preconditions**:
				None

		**Postconditions**:
				gameReady will be True

		**Returns**:
				None.
		"""
		startGame = pygame.mixer.Sound("sounds/gameStart.wav")
		self.gameReady = True
		startGame.play()
