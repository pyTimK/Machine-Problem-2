import pyglet

class Bongo:
	show_name = False
	def __init__(self, image, name):
		self.image = pyglet.image.load('res/sprites/'+image)
		self.name = name
		self.sprite = pyglet.sprite.Sprite(self.image, x=0, y=0)


	def draw(self):
		self.sprite.draw()




class Player:
	def __init__(self):
		self.name = ''
		self.score = 0
		self.state = 'home_screen'

	def update(self):
		pass


class Game:
	def __init__(self, turn):
		self.turn=turn

class Board:
	def __init__(self,in_control,grid,x=0,y=0):
		self.texture = pyglet.image.Texture.create(400,400)
		self.image = pyglet.image.load('res/sprites/board.png')
		self.texture.blit_into(self.image,0,0,0)
		self.in_control = in_control
		self.grid = grid
		self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y)

		#occupied_positions and attack_positions are both lists of tuples
		self.occupied_positions = []
		self.attack_positions = []

	def draw(self):
		self.sprite.draw()	

class GamePiece:
	def __init__(self,name,size,x=0,y=0):
		self.image = pyglet.image.load('res/sprites/'+name+'.png')
		self.image.anchor_x=self.image.width//2
		self.image.anchor_y=self.image.height//2
		self.name = name
		self.size = size
		self.orientation = 'horizontal'
		self.coordinates=[]
		self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y)
	def switch_orientation(self):
		if self.orientation=='vertical':
			self.orientation='horizontal'
			self.sprite.rotation=0
		elif self.orientation=='horizontal':
			self.orientation='vertical'
			self.sprite.rotation=90


	def draw(self):
		self.sprite.draw()
