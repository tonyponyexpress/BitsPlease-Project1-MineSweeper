class Space:
	"""The Space class stores all of the information relevant to a specific space on the board. Closer to a structure than an actual class

	**Class Variables**:
		*x_loc* = Integer location on the board. 0 is the left hand side.

		*y_loc* = Integer location on the board. 0 is the top of the board.

		*isMine* = Boolean that logs if the space has a mine. True if it does, false otherwise.

		*isFlagged* = Boolean that logs if the user placed a flag on this space. True if the user did.

		*IsRevealed* = Boolean that logs if the contents of the space are revealed to the user. True if the user should see the contents.

		*numOfSurroundingMines* = Integer that tracks how many spaces in the 8 closest spaces have mines."""
	def __init__(self, x_loc, y_loc):
		self.x_loc = x_loc
		self.y_loc = y_loc
		self.isMine = False
		self.isFlagged = False
		self.isRevealed = False
		self.numOfSurroundingMines = 0
		self.isCheatFlag = False
		self.isCheatSpace = False
