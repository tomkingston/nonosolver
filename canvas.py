import pprint		# just to print dictionaries nicely
import readline		# history of commands etc

class Canvas(object):
	bitmap = [[]]			# 2 dimensional array (list within a list) to store image
	blank_pixel = None
	def __init__(self, width=0, height=0, blank_pixel = None):
		self.blank_pixel = blank_pixel if blank_pixel else self.blank_pixel
		self.initialise_grid(width, height)
	
	def initialise_grid(self, m, n):
		self.bitmap = [[self.blank_pixel] * n for y in range(m)]
	
	def clear(self):
		height = len(self.bitmap)
		width = len(self.bitmap[0])
		self.bitmap = [[self.blank_pixel] * width for y in range(height)]
		
	def colour_pixel(self, x, y, c):
		self.bitmap[x][y] = c
	
	def get_row(self, row_index):
		row = []
		for col, value in enumerate(self.bitmap):
			 row.append(self.bitmap[col][row_index])
		return row
	
	def get_col(self, col_index):
		return self.bitmap[col_index]
		
	def vertical_segment(self, x, y1, y2, c):
		if y1 > y2:
			y1, y2 = y2, y1 			# ensure that we start with smallest number
		for y in range(y1, y2 + 1):
			self.colour_pixel(x, y, c)
	
	def horizontal_segment(self, x1, x2, y, c):
		if x1 > x2:
			x1, x2 = x2, x1 			# ensure that we start with smallest number
		for x in range(x1, x2 + 1):
			self.colour_pixel(x, y, c)
	
	def fill_region(self, x, y, c):
		target_colour = self.bitmap[x][y]
		if c != target_colour:
			self._fill_region(x, y, c, target_colour)
		
	def _fill_region(self, x, y, c, target_colour):
		# use recursion to colour pixels
		if self.bitmap[x][y] == target_colour:
			self.colour_pixel(x, y, c)				# colour this pixel
			if x > 0:
				self._fill_region(x - 1, y, c, target_colour)		# check left
			if x < len(self.bitmap) - 1:
				self._fill_region(x + 1, y, c, target_colour)		# check right
			if y > 0:
				self._fill_region(x, y - 1, c, target_colour)		# check above
			if y < len(self.bitmap[x]) - 1:
				self._fill_region(x, y +1, c, target_colour)		# check below
	
	def show(self):
		height = len(self.bitmap[0])
		width = len(self.bitmap)
		output = ''
		for y in range(height):
			for x in range(width):
				output += str(self.bitmap[x][y])
			output += "\n"
		return output
	
	def transform(self):
		height = len(self.bitmap[0])
		width = len(self.bitmap)
		output = [[None] * height for y in range(width)]	# initialise blank grid
		for y in range(height):
			for x in range(width):
				output[y][x] = self.bitmap[x][y]
		return output