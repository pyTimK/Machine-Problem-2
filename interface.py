import pyglet
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

	def draw(self):
		pyglet.image.SolidColorImagePattern(self.color).create_image(self.box_width, self.box_height).blit(self.posx, self.posy)


bg_white = Background(0,0,width,height)
bg_gray = Background(0,0,width,height,(233,233,233,255))

#Load All Bongo Cats
bongo_ai = Image('bongo_ai.png')



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
def set_ship_screen(chosen_hero, human_board, human_carrier, human_battleship, human_cruiser, human_submarine, human_destroyer):
	bg_gray.draw()
	
	chosen_hero.draw(0,height-chosen_hero.image.height)
	human_board.image.blit(50,5)
	Text('Place your Ships!', 500, 300).draw()
	human_carrier.draw()
	human_battleship.draw()
	human_cruiser.draw()
	human_submarine.draw()
	human_destroyer.draw()




#Game Screen
def game_screen(chosen_hero,human_board,ai_board):
	bg_gray.draw()
	
	chosen_hero.draw(0,height-chosen_hero.image.height)
	human_board.image.blit(50,5)

	bongo_ai.image.blit(width-bongo_ai.image.width,height-chosen_hero.image.height)
	ai_board.image.blit(width-(ai_board.image.width+50),5)

