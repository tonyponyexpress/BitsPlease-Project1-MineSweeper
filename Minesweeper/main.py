from pygame import event, constants, time
from enum import Enum
from Minesweeper.Minesweeper import Minesweeper
from Minesweeper.Minefield import Minefield
from Minesweeper.StartScreen import StartScreen
from Minesweeper.EndScreen import EndScreen
from Minesweeper.CheatMode import CheatMode
import pygame
pygame.init()
pygame.mixer.init()

def main():
	"""
	The __main__ class utilizes a finite state machine structure to manage the overall flow
	of the game from start up to game ending.

	**States**
		There are five states that the game undergoes. The states and their interactions summarized:

		*Start*: The default state when the game is first run. This state creates the StartScreen, which
		asks players what board size they perfer and the number of mines on the board. This state will end
		either when the player quits the game with a state *Exit* or generates a game with a state *Minesweeper*.

		*Minesweeper*: This state runs when the player is actually playing minesweeper. This state monitors how the game
		is progressing. Once the player wins or loses, this state will record the outcome then change state.
		There are only two ways to change state - when the game is won or lost with a state *End* or when the player quits
		the game with a state *Exit*.

		*End*: This state throws up the appropirate end screen depending on whether or not the player won or lost. Then,
		awaits whether or not the player quits the game with a state *Exit* or starts a new game with state *Start*.

		*Exit*: This state exits out of the finite state machine and terminates the application.

		*CheatMode*: This state runs when the player enters cheat mode. This state shows the location of the mines and the
		number of the spaces with adjacent mines. When the user exits cheat mode it goes back to Minesweeper state


	**Args**:
			None.

	**Preconditions**:
			None.

	**Postconditions**:
			None.

	**Returns**:
			None.
	"""
	clock = time.Clock()
	State = Enum('State','Start Minesweeper End Exit CheatMode')
	currentState = State.Start
	startScreen = None
	minesweeper = None
	endScreen = None
	cheatMode = None
	x,y,mines = 0, 0, 0

	while currentState != State.Exit:
		if (currentState == State.Start):
			if startScreen is None:
				if minesweeper is None:
					startScreen = StartScreen()
				else:
					startScreen = StartScreen(x, y, mines)
			for newEvent in event.get():
				if newEvent.type == constants.QUIT:
					currentState = State.Exit
			startScreen.render()
			clock.tick(60)
			if startScreen.gameReady:
				currentState = State.Minesweeper
				x, y, mines = startScreen.x_size, startScreen.y_size, startScreen.numMines
				minesweeper = Minesweeper(x, y, mines)
				startScreen = None

		elif currentState == State.Minesweeper:
			for newEvent in event.get():
				if newEvent.type == constants.QUIT:
					currentState = State.Exit
				elif newEvent.type == constants.MOUSEBUTTONDOWN:
					(end, win) = minesweeper.onClick(newEvent)
					if end:
						if win is None:
							currentState = State.Start
						else:
							currentState = State.End
							if not win:
								minesweeper.onLose()
							endScreen = EndScreen(win)
                    ###################################### new for cheat mode ######################################
					elif win is None:
						pygame.mixer.stop();
						cheatGame = pygame.mixer.Sound("sounds/cheatmode.wav")
						cheatGame.play()
						minesweeper.cheatFlags()
						cheatMode = CheatMode()
						currentState = State.CheatMode
                    ################################################################################################
			minesweeper.render()
			clock.tick(60)

		elif currentState == State.End:
			endScreen.render()
			clock.tick(60)

			for newEvent in event.get():
				if newEvent.type == constants.QUIT:
					currentState = State.Exit
				elif newEvent.type == constants.MOUSEBUTTONDOWN:
					currentState = State.Start
					endScreen = None

        ###################################### new for cheat mode ######################################
		elif currentState == State.CheatMode:
			cheatMode.render()
			for newEvent in event.get():
				if newEvent.type == constants.QUIT:
					currentState = State.Exit
				elif newEvent.type == constants.MOUSEBUTTONDOWN:
					minesweeper.undoCheatFlags()
					currentState = State.Minesweeper
					cheatMode = None
        ################################################################################################

		else:
			currentState = State.Start
			print('Error: This really should never happen, resetting game...')
