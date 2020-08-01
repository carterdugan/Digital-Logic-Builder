import pygame as pg

# Initialize pygame
pg.init()
# Set the button highlight color
buttonHighlightColor = pg.Color("White")
# Create the font
font = pg.font.Font(None, 20)
# On tick and off tick for the timer
onTick = 300
offTick = 600

# Custom error class
class CustomError(Exception):
	pass

# Widget super class that handles all default functions
class Widget:
	def inRange(self, x, y):
		if (x >= self.x
			and x < self.x + self.width
			and y > self.y
			and y < self.y + self.height):
			return True
		else:
			return False
	def typing(self, key, code):
		pass
	def clicked(self):
		pass

# Button class to add buttons to windows
class Button(Widget):
	def __init__(self, name, window, image, command):
		self.highlight = False
		self.name = name
		self.window = window
		self.surface = self.window.surface
		self.image = image
		self.command = command

		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0

		self.hover = Hover(self.surface, self.name)

	# Check if the button was clicked
	def clicked(self):
		self.command()

	# Function  for drawig the button
	def draw(self):
		x, y = pg.mouse.get_pos()
		if self.inRange(x, y):
			self.highlight = True
		else:
			self.highlight = False
		if self.highlight:
			pg.draw.rect(
				self.surface,
				buttonHighlightColor,
				(
				self.x,
				self.y,
				self.width,
				self.height
					)
				)
		self.surface.blit(self.image, (self.x, self.y))
		if self.highlight:
			self.hover.x = x
			self.hover.y = y
			self.hover.draw()

# Class for user text entries
class Entry(Widget):
	def __init__(self, surface, window, fontColor, backgroundColor, text=""):
		self.click = False
		self.surface = surface
		self.window = window
		self.fontColor = fontColor
		self.backgroundColor = backgroundColor
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = font.render("Example", True, pg.Color("Black")).get_height()
		self.text = text
		self.cache = ""
		self.last = pg.time.get_ticks()
	def draw(self):
		now = pg.time.get_ticks()
		pg.draw.rect(
			self.surface,
			self.backgroundColor,
			(
				self.x,
				self.y,
				self.width,
				self.height
				)
			)
		if self.click and now - self.last >= 500:
			if now - self.last >= 1000:
				self.last = now

			self.surface.blit(font.render(str(self.text + "|"), True, self.fontColor), (self.x, self.y))
		else:
			self.surface.blit(font.render(str(self.text), True, self.fontColor), (self.x, self.y))
	
	# Check if the text entry was clicked
	def clicked(self):
		if self.click:
			self.click = False
		else:
			self.click = True
	# Handle all characters entered into the text field.
	# MUST be called from the keystroke listener
	def typing(self, key, code):
		if self.click:
			if key == pg.K_BACKSPACE:
				self.text = self.text[:-1]
				try:
					self.text = self.cache[-1] + self.text
					self.cache = self.cache[:-1]
				except:
					pass
			elif len(code) == 1:
				self.text = str(self.text + code)
				while font.render(str(self.text + "|"), True, self.fontColor).get_width() > self.width:
					self.cache += (self.text[0])
					self.text = self.text[1:]
	# Return the contents of the text field.
	def getContents(self):
		return str(self.cache + self.text)

# Class for adding raw text to a menu
class Text(Widget):
	def __init__(self, surface, window, text, color):
		self.surface = surface
		self.window = window
		self.text = text
		self.color = color
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = font.render("Example", True, pg.Color("Black")).get_height()

	# Check if the text is going off of the window
	def load(self):
		carry = None
		if font.render(self.text, True, self.color).get_width() > self.width:
			carry = ""
		while font.render(self.text, True, self.color).get_width() > self.width:
			carry = carry + self.text[-1]
			self.text = self.text[:-1]
		if carry:
			self.window.addText(carry, self.color)
		self.text = font.render(self.text, True, self.color)
	def draw(self):
		self.surface.blit(self.text, (self.x, self.y))



# Menu for the hovering text over a button
class Hover:
	def __init__(self, surface, text):
		self.surface = surface
		self.x = 0
		self.y = 0
		self.text = text
		self.image = font.render(self.text, True, pg.Color("Black"), pg.Color("White"))
	def draw(self):
		self.surface.blit(self.image, (self.x - 10, self.y + 10))

# Class for creating a custom menu. Unfinished
class Menu:
	def __init__(self,
	title,
	surface,
	color,
	titleColor,
	displayTitle = False,
	center=True,
	x=None,
	y=None,
	width=None,
	height=None):
		if x or y or width or height:
			if center:
				raise CustomError("Menu cannot be center and have custom dimensions")
		self.opened = False
		self.title = font.render(title, True, titleColor)
		self.surface = surface
		self.dimensions = (self.surface.get_width(), self.surface.get_height())
		self.color = color
		self.displayTitle = displayTitle
		if center:
			self.width = self.dimensions[0] // 2
			self.height = self.title.get_height()
			self.x = (self.dimensions[0] - self.width) // 2
			self.y = (self.dimensions[1] - self.height) // 2
		else:
			self.x = x
			self.y = y
			self.width = width
			self.height = height
		self.contents = []
		self.center = center
	# Set the windowe to open
	def open(self):
		self.opened = True
	# Set the window to closed
	def close(self):
		self.opened = False
	# Adds a button to the menu
	def addButton(self, name, image, command):
		if self.center:
			self.y -= image.get_height() // 2
			newButton = Button(name, self, image, command)
			newButton.width = image.get_width()
			newButton.height = image.get_height()

			newButton.x = (self.dimensions[0] - newButton.width) // 2
			newButton.y = (self.y + self.height)
			for content in self.contents:
				content.y -= image.get_height() // 2
			self.height += image.get_height()
			self.contents.append(newButton)
		else:
			newButton = Button(name, self, image, command)
			self.contents.append(newButton)
			newButton.y = self.y
			newButton.x = self.height * self.contents.index(newButton)
			newButton.width = image.get_width()
			newButton.height = image.get_height()
		return newButton
	# Adds a text entry to the menu
	def addEntry(self, fontColor, backgroundColor):
		newEntry = Entry(self.surface, self, fontColor, backgroundColor)
		if self.center:
			self.y -= newEntry.height // 2
			for content in self.contents:
				content.y -= newEntry.height // 2
			newEntry.x = self.x + 10
			newEntry.width = self.width - 20
			newEntry.y = self.y + self.height

			self.height += newEntry.height
			self.contents.append(newEntry)
		return newEntry
	# Adds raw text to the menu
	def addText(self, text, color):
		newText = Text(self.surface, self, text, color)
		if self.center:
			self.y -= newText.height // 2
			for content in self.contents:
				content.y -= newText.height // 2
			newText.x = self.x + 10
			newText.width = self.width - 20
			newText.y = self.y + self.height
			self.height += newText.height
			self.contents.append(newText)
			newText.load()
		return newText
	# Draw the menu and all of its contents
	def draw(self):
		if self.opened:
			pg.draw.rect(
				self.surface,
				self.color,
				(
				self.x,
				self.y,
				self.width,
				self.height
					)
				)
			if self.displayTitle:
				self.surface.blit(self.title, (self.x, self.y))
			for content in self.contents:
				content.draw()