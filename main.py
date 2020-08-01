import pygame as pg
import os
import time
from tools import *
from guilib import *


class Main:
	def __init__(self):
		# Initialize pygame
		pg.init()
		# Initialize mainLoop and functionLoop
		self.mainLoop = True
		self.functionLoop = False
		# Set window dimensions
		self.winWidth = 900
		self.winHeight = 932
		# Create game window surface
		self.win = pg.display.set_mode((self.winWidth, self.winHeight))

		# Create font and clock
		self.font = pg.font.Font(None, 30)
		self.clock = pg.time.Clock()


		# Load colors
		self.backgroundColor = (255, 230, 255)
		self.nodeColor =  pg.Color("Black")
		self.menuColor = (255, 200, 200)
		self.fontColor = (220, 90, 220)
		# self.backgroundColor = (255, 255, 255)
		# self.nodeColor =  pg.Color("Black")
		# self.menuColor = (200, 200, 200)
		# self.fontColor = (0, 0, 0)

		#Load images to be used
		self.CloseButtonImage = pg.transform.scale(pg.image.load(os.path.join("images", "close.png")), (16, 16))

		self.switchOffImage = pg.image.load(os.path.join("images", "switchOff.png"))
		self.switchOnImage = pg.image.load(os.path.join("images", "switchOn.png"))

		self.ledOffImage = pg.image.load(os.path.join("images", "ledOff.png"))
		self.ledOnImage = pg.image.load(os.path.join("images", "ledOn.png"))

		self.emptyTimerImage = pg.image.load(os.path.join("images", "emptyTimer.png"))
		self.bottomTimerImage = pg.image.load(os.path.join("images", "bottomTimer.png"))
		self.bottomMiddleTimerImage = pg.image.load(os.path.join("images", "bottomMiddleTimer.png"))
		self.fullTimerImage = pg.image.load(os.path.join("images", "fullTimer.png"))
		self.topMiddleTimerImage = pg.image.load(os.path.join("images", "topMiddleTimer.png"))
		self.topTimerImage = pg.image.load(os.path.join("images", "topTimer.png"))

		self.sevenButton = pg.image.load(os.path.join("images", "empty.png"))
		self.emptyImage = pg.transform.scale(pg.image.load(os.path.join("images", "empty.png")), (96, 96))
		self.aImage = pg.transform.scale(pg.image.load(os.path.join("images", "a.png")), (96, 96))
		self.bImage = pg.transform.scale(pg.image.load(os.path.join("images", "b.png")), (96, 96))
		self.cImage = pg.transform.scale(pg.image.load(os.path.join("images", "c.png")), (96, 96))
		self.dImage= pg.transform.scale(pg.image.load(os.path.join("images", "d.png")), (96, 96))
		self.eImage = pg.transform.scale(pg.image.load(os.path.join("images", "e.png")), (96, 96))
		self.fImage = pg.transform.scale(pg.image.load(os.path.join("images", "f.png")), (96, 96))
		self.gImage = pg.transform.scale(pg.image.load(os.path.join("images", "g.png")), (96, 96))


		self.orImage = pg.image.load(os.path.join("images", "or.png"))
		self.andImage = pg.image.load(os.path.join("images", "and.png"))
		self.norImage = pg.image.load(os.path.join("images", "nor.png"))
		self.nandImage = pg.image.load(os.path.join("images", "nand.png"))
		self.xorImage = pg.image.load(os.path.join("images", "xor.png"))
		self.xnorImage = pg.image.load(os.path.join("images", "xnor.png"))
		self.notImage = pg.image.load(os.path.join("images", "not.png"))
		self.bufferImage = pg.image.load(os.path.join("images", "buffer.png"))


		self.halfImage = pg.image.load(os.path.join("images", "halfAdder.png"))
		self.fullImage = pg.image.load(os.path.join("images", "fullAdder.png"))


		self.CommandBlockImage = pg.image.load(os.path.join("images", "commandBlock.png"))


		# Create the input menu
		self.inputMenu = Menu("Inputs", self.win, self.menuColor, self.fontColor, True, True)
		# Create buttons for input menu
		self.inputMenu.addButton("Switch", self.switchOffImage, selectSwitch)
		self.inputMenu.addButton("Close", self.CloseButtonImage, self.inputMenu.close)

		# Create output menu
		self.outputMenu = Menu("Outputs", self.win, self.menuColor, self.fontColor, True, True)
		self.outputMenu.addButton("LED", self.ledOffImage, selectLED)
		self.outputMenu.addButton("Timer", self.emptyTimerImage, selectTimer)
		self.outputMenu.addButton("Seven Segment", self.sevenButton, selectSevenSegment)
		self.outputMenu.addButton("Close", self.CloseButtonImage, self.outputMenu.close)

		# Create the menu for logic gates
		self.gatesMenu = Menu("Logic Gates", self.win, self.menuColor, self.fontColor, True, True)
		self.gatesMenu.addButton("Or", self.orImage, selectOr)
		self.gatesMenu.addButton("And", self.andImage, selectAnd)
		self.gatesMenu.addButton("Nor", self.norImage, selectNor)
		self.gatesMenu.addButton("Nand", self.nandImage, selectNand)
		self.gatesMenu.addButton("Xor", self.xorImage, selectXor)
		self.gatesMenu.addButton("Xnor", self.xnorImage, selectXnor)
		self.gatesMenu.addButton("Not", self.notImage, selectNot)
		#self.gatesMenu.addButton("Buffer", self.bufferImage, None)
		self.gatesMenu.addButton("Close", self.CloseButtonImage, self.gatesMenu.close)

		# Create the menu for adders
		self.adderMenu = Menu("Adders", self.win, self.menuColor, self.fontColor, True, True)
		self.adderMenu.addButton("Half Adder", self.halfImage, selectHalfAdder)
		self.adderMenu.addButton("Full Adder", self.fullImage, selectFullAdder)
		self.adderMenu.addButton("Close", self.CloseButtonImage, self.adderMenu.close)


		# Create settings menu
		self.settingsMenu = Menu("Settings Menu", self.win, self.menuColor, self.fontColor, True, True)
		# Create images for settings menu
		self.ExitButtonImage = pg.transform.scale(pg.image.load(os.path.join("images", "exit.png")), (64, 64))
		self.settingsMenu.addText(str(
			"Command Block Code"
			), self.fontColor)
		# Add entries to settings menu
		self.settingsEntry = self.settingsMenu.addEntry(pg.Color("Black"), pg.Color("White"))
		self.settingsMenu.addButton("Deploy Command Block", self.CommandBlockImage, selectCommandBlock)
		# Add buttons to settings menu
		self.settingsMenu.addButton("Exit", self.ExitButtonImage, quit)
		self.settingsMenu.addButton("Close", self.CloseButtonImage, self.settingsMenu.close)

		# Create the menu bar at the top of the screen
		self.menuBar = Menu("Menu", self.win, self.menuColor, self.fontColor, False, False, 0, 0, self.winWidth, 32)
		# Open the menu bar. It will always be open
		self.menuBar.open()
		# Load images for the menu bar
		self.InputButtonImage = pg.image.load(os.path.join("images", "input.png"))
		self.OutputButtonImage = pg.image.load(os.path.join("images", "output.png"))
		self.SettingsButtonImage = pg.image.load(os.path.join("images", "settings.png"))
		# Create buttons for the menu bar
		self.menuBar.addButton("Inputs", self.InputButtonImage, self.inputMenu.open)
		self.menuBar.addButton("Outputs", self.OutputButtonImage, self.outputMenu.open)
		self.menuBar.addButton("Logic Gates", self.orImage, self.gatesMenu.open)
		self.menuBar.addButton("Adders", self.halfImage, self.adderMenu.open)
		self.menuBar.addButton("Settings", self.SettingsButtonImage, self.settingsMenu.open)

		# Create a list of images for loading and checking in the future
		self.menus = [self.menuBar, self.settingsMenu, self.inputMenu, self.outputMenu, self.gatesMenu, self.adderMenu]

		# Create the grid list to hold nodes
		self.grid = []

		# Set grid dimensions. These should fit in with window dimensions
		self.gridRows = 60
		self.gridColumns = 60
		self.gridWidth = self.winWidth // self.gridColumns
		self.gridHeight = (self.winHeight - 32) // self.gridRows

		# Set the current tool to None
		self.tool = None

		# Create list of wires
		self.wires = []

		# List of components
		self.components = []

		# Create all nodes
		for row in range(self.gridRows):
			for column in range(self.gridColumns):
				newNode = Node(self.gridWidth*column, self.gridHeight*row + 32)
				self.grid.append(newNode)

		# Calculate the margin to be used for determining selected nodes
		self.margin = (self.winWidth // self.gridColumns)%self.grid[0].r

	# Update the screen
	def update(self):
		pg.display.update()
		self.win.fill(self.backgroundColor)
		# Draw all nodes
		if program.mainLoop:
			for node in self.grid:
				node.draw(self.win, self.nodeColor)
				#node.draw(self.win, (25, 185, 25))

		# Draw all wires
		for wire in program.wires:
			wire.draw(program.win)
		# Draw all components
		for component in program.components:
			component.draw(program.win)

		if program.mainLoop:
		# Draw all open menus
			for menu in self.menus:
				menu.draw()
		if program.functionLoop:
			fps = program.font.render("FPS: " + str(int(self.clock.get_fps())), True, pg.Color("Black"))
			self.win.blit(fps, (10, 10))
		# Free up some cpu
		self.clock.tick(30)
		#time.sleep(0.02)

# Functions for selecting each tool
def selectSwitch():
	x, y = pg.mouse.get_pos()
	program.tool = Switch(getPoint((x, y), program.grid, program.margin), program.switchOnImage, program.switchOffImage)
	program.tool.update()
def selectLED():
	x, y = pg.mouse.get_pos()
	program.tool = LED(getPoint((x,y), program.grid, program.margin), program.ledOnImage, program.ledOffImage)
	program.tool.update()
def selectTimer():
	x, y = pg.mouse.get_pos()
	images = [program.emptyTimerImage,
	program.bottomTimerImage,
	program.bottomMiddleTimerImage,
	program.fullTimerImage,
	program.topMiddleTimerImage,
	program.topTimerImage
	]
	program.tool = Timer(getPoint((x,y), program.grid, program.margin), images, program.grid, program.margin)
	program.tool.update()
def selectSevenSegment():
	x, y = pg.mouse.get_pos()
	images = [program.emptyImage,
	program.aImage,
	program.bImage,
	program.cImage,
	program.dImage,
	program.eImage,
	program.fImage,
	program.gImage
	]
	program.tool = SevenSegment(getPoint((x,y), program.grid, program.margin), images, program.grid, program.margin)
	program.tool.update()
def selectOr():
	x, y = pg.mouse.get_pos()
	image = program.orImage
	program.tool = OrGate(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectAnd():
	x, y = pg.mouse.get_pos()
	image = program.andImage
	program.tool = AndGate(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectNor():
	x, y = pg.mouse.get_pos()
	image = program.norImage
	program.tool = NorGate(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectNand():
	x, y = pg.mouse.get_pos()
	image = program.nandImage
	program.tool = NandGate(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectXor():
	x, y = pg.mouse.get_pos()
	image = program.xorImage
	program.tool = XorGate(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectXnor():
	x, y = pg.mouse.get_pos()
	image = program.xnorImage
	program.tool = XnorGate(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectNot():
	x, y = pg.mouse.get_pos()
	image = program.notImage
	program.tool = NotGate(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectHalfAdder():
	x, y = pg.mouse.get_pos()
	image = program.halfImage
	program.tool = HalfAdder(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectFullAdder():
	x, y = pg.mouse.get_pos()
	image = program.fullImage
	program.tool = FullAdder(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin)
	program.tool.update((x,y), program.grid, program.margin)
def selectCommandBlock():
	x, y = pg.mouse.get_pos()
	image = pg.transform.scale(program.CommandBlockImage, (96, 96))
	program.tool = CommandBlock(getPoint((x,y), program.grid, program.margin), image, program.grid, program.margin, program.settingsEntry.getContents())
	program.tool.update((x,y), program.grid, program.margin)

# Function for drawing the selected tool as the mouse moves
def drawTool():
	pos = pg.mouse.get_pos()
	for menu in program.menus:
		if menu != program.menuBar:
			if menu.opened:
				return
	if program.tool:
		try:
			program.tool.update(pos, program.grid, program.margin)
			program.tool.draw(program.win)
		except:
			return


# Function for placing the selected tool
def place():
	pos = pg.mouse.get_pos()
	for menu in program.menus:
		if menu != program.menuBar:
			if menu.opened:
				return
	if program.tool:
		try:
			program.tool.update(pos, program.grid, program.margin)
		except:
			return

		program.components.append(program.tool)
		toolType = type(program.tool)
		program.tool = None




# A loop for drawing wires
def drawing(status, position):
	# Dont draw a wire if any menus are open
	for menu in program.menus:
		if menu.opened and menu != program.menuBar:
			return
	# Create new wire
	newWire = Wire(position)
	# While this loop is true, continue drawing the wire
	while status:
		for event in pg.event.get():
			# Place the wire
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button != 4 and event.button != 5:
					program.wires.append(newWire)
					status = False
			# Update the wire with the mouse
			elif event.type == pg.MOUSEMOTION:
				pos = getPoint(pg.mouse.get_pos(), program.grid, program.margin)
				if pos == None:
					pos = program.grid[0]
				newWire.update(pos)
			# Cancel the wire placement
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_e:
					status = False
		# Draw the wire throughout the loop
		newWire.draw(program.win)
		program.update()

# Main function loop
def main():
	# While the mainLoop (sketching the blueprint)
	while program.mainLoop:
		for event in pg.event.get():
			# Close the program
			if event.type == pg.QUIT:
				program.mainLoop = False
				program.functionLoop = False
				return
			# Listen for left click
			elif event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:
					place()
					x, y = pg.mouse.get_pos()
					# Check if user is clicking a menu button
					for menu in program.menus:
						if menu.opened:
							for widget in menu.contents:
								if widget.inRange(x, y):
									try:
										widget.clicked()
										pass
									except TypeError:
										continue
				# Listen for right click
				elif event.button == 3:
					drawing(True, getPoint(pg.mouse.get_pos(), program.grid, program.margin))
			# Listen for keyboard input
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_RETURN:
					program.functionLoop = True
					program.mainLoop = False
					main()
				elif event.key == pg.K_DELETE:
					point = getPoint(pg.mouse.get_pos(), program.grid, program.margin)
					for component in program.components:
						for node in component.nodes:
							if node == point:
								program.components.remove(component)
					for wire in program.wires:
						for node in wire.nodes:
							if node == point:
								program.wires.remove(wire)
								break
				# Check if user is typing in entry box
				for menu in program.menus:
					if menu.opened:
						for widget in menu.contents:
							widget.typing(event.key, event.unicode)
		drawTool()
		program.update()

	# The loop for the electrical circuit to play out
	while program.functionLoop:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				program.functionLoop = False
				program.mainLoop = False
				return
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_BACKSPACE:
					program.functionLoop = False
					program.mainLoop = True
					main()
			elif event.type == pg.MOUSEBUTTONDOWN:
				for component in program.components:
					component.checkClick()

		# Call the wires to function
		for wire in program.wires:
			wire.function()
		# Call all components to function
		for component in program.components:
			component.function()
		program.update()


# Run setup
program = Main()
# Run the program
main()