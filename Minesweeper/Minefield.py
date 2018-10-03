from Minesweeper.Space import Space
import random
import pygame

pygame.init()
pygame.mixer.init()

class Minefield:
	"""Minefield manages the internal game logic. The backend of the game board.

	Minefield is designed to be our internal game engine. In this class, there is logic to determine where the mines are placed, to reveal the gameboard, and deal with flags.

	**Class Variables**:
			*x_size*: Integer x size of board

			*y_size*: Integer y size of board

			*numMines*: Integer number of mines

			*minefield*: 2D array to track where the mines are located.
	"""

	def __init__(self, x_size, y_size, numMines):

		self.x_size = x_size
		self.y_size = y_size
		self.numMines = numMines

		#initialize minefield array
		self.minefield = [[Space(x,y) for x in range(x_size)] for y in range(y_size)]

		# for y in range(self.y_size):
		# 	self.minefield[y] = []
		# 	for x in range(self.x_size):
		# 		self.minefield[y][x] = Space(x, y)

		#set mines in the minefield
		self.setMines()

		#initialize surrounding mine numbers
		for y in range(self.y_size):
			for x in range(self.x_size):
				self.checkNeighbors(x, y)

	def setMines(self):
		"""setMines randomly places the mines around the board.

		**Args**:
				None.

		**Preconditions**:
				Spaces are created and stored.

		**Postconditions**:
				isMine altered in numMines spaces

		**Returns**:
				None."""

		currentMines = 0
		random.seed()

		while currentMines < self.numMines:
			mine_x, mine_y = random.randrange(self.x_size), random.randrange(self.y_size)
			thisSpace = self.getSpace(mine_x, mine_y)

			if not thisSpace.isMine:
				thisSpace.isMine = True
				currentMines += 1

	def checkNeighbors(self, x, y):
		"""Determines the number of mines that are directly around a certain space.

			**Args**:
				*x*: the x coordinate of the space (start at 0)

                                *y*: the y coordinate of the space (start at 0)

			**Preconditions**:
				The mines must already be placed in the grid, spaces must exist

			**Postconditions**:
				Sets the variable numOfSurroundingMines in the space in x,y to the integer number of mines touching that space.

                        **Return**:
                                None."""
		#Using the count variable to monitor the number of surrounding mines
		count = 0
		leftX = 0 if x == 0 else x-1
		rightX = self.x_size-1 if x == self.x_size-1 else x+1
		leftY = 0 if y == 0 else y-1
		rightY = self.y_size-1 if y == self.y_size-1 else y+1

		checkCoordinates = [(xCoord, yCoord) for xCoord in range(leftX, rightX+1) for yCoord in range(leftY, rightY+1) if not (xCoord, yCoord) == (x,y)]
		for gridPoint in checkCoordinates:
			if (self.getSpace(gridPoint[0],gridPoint[1]).isMine):
				count += 1

		self.getSpace(x, y).numOfSurroundingMines = count

	def checkFlags(self):
		"""Checks to see all of mined spaces have flags

			**Args**:
					None.

			**Preconditions**:
					The mines must already be placed in grid, spaces must exist

			**Postconditions**:
					None.

			**Returns**:
					True if all the mines have a flag on them, false otherwise
		"""
		isComplete = True
		for y in range(self.y_size):
			for x in range(self.x_size):
				if self.getSpace(x, y).isFlagged != self.getSpace(x,y).isMine:
					isComplete = False
		if isComplete:
			pygame.mixer.stop();
			winGame = pygame.mixer.Sound("sounds/WINNER.wav")
			winGame.play()
		return isComplete

	def reveal(self, x, y):
		"""Determines whether or not to reveal a space.

			Specifically, it reveals a space when it is clicked, as well as all empty spaces around the clicked space.

                        It also reveals the board if a mine is clicked.

			**Args**:
					*x*: x-coordinate of the space (starts at 0)

                                        *y*: y-coordinate of the space (starts at 0)

			**Preconditions**:
					x and y coordinates are legitimate (i.e. 0 <= x < self.xsize and 0 <= y < self.ysize)

			**Postconditions**:
					Set Revealed to True if space is to be revealed

			**Return**:
					True if space is revealed, false otherwise
		"""
		thisSpace = self.getSpace(x, y)

		thisSpace.isRevealed = True
		if thisSpace.isMine:
			loseGame = pygame.mixer.Sound("sounds/mine.wav")
			loseGame.play()
			return True
		else:
			if thisSpace.numOfSurroundingMines == 0:
				blankSound = pygame.mixer.Sound("sounds/blankspace.wav")
				blankSound.play()
				x_range, y_range = range(x - 1, x + 2), range(y - 1, y + 2)
				for y_curr in y_range:
					for x_curr in x_range:
						if (x_curr >= 0 and y_curr >= 0) and (x_curr < self.x_size and y_curr < self.y_size) and not (x_curr == x and y_curr == y):
							if (not self.getSpace(x_curr, y_curr).isRevealed) and (not self.getSpace(x_curr, y_curr).isFlagged):
								self.reveal(x_curr, y_curr)

			return False

	def toggleFlag(self, x, y):
		"""Toggles whether or not a flag is on the space defined by x and y.

				**Args:**
								*x*: x-coordinate of the space (starts at 0)

								*y*: y-coordinate of the space (starts at 0)

				**Preconditions**:
								x and y coordinates are legitimate (i.e. 0 <= x < self.xsize and 0 <= y < self.ysize)

				**Postconditions**:
								Flips value of isFlagged on specific space

				**Return**:
								None.
		"""
		self.minefield[y][x].isFlagged = not self.getSpace(x, y).isFlagged
		if (self.minefield[y][x].isFlagged and not(self.checkFlags())):
						flagOn = pygame.mixer.Sound("sounds/flagon.wav")
						flagOn.play()

		else:
			flagOff = pygame.mixer.Sound("sounds/flagoff.wav")
			flagOff.play()

		# if thisSpace.isFlagged == False:
		# 	thisSpace.isFlagged = True
		# else:
		# 	thisSpace.isFlagged = False

	def getSpace(self, x, y):
		"""Getter that returns a space object at location x, y

				**Args:**
								*x*: x-coordinate of the space (starts at 0)

								*y*: y-coordinate of the space (starts at 0)

				**Preconditions**:
								x and y coordinates are legitimate (i.e. 0 <= x < self.xsize and 0<= y < self.ysize)

				**Postconditions**:
								None.

				**Return**:
								Returns the space at location x, y to the caller.
		"""
		return self.minefield[y][x]
