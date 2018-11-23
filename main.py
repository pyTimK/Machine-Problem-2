import pyglet, interface, engine
from pyglet.window import mouse
from pyglet.window import key
from interface import Text
from GameObjects import Bongo
from GameObjects import Player
from GameObjects import Game
from GameObjects import Board
from GameObjects import GamePiece
width,height = interface.width,interface.height
window = pyglet.window.Window(width,height,"Battle Ship",resizable=False)


bongo_cats = [Bongo('bongo1.png','BONGO CAT'), Bongo('bongo2.png','SHERLOCK'), Bongo('bongo3.png','VALENTINE'), Bongo('bongo4.png','EDGAR'), Bongo('bongo5.png','JOSE RIZAL'), Bongo('bongo6.png','Douglas MacArthur'), Bongo('bongo7.png','THANOS')]
player = Player()
show_name=None
chosen_hero=None
image_being_dragged=None

human_board = Board('human',engine.grid())
ai_board = Board('ai',engine.grid())

#Load all Ships
human_carrier = GamePiece('carrier.png',5,600,20)
human_battleship = GamePiece('battleship.png',4,700,100)
human_cruiser = GamePiece('cruiser.png',3,800,90)
human_submarine = GamePiece('submarine.png',3,500,40)
human_destroyer = GamePiece('destroyer.png',2,550,200)
ai_carrier = GamePiece('carrier.png',5)
ai_battleship = GamePiece('battleship.png',4)
ai_cruiser = GamePiece('cruiser.png',3)
ai_submarine = GamePiece('submarine.png',3)
ai_destroyer = GamePiece('destroyer.png',2)

human_ship_list=[human_carrier, human_battleship, human_cruiser, human_submarine, human_destroyer]

cursor_default = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
cursor_hand = window.get_system_mouse_cursor(window.CURSOR_HAND)

window.set_mouse_cursor(cursor_default)



def mouse_position_is_in(instance_name,x,y):
	if instance_name.x<=x<=instance_name.x+instance_name.image.width and instance_name.y<=y<=instance_name.y+instance_name.image.height:
		return True
	return False

@window.event
def on_mouse_motion(x, y, dx, dy):
	global show_name
	if player.state == 'choose_player_screen':
		for bongo_cat in bongo_cats:
			if mouse_position_is_in(bongo_cat,x,y):
				window.set_mouse_cursor(cursor_hand)
				show_name=bongo_cat
				break
			elif chosen_hero!=None and interface.start_bg.posx<=x<=interface.start_bg.posx+interface.start_bg.box_width and interface.start_bg.posy<=y<=interface.start_bg.posy+interface.start_bg.box_height:
				window.set_mouse_cursor(cursor_hand)
			else:
				show_name=None
				window.set_mouse_cursor(cursor_default)



	elif player.state == 'set_ship_screen':
		for human_ship in human_ship_list:
			if mouse_position_is_in(human_ship,x,y):
				window.set_mouse_cursor(cursor_hand)
				break
			else:
				window.set_mouse_cursor(cursor_default)




@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
	if player.state=='set_ship_screen':
		if button==mouse.LEFT:
			image_being_dragged.x=x-image_being_dragged.image.width//2
			image_being_dragged.y=y-image_being_dragged.image.height//2


@window.event
def on_mouse_press(x,y,button,modifier):
	global chosen_hero, mouse_dragging, image_being_dragged
	if button==mouse.LEFT:
		if player.state=='home_screen':
			player.state='choose_player_screen'
		elif player.state=='choose_player_screen':
			if show_name!=None:
					player.name = show_name.name			
					chosen_hero=show_name
			if chosen_hero!=None and interface.start_bg.posx<=x<=interface.start_bg.posx+interface.start_bg.box_width and interface.start_bg.posy<=y<=interface.start_bg.posy+interface.start_bg.box_height:
					player.state = 'set_ship_screen'

		elif player.state =='set_ship_screen':
			for human_ship in human_ship_list:
				if mouse_position_is_in(human_ship,x,y):
					image_being_dragged=human_ship

		

@window.event
def on_key_press(symbol, modifiers):
	if player.state=='home_screen':
		player.state='choose_player_screen'


	elif player.state =='choose_player_screen':
		if 97<=symbol<=122 and len(player.name)<=15:
			player.name+=chr(symbol)

		elif symbol==key.SPACE and 1<=len(player.name)<=15:
			player.name+=' '

		elif symbol==key.ENTER and 1<=len(player.name):
			player.state = 'set_ship_screen'



#keyboard events
@window.event
def on_text_motion(motion):
	if motion == key.MOTION_BACKSPACE and len(player.name)>0:
		player.name=player.name[:-1]


#default
@window.event
def on_draw():
	window.clear()

	if player.state=='home_screen':
		interface.home_screen()


	elif player.state=='choose_player_screen':
		interface.choose_player_screen(bongo_cats,show_name,player.name,chosen_hero)

	elif player.state=='set_ship_screen':
		interface.set_ship_screen(chosen_hero, human_board, human_carrier, human_battleship, human_cruiser, human_submarine, human_destroyer)

	elif player.state=='game_screen':
		interface.game_screen(chosen_hero,human_board,ai_board)
		

@window.event
def update(dt):
	pass


if __name__ == "__main__":
	pyglet.clock.schedule_interval(update, 1/60)
	pyglet.app.run()