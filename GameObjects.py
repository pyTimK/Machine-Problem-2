import pyglet

class Bongo:
	show_name = False
	def __init__(self, image, name):
		self.image = pyglet.image.load('res/sprites/'+image)
		self.name = name
		self.x = 0
		self.y = 0



	def draw(self,posx,posy):
		self.x=posx
		self.y=posy
		self.image.blit(posx,posy)




class Player:
	def __init__(self):
		self.name = ''
		self.score = 0
		self.state = 'home_screen'

	def update(self):
		pass


class Game:
	def __init__(self, missing_word, num_of_tries):
		self.word = missing_word.lower()
		self.tries = num_of_tries
		self.letters = engine.generate_letters(self.word)

class Board:
		def __init__(self,in_control,grid):
			self.image = pyglet.image.load('res/sprites/board.png')
			self.in_control = in_control
			self.grid = grid

			#occupied_positions and attack_positions are both lists of tuples
			self.occupied_positions = []
			self.attack_positions = []


class GamePiece:
	def __init__(self,image,size,x=0,y=0):
		self.image = pyglet.image.load('res/sprites/'+image)
		self.size = size
		self.x=x
		self.y=y


	def draw(self):
		self.image.blit(self.x,self.y)
