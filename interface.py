import pyglet, engine

width = 1200
height = 600

class Image:
	def __init__(self, image, batch=None):
		self.image = pyglet.image.load('res/sprites/'+image)


class Text:
	def __init__(self, text,xpos,ypos,color=(0,0,0,255),anchor_x='left', anchor_y='bottom',font_size=25,batch=None ):
		self.text=text
		self.xpos=xpos
		self.ypos=ypos
		self.color=color
		self.font_size=font_size
		self.batch=batch
		self.anchor_x=anchor_x
		self.anchor_y=anchor_y

	def draw(self):
		pyglet.text.Label(self.text,
	                      font_size=self.font_size,
	                      x=self.xpos, y=self.ypos, anchor_x=self.anchor_x, anchor_y=self.anchor_y,
	        	          color=self.color, batch=self.batch).draw()



class Background:
	def __init__(self, posx, posy, box_width, box_height,color=(255,255,255,255)):
		self.posx=posx
		self.posy=posy
		self.box_width=box_width
		self.box_height=box_height
		self.color=color
		self.image = pyglet.image.SolidColorImagePattern(self.color).create_image(self.box_width, self.box_height)

	def draw(self):
		self.image.blit(self.posx, self.posy)





bg_white = Background(0,0,width,height)
bg_gray = Background(0,0,width,height,(233,233,233,255))
must_shade = False
ship_shade = Background(0, 0, 0, 0, color=(255,255,255,10))
#Load All Bongo Cats
bongo_ai = Image('bongo_ai.png')
hit_img = pyglet.image.load('res/sprites/attack_texture.png')
success_hit_img = pyglet.image.load('res/sprites/success_hit.png')


#Home Screen
welcome_text = Text('Ito ang Home Screen', width//2, height-150, anchor_x='center')
click_anywhere_text = Text('Click Anywhere To Continue', width//2, 100, anchor_x='center')


def home_screen():
	bg_white.draw()
	welcome_text.draw()
	click_anywhere_text.draw()

#Choose Player Screen
def draw_all_cats(bongo_cats, show_name):
	n=len(bongo_cats)
	start_x = (4*(width-1000))//11 #dynamically starts the x position of the bongo images
	margin_right = start_x//4
	for i in range(n):
		if i<4:
			bongo_cats[i].draw(start_x+i*(bongo_cats[i].image.width+margin_right),212)
		elif 4<=i<=8:
			bongo_cats[i].draw(start_x+(i-4)*(bongo_cats[i].image.width+margin_right),12)

		if bongo_cats[i] == show_name:
			pyglet.text.Label(bongo_cats[i].name, font_size=20, x=bongo_cats[i].x+bongo_cats[i].image.width//2, y=bongo_cats[i].y+25, anchor_x='center', anchor_y='center', color=(0,0,0,255)).draw()
		

start_bg = Background(width-320, 25, 300, 150)
start_text = Text('START', start_bg.posx+start_bg.box_width//2,start_bg.posy+start_bg.box_height//2,anchor_x='center',anchor_y='center')



def choose_player_screen(bongo_cats, show_name, player_name,chosen_hero):
	bg_gray.draw()
	draw_all_cats(bongo_cats, show_name)
	Text(player_name.upper(),width//2,height-70, anchor_x='center').draw()
	if chosen_hero != None:
		pyglet.text.Label(chosen_hero.name, font_size=20, x=chosen_hero.x+chosen_hero.image.width//2, y=chosen_hero.y+25, anchor_x='center', anchor_y='center', color=(0,0,0,255)).draw()
		start_bg.draw()
		start_text.draw()

	else:
		Text('Chose Your Hero', width//2, height-150, anchor_x='center').draw()


#Set Ship Screen
def set_shade(human_board, image_being_dragged, orientation):
	size = image_being_dragged.size
	x = (image_being_dragged.x-human_board.x)//40
	y = (image_being_dragged.y-human_board.y)//40

	ship_shade.posx = human_board.x+x*40
	ship_shade.posy = human_board.y+y*40

	ship_shade.box_width = image_being_dragged.image.width
	ship_shade.box_height = image_being_dragged.image.height

	if ship_shade.posy<human_board.y:
		ship_shade.posy=human_board.y
	elif ship_shade.posy+ship_shade.box_height>human_board.y+human_board.image.height:
		ship_shade.posy=human_board.y+human_board.image.height-ship_shade.box_height

	if ship_shade.posx<human_board.x:
		ship_shade.posx=human_board.x
	elif ship_shade.posx+ship_shade.box_width>human_board.x+human_board.image.width:
		ship_shade.posx=human_board.x+human_board.image.width-ship_shade.box_width

	#ship_shade.draw()
	if ship_shade.color==(255,255,255,100):
		bg_whitebox = pyglet.image.load('res/sprites/bg_whitebox.png')
	else:
		bg_whitebox = pyglet.image.load('res/sprites/bg_graybox.png')

	bg_whitebox.width=ship_shade.box_width
	bg_whitebox.height=ship_shade.box_height
	bg_whitebox.blit(ship_shade.posx,ship_shade.posy)

def set_ship_screen(chosen_hero, human_board, image_being_dragged, human_ship_list):
	bg_gray.draw()
	
	chosen_hero.draw(0,height-chosen_hero.image.height)
	human_board.texture.blit(human_board.x,human_board.y)

	Text('Place your Ships!', 650, 350, anchor_x='center').draw()
	Text('Right Click to Rotate', 650, 320, anchor_x='center', font_size=13).draw()
	if must_shade and image_being_dragged!=None:
		set_shade(human_board, image_being_dragged, image_being_dragged.orientation)
		engine.orientation=image_being_dragged.orientation

		x=(ship_shade.posx - human_board.x)//40
		y=(human_board.image.height+human_board.x - (ship_shade.posy + ship_shade.box_height))//40-1
		if engine.orientation == 'vertical':
		    base, fixed = y,x
		elif engine.orientation == 'horizontal':
		    fixed, base = y,x

		if engine.shipcheck(base, fixed, image_being_dragged.size, human_board.grid, human_board.occupied_positions):
			ship_shade.color=(255,255,255,100)
		else:
			ship_shade.color=(100,100,100,100)


	for human_ship in human_ship_list:
		human_ship.draw()

	
	if len(human_board.occupied_positions)==17:
		start_bg.draw()
		start_text.draw()



#Game Screen
white_texture = pyglet.image.Texture.create(width,height)
white_texture.blit_into(bg_gray.image,0,0,0)

def game_screen(player, chosen_hero,human_board,ai_board, human_ship_list, ai_ship_list, game, game_over):
	bg_gray.draw()
	
	chosen_hero.draw(0,height-chosen_hero.image.height)
	human_board.texture.blit(human_board.x,human_board.y)

	bongo_ai.image.blit(width-bongo_ai.image.width,height-chosen_hero.image.height)
	ai_board.texture.blit(ai_board.x,ai_board.y)

	Text(player.name,chosen_hero.image.width+20, height-100).draw()
	Text('vs',width//2, height-100, anchor_x='center').draw()
	Text('SKYNET',width-bongo_ai.image.width-20, height-100, anchor_x='right').draw()

	for human_ship in human_ship_list:
		human_board.texture.blit_into(human_ship.image, human_ship.x - human_board.x, human_ship.y - human_board.y, 1)


	if game_over:
		if game.turn=='player':
			Text('You Win!',width//2,height-200,anchor_x='center').draw()
		else:
			Text('Try Harder!',width//2,height-200,anchor_x='center').draw()

		for ai_ship in ai_ship_list:
			ai_board.texture.blit_into(ai_ship.image, ai_ship.x - ai_board.x, ai_ship.y - ai_board.y, 1)

	for coordinate in ai_board.attack_positions:
		x,y = coordinate
		if coordinate in ai_board.occupied_positions:
			ai_board.texture.blit_into(success_hit_img,x*40,(9-y)*40,2)
		else:
			ai_board.texture.blit_into(hit_img,x*40,(9-y)*40,2)

	for coordinate in human_board.attack_positions:
		x,y = coordinate
		if coordinate in human_board.occupied_positions:
			human_board.texture.blit_into(success_hit_img,x*40,(9-y)*40,2)
		else:
			human_board.texture.blit_into(hit_img,x*40,(9-y)*40,2)

	
