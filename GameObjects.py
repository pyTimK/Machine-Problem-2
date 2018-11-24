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
	def __init__(self, turn):
		self.turn=turn

class Board:
	def __init__(self,in_control,grid,x=0,y=0):
		self.texture = pyglet.image.Texture.create(400,400)
		self.image = pyglet.image.load('res/sprites/board.png')
		self.texture.blit_into(self.image,0,0,0)
		self.in_control = in_control
		self.grid = grid
		self.x=x
		self.y=y
		#occupied_positions and attack_positions are both lists of tuples
		self.occupied_positions = []
		self.attack_positions = []



	def draw(self):
		self.image.blit(self.x,self.y)	

class GamePiece:
	def __init__(self,name,size,init_x=0,init_y=0):
		self.image = pyglet.image.load('res/sprites/'+name+'_v.png')
		self.name = name
		self.size = size
		self.init_x=init_x
		self.init_y=init_y
		self.x=init_x
		self.y=init_y
		self.orientation = 'vertical'

	def switch_orientation(self):
		if self.orientation=='vertical':
			self.orientation='horizontal'
			self.image = pyglet.image.load('res/sprites/'+self.name+'_h.png')
		elif self.orientation=='horizontal':
			self.orientation='vertical'
			self.image = pyglet.image.load('res/sprites/'+self.name+'_v.png')

	def draw(self):
		self.image.blit(self.x,self.y)
