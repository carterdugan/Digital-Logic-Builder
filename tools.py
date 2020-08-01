import pygame as pg

nodeRadius = 4
wireColor = pg.Color("Purple")
takenNodeColor = pg.Color("Red")
outputNodeColor = pg.Color("Blue")


# Tick speeds of timer
timerOnTick = 600

# Get a point on the grid
def getPoint(position, grid, margin):
	for node in grid:
		if (
			position[0] >= node.x - node.r - margin
			and position[0] <= node.x + node.r + margin
			and position[1] >= node.y - node.r - margin
			and position[1] <= node.y + node.r + margin
		):
			return node
		else:
			continue

# Class for nodes with deal with placing
# and exchanging power between components.
class Node:
	def __init__(self, x, y):
		self.x = x + nodeRadius
		self.y = y + nodeRadius
		self.r = nodeRadius
		self.isCharged = False
	def draw(self, window, color):
		pg.draw.circle(
			window, 
			color, 
			(self.x, self.y), 
			self.r
			)

# The super class that deals with default returns
# and the drawing function that applies to all
# sub classes
class Component:
	def draw(self, surface):
		surface.blit(self.image, (self.x, self.y))
		for node in self.nodes:
			node.draw(surface, takenNodeColor)
	def checkClick(self):
		pass

# The gate super class. This
# is currently unused.
class Gate:
	def __init__(self):
		pass

# The wire class. Subclass of component,
# though for no real reason. Handles the
# placing of a wire.
class Wire(Component):
	def __init__(self, node):
		self.w = 8
		self.color = wireColor
		self.inputNode = node
		self.outputNode = node
		self.nodes = [self.inputNode, self.outputNode]
	def update(self, node):
		self.outputNode = node
		self.nodes = [self.inputNode, self.outputNode]
	def draw(self, window):
		pg.draw.line(
			window,
			self.color,
			(self.inputNode.x, self.inputNode.y),
			(self.outputNode.x, self.outputNode.y),
			self.w
			)
		self.inputNode.draw(window, takenNodeColor)
		self.outputNode.draw(window, outputNodeColor)
	def function(self):
		if self.inputNode.isCharged:
			self.outputNode.isCharged = True
		else:
			self.outputNode.isCharged = False


# The switch class. Overrides the component
# checkClick function and is the only sub
# class to do so.
class Switch(Component):
	def __init__(self, node, onImage, offImage):
		self.isCharged = False
		self.outputNode = node
		self.onImage = onImage
		self.offImage = offImage
		self.image = self.offImage
	def update(self, pos, grid, margin):
		self.outputNode = getPoint(pos, grid, margin)
		self.x = self.outputNode.x - (self.image.get_width() // 2)
		self.y = self.outputNode.y
		self.nodes = [self.outputNode]
	def function(self):
		if self.isCharged:
			self.image = self.onImage
			self.outputNode.isCharged = True
		else:
			self.image = self.offImage
			self.outputNode.isCharged = False
	def checkClick(self):
		x, y = pg.mouse.get_pos()
		if (
			x > self.x
			and x < self.x + self.image.get_width()
			and y > self.y
			and y < self.y + self.image.get_height()
			):
			if self.isCharged:
				self.isCharged = False
			else:
				self.isCharged = True

# The LED Class. Lights up when
# powered.
class LED(Component):
	def __init__(self, node, onImage, offImage):
		self.inputNode = node
		self.onImage = onImage
		self.offImage = offImage
		self.image = offImage
	def update(self, pos, grid, margin):
		self.inputNode = getPoint(pos, grid, margin)
		self.x = self.inputNode.x - (self.image.get_width() // 2)
		self.y = self.inputNode.y - self.image.get_height()
		self.nodes = [self.inputNode]
	def function(self):
		if self.inputNode.isCharged:
			self.image = self.onImage
		else:
			self.image = self.offImage

# The timer class. The amount of ticks
# can be changed at the top of this file
class Timer(Component):
	def __init__(self, node, images, grid, margin):
		self.images = images
		self.image = self.images[0]
		self.inputNode = node
		self.last = pg.time.get_ticks()
	def update(self, pos, grid, margin):
		self.inputNode = getPoint(pos, grid, margin)
		self.outputNode = getPoint((self.inputNode.x, (self.inputNode.y - self.image.get_height())), grid, margin)
		self.x = self.inputNode.x - (self.image.get_width() // 2)
		self.y = self.inputNode.y - self.image.get_height()
		self.nodes = [self.inputNode, self.outputNode]
	def function(self):
		now = pg.time.get_ticks()
		if self.inputNode.isCharged:
			if (now - self.last >= timerOnTick * (1/3)
				and now - self.last < timerOnTick * (2/3)):
				self.image = self.images[1]

			elif (now - self.last >= timerOnTick * (2/3)
				and now - self.last < timerOnTick):
				self.image = self.images[2]


			elif (now - self.last >= timerOnTick
				and now - self.last < timerOnTick * (4/3)):
				self.image = self.images[3]
				

			elif (now - self.last >= timerOnTick * (4/3)
				and now - self.last < timerOnTick * (5/3)):
				self.image = self.images[4]

			elif (now - self.last >= timerOnTick * (5/3)
				and now - self.last < timerOnTick * 2):
				self.image = self.images[5]

			else:
				self.image = self.images[0]

		if now - self.last >= timerOnTick:
			if self.inputNode.isCharged:
				self.outputNode.isCharged = True
		if now - self.last >= timerOnTick * 2:
			self.last = now
			self.outputNode.isCharged = False

# The seven segment display.
class SevenSegment(Component):
	def __init__(self, node, images, grid, margin):
		self.images = images
		self.image = self.images[0]
		self.a = node
	def update(self, pos, grid, margin):
		self.a = getPoint((pos[0], pos[1]), grid, margin)
		self.b = getPoint((self.a.x, self.a.y + (margin * 5)), grid, margin)
		self.c = getPoint((self.a.x, self.b.y + (margin * 5)), grid, margin)
		self.d = getPoint((self.a.x, self.c.y + (margin * 5)), grid, margin)
		self.e = getPoint((self.a.x, self.d.y + (margin * 5)), grid, margin)
		self.f = getPoint((self.a.x, self.e.y + (margin * 5)), grid, margin)
		self.g = getPoint((self.a.x, self.f.y + (margin * 5)), grid, margin)
		self.x = self.a.x
		self.y = self.a.y
		self.nodes = [self.a, self.b, self.c, self.d, self.e, self.f, self.g]
	def draw(self, surface):
		pg.draw.rect(surface, (150, 150, 150), (self.x, self.y, self.images[0].get_width(), self.images[0].get_height()))
		surface.blit(self.images[0], (self.x, self.y))
		if self.a.isCharged:
			surface.blit(self.images[1], (self.x, self.y))
		if self.b.isCharged:
			surface.blit(self.images[2], (self.x, self.y))
		if self.c.isCharged:
			surface.blit(self.images[3], (self.x, self.y))
		if self.d.isCharged:
			surface.blit(self.images[4], (self.x, self.y))
		if self.e.isCharged:
			surface.blit(self.images[5], (self.x, self.y))
		if self.f.isCharged:
			surface.blit(self.images[6], (self.x, self.y))
		if self.g.isCharged:
			surface.blit(self.images[7], (self.x, self.y))
		for node in self.nodes:
			node.draw(surface, takenNodeColor)
	def function(self):
		pass

# The or gate. Powered if one
# or both inputs are powered
class OrGate(Component, Gate):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.inputNode1 = node
	def update(self, pos, grid, margin):
		self.inputNode1 = getPoint(pos, grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 8, self.inputNode1.y), grid, margin)
		self.outputNode = getPoint((self.inputNode1.x + margin * 4, (self.inputNode1.y - margin * 8)), grid, margin)
		self.x = self.inputNode1.x
		self.y = self.inputNode1.y - self.image.get_height()
		self.nodes = [self.inputNode1, self.inputNode2, self.outputNode]
	def function(self):
		if self.inputNode1.isCharged or self.inputNode2.isCharged:
			self.outputNode.isCharged = True
		else:
			self.outputNode.isCharged = False

# The and gate. Powered if both
# inputs are powered.
class AndGate(Component, Gate):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.inputNode1 = node
	def update(self, pos, grid, margin):
		self.inputNode1 = getPoint(pos, grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 8, self.inputNode1.y), grid, margin)
		self.outputNode = getPoint((self.inputNode1.x + margin * 4, (self.inputNode1.y - margin * 8)), grid, margin)
		self.x = self.inputNode1.x
		self.y = self.inputNode1.y - self.image.get_height()
		self.nodes = [self.inputNode1, self.inputNode2, self.outputNode]
	def function(self):
		if self.inputNode1.isCharged and self.inputNode2.isCharged:
			self.outputNode.isCharged = True
		else:
			self.outputNode.isCharged = False

# The nor gate. Powered if both
# inputs are unpowered.
class NorGate(Component, Gate):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.inputNode1 = node
	def update(self, pos, grid, margin):
		self.inputNode1 = getPoint(pos, grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 8, self.inputNode1.y), grid, margin)
		self.outputNode = getPoint((self.inputNode1.x + margin * 4, (self.inputNode1.y - margin * 8)), grid, margin)
		self.x = self.inputNode1.x
		self.y = self.inputNode1.y - self.image.get_height()
		self.nodes = [self.inputNode1, self.inputNode2, self.outputNode]
	def function(self):
		if not self.inputNode1.isCharged and not self.inputNode2.isCharged:
			self.outputNode.isCharged = True
		else:
			self.outputNode.isCharged = False

# The nand gate. Powered unless
# both inputs are powered or
# unpowered
class NandGate(Component, Gate):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.inputNode1 = node
	def update(self, pos, grid, margin):
		self.inputNode1 = getPoint(pos, grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 8, self.inputNode1.y), grid, margin)
		self.outputNode = getPoint((self.inputNode1.x + margin * 4, (self.inputNode1.y - margin * 8)), grid, margin)
		self.x = self.inputNode1.x
		self.y = self.inputNode1.y - self.image.get_height()
		self.nodes = [self.inputNode1, self.inputNode2, self.outputNode]
	def function(self):
		if self.inputNode1.isCharged and self.inputNode2.isCharged:
			self.outputNode.isCharged = False
		else:
			self.outputNode.isCharged = True
# The xor gate. Only powered
# if one of the inputs are
# powered
class XorGate(Component, Gate):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.inputNode1 = node
	def update(self, pos, grid, margin):
		self.inputNode1 = getPoint(pos, grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 8, self.inputNode1.y), grid, margin)
		self.outputNode = getPoint((self.inputNode1.x + margin * 4, (self.inputNode1.y - margin * 8)), grid, margin)
		self.x = self.inputNode1.x
		self.y = self.inputNode1.y - self.image.get_height()
		self.nodes = [self.inputNode1, self.inputNode2, self.outputNode]
	def function(self):
		if self.inputNode1.isCharged and not self.inputNode2.isCharged:
			self.outputNode.isCharged = True
		elif not self.inputNode1.isCharged and self.inputNode2.isCharged:
			self.outputNode.isCharged = True
		else:
			self.outputNode.isCharged = False

# The xnor gate. Powered
# unless one input is
# unpowered
class XnorGate(Component, Gate):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.inputNode1 = node
	def update(self, pos, grid, margin):
		self.inputNode1 = getPoint(pos, grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 8, self.inputNode1.y), grid, margin)
		self.outputNode = getPoint((self.inputNode1.x + margin * 4, (self.inputNode1.y - margin * 8)), grid, margin)
		self.x = self.inputNode1.x
		self.y = self.inputNode1.y - self.image.get_height()
		self.nodes = [self.inputNode1, self.inputNode2, self.outputNode]
	def function(self):
		if self.inputNode1.isCharged and self.inputNode2.isCharged:
			self.outputNode.isCharged = True
		elif not self.inputNode1.isCharged and not self.inputNode2.isCharged:
			self.outputNode.isCharged = True
		else:
			self.outputNode.isCharged = False

# The not gate. Always outputs the
# opposite of the input.
class NotGate(Component, Gate):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.inputNode = node
	def update(self, pos, grid, margin):
		self.inputNode = getPoint(pos, grid, margin)
		self.outputNode = getPoint((self.inputNode.x, (self.inputNode.y - margin * 8)), grid, margin)
		self.x = self.inputNode.x - self.image.get_width() // 2
		self.y = self.inputNode.y - self.image.get_height()
		self.nodes = [self.inputNode, self.outputNode]
	def function(self):
		if self.inputNode.isCharged:
			self.outputNode.isCharged = False
		else:
			self.outputNode.isCharged = True

# The half adder. Can add up to
# 2 in binary (10)
class HalfAdder(Component):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.outputNode1 = node
	def update(self, pos, grid, margin):
		self.outputNode1 = getPoint(pos, grid, margin)
		self.outputNode2 = getPoint((self.outputNode1.x + margin * 8, self.outputNode1.y), grid, margin)
		self.inputNode1 = getPoint((self.outputNode1.x, self.outputNode1.y + margin * 8), grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 8, self.inputNode1.y), grid, margin)
		self.x = self.outputNode1.x
		self.y = self.outputNode1.y
		self.nodes = [self.outputNode1, self.outputNode2, self.inputNode1, self.inputNode2]
	def function(self):
		if self.inputNode1.isCharged and self.inputNode2.isCharged:
			self.outputNode1.isCharged = True
			self.outputNode2.isCharged = False
		elif self.inputNode1.isCharged or self.inputNode2.isCharged:
			self.outputNode2.isCharged = True
			self.outputNode1.isCharged = False
		else:
			self.outputNode2.isCharged = False
			self.outputNode1.isCharged = False

# The full adder. Adds up to
# 3 in binary. (11)
class FullAdder(Component):
	def __init__(self, node, image, grid, margin):
		self.image = image
		self.outputNode1 = node
	def update(self, pos, grid, margin):
		self.outputNode1 = getPoint(pos, grid, margin)
		self.outputNode2 = getPoint((self.outputNode1.x + margin * 8, self.outputNode1.y), grid, margin)
		self.inputNode1 = getPoint((self.outputNode1.x, self.outputNode1.y + margin * 8), grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 4, self.inputNode1.y), grid, margin)
		self.inputNode3 = getPoint((self.inputNode1.x + margin * 8, self.inputNode1.y), grid, margin)
		self.x = self.outputNode1.x
		self.y = self.outputNode1.y
		self.nodes = [self.outputNode1, self.outputNode2, self.inputNode1, self.inputNode2, self.inputNode3]
	def function(self):
		total = 0
		for i in range(2, 5):
			if self.nodes[i].isCharged:
				total += 1

		if total == 3:
			self.outputNode1.isCharged = True
			self.outputNode2.isCharged = True
		elif total == 2:
			self.outputNode1.isCharged = True
			self.outputNode2.isCharged = False
		elif total == 1:
			self.outputNode2.isCharged = True
			self.outputNode1.isCharged = False
		else:
			self.outputNode1.isCharged = False
			self.outputNode2.isCharged = False

# The command block. A block that
# can currently be used to
# redirect/negate power from one
# node to another, and do so in a
# user-set time frame.
class CommandBlock(Component):
	def __init__(self, node, image, grid, margin, cmd):
		self.image = image
		self.outputNode1 = node
		self.cmds = cmd.split(";")
	def update(self, pos, grid, margin):
		self.outputNode1 = getPoint(pos, grid, margin)
		self.outputNode2 = getPoint((self.outputNode1.x + margin * 4, self.outputNode1.y), grid, margin)
		self.outputNode3 = getPoint((self.outputNode2.x + margin * 4, self.outputNode1.y), grid, margin)
		self.outputNode4 = getPoint((self.outputNode3.x + margin * 4, self.outputNode1.y), grid, margin)
		self.outputNode5 = getPoint((self.outputNode4.x + margin * 4, self.outputNode1.y), grid, margin)
		self.outputNode6 = getPoint((self.outputNode5.x + margin * 4, self.outputNode1.y), grid, margin)
		self.outputNode7 = getPoint((self.outputNode6.x + margin * 4, self.outputNode1.y), grid, margin)

		self.inputNode1 = getPoint((self.outputNode1.x, self.outputNode1.y + margin * 28), grid, margin)
		self.inputNode2 = getPoint((self.inputNode1.x + margin * 4, self.inputNode1.y), grid, margin)
		self.inputNode3 = getPoint((self.inputNode2.x + margin * 4, self.inputNode1.y), grid, margin)
		self.inputNode4 = getPoint((self.inputNode3.x + margin * 4, self.inputNode1.y), grid, margin)
		self.inputNode5 = getPoint((self.inputNode4.x + margin * 4, self.inputNode1.y), grid, margin)
		self.inputNode6 = getPoint((self.inputNode5.x + margin * 4, self.inputNode1.y), grid, margin)
		self.inputNode7 = getPoint((self.inputNode6.x + margin * 4, self.inputNode1.y), grid, margin)
		self.x = self.outputNode1.x
		self.y = self.outputNode1.y
		self.nodes = [
		self.outputNode1,
		self.outputNode2,
		self.outputNode3,
		self.outputNode4,
		self.outputNode5,
		self.outputNode6,
		self.outputNode7,
		self.inputNode1,
		self.inputNode2,
		self.inputNode3,
		self.inputNode4,
		self.inputNode5,
		self.inputNode6,
		self.inputNode7
		]
		self.commands = []
		try:
			for command in self.cmds:
				if command:
					if "@" in command:
						ticks = int(command.split("@")[1])
						command = command.split("@")[0]
					else:
						ticks = 0
					ins = []
					outs = []
					if "=" in command:
						inputs = command.split("=")[0].split("&")
						outputs = command.split("=")[1].split("&")
						boo = True
					elif "!" in command:
						inputs = command.split("!")[0].split("&")
						outputs = command.split("!")[1].split("&")
						boo = False
					for i in inputs:
						ins.append(getattr(self, i))
					for j in outputs:
						outs.append(getattr(self, j))
					self.commands.append(Command(ins, outs, boo, ticks))
				else:
					pass
		except:
			print("Exception")
	def function(self):
		for command in self.commands:
			command.function()

# The command class that handle the
# commands given to the command block
class Command:
	def __init__(self, inputs, outputs, boo, ticks):
		self.inputs = inputs
		self.outputs = outputs
		self.boo = boo
		self.ticks = ticks
		self.last = pg.time.get_ticks()
	def function(self):
		now = pg.time.get_ticks()
		ins = []
		for i in self.inputs:
			ins.append(getattr(i, "isCharged"))
		if all(ins):
			if self.ticks > 0:
				if now - self.last >= self.ticks:
					for j in self.outputs:
						j.isCharged = self.boo
				if now - self.last >= self.ticks * 2:
					for j in self.outputs:
						j.isCharged = not j.isCharged
					self.last = now
			else:
				for j in self.outputs:
					j.isCharged = self.boo
		else:
			for j in self.outputs:
				j.isCharged = not self.boo