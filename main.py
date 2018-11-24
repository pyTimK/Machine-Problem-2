import pyglet, interface, engine, time
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

game=Game('player')

bongo_cats = [Bongo('bongo1.png','BONGO CAT'), Bongo('bongo2.png','SHERLOCK'), Bongo('bongo3.png','VALENTINE'), Bongo('bongo4.png','EDGAR'), Bongo('bongo5.png','JOSE RIZAL'), Bongo('bongo6.png','Douglas MacArthur'), Bongo('bongo7.png','THANOS')]
player = Player()
show_name=None
chosen_hero=None
image_being_dragged=None
human_board = Board('human',engine.grid(),50,5)
ai_board = Board('ai',engine.grid())
ai_board.x, ai_board.y = width-(ai_board.image.width+50),5
game_over=False
#Load all Ships
human_carrier = GamePiece('carrier', 5, 600, 20)
human_battleship = GamePiece('battleship', 4, 700, 100)
human_cruiser = GamePiece('cruiser', 3, 800, 90)
human_submarine = GamePiece('submarine', 3, 500, 40)
human_destroyer = GamePiece('destroyer', 2, 550, 200)
ai_carrier = GamePiece('carrier', 5)
ai_battleship = GamePiece('battleship', 4)
ai_cruiser = GamePiece('cruiser', 3)
ai_submarine = GamePiece('submarine', 3)
ai_destroyer = GamePiece('destroyer', 2)

human_ship_list=[human_carrier, human_battleship, human_cruiser, human_submarine, human_destroyer]
ai_ship_list=[ai_carrier, ai_battleship, ai_cruiser, ai_submarine, ai_destroyer]

cursor_default = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
cursor_hand = window.get_system_mouse_cursor(window.CURSOR_HAND)

window.set_mouse_cursor(cursor_default)



def setting_ships_in_grid(setting,ship_object):
	engine.occupied = human_board.occupied_positions
	engine.orientation = ship_object.orientation
	x = (ship_object.x - human_board.x)//40
	y = (human_board.image.height+human_board.x - (ship_object.y + ship_object.image.height))//40-1

	if setting=='set':
		engine.shipset(human_board.grid, (x,y), engine.orientation, ship_object.name )
	else:
		engine.ship_unset(human_board.grid, (x,y), engine.orientation, ship_object.name )

	human_board.occupied_positions = engine.occupied
	


@window.event
def on_mouse_motion(x, y, dx, dy):
	global show_name
	if player.state == 'choose_player_screen':
		for bongo_cat in bongo_cats:
			if engine.mouse_position_is_in(bongo_cat,x,y):
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
			if engine.mouse_position_is_in(human_ship,x,y):
				window.set_mouse_cursor(cursor_hand)
				break

			elif len(human_board.occupied_positions)==17 and interface.start_bg.posx<=x<=interface.start_bg.posx+interface.start_bg.box_width and interface.start_bg.posy<=y<=interface.start_bg.posy+interface.start_bg.box_height:
				window.set_mouse_cursor(cursor_hand)
			else:
				window.set_mouse_cursor(cursor_default)


	elif player.state == 'game_screen':
		if engine.mouse_position_is_in(ai_board,x,y):
			window.set_mouse_cursor(cursor_hand)
		else:
			window.set_mouse_cursor(cursor_default)

@window.event
def on_mouse_release(x,y,button,modifier):
	global image_being_dragged
	if player.state == 'set_ship_screen':
		if image_being_dragged!=None:
			if interface.must_shade and interface.ship_shade.color==(255,255,255,100):
				image_being_dragged.x = interface.ship_shade.posx
				image_being_dragged.y = interface.ship_shade.posy

				setting_ships_in_grid('set',image_being_dragged)

			else:
				image_being_dragged.x = image_being_dragged.init_x
				image_being_dragged.y = image_being_dragged.init_y

		image_being_dragged=None

	interface.must_shade=False

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
	if player.state=='set_ship_screen':
		if button==mouse.LEFT and image_being_dragged!=None:
			image_being_dragged.x=x-image_being_dragged.image.width//2
			image_being_dragged.y=y-image_being_dragged.image.height//2

		if engine.mouse_position_is_in(human_board,x,y) and image_being_dragged!=None:
			interface.must_shade=True

		else:
			interface.must_shade=False



@window.event
def on_mouse_press(x,y,button,modifier):
	global chosen_hero, mouse_dragging, image_being_dragged, game_over
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
				if engine.mouse_position_is_in(human_ship,x,y):
					image_being_dragged=human_ship
			if image_being_dragged!=None and engine.mouse_position_is_in(human_board,x,y):
				setting_ships_in_grid('unset',image_being_dragged)


			if len(human_board.occupied_positions)==17 and interface.start_bg.posx<=x<=interface.start_bg.posx+interface.start_bg.box_width and interface.start_bg.posy<=y<=interface.start_bg.posy+interface.start_bg.box_height:
				player.state='game_screen'
				for i in range(len(human_board.occupied_positions)):
					x, y = human_board.occupied_positions[i]
					human_board.occupied_positions[i] = y, x

				window.set_mouse_cursor(cursor_default)
				engine.occupied = []
				engine.ai_set_ships(ai_board,ai_ship_list)
				for coordinate in engine.occupied:
					y, x = coordinate
					ai_board.occupied_positions.append((x,y))



		elif player.state == 'game_screen':

			if engine.mouse_position_is_in(ai_board,x,y):
				coordinate = ((x-ai_board.x)//40,9-(y-ai_board.y)//40)
				if coordinate not in ai_board.attack_positions:
					ai_board.attack_positions.append(coordinate)
					if coordinate in ai_board.occupied_positions:
						game.turn='player'
						if set(ai_board.occupied_positions).issubset(ai_board.attack_positions):
							game_over=True
					else:
						game.turn='ai'
					#Ai's Turn
					while game.turn=='ai':
						engine.previous = [4, (0, 0)]
						engine.player_ships = ['carrier', 'battleship', 'cruiser', 'submarine', 'destroyer']
						engine.occupied=[]
						for coordinate in human_board.occupied_positions:
							y, x =coordinate
							engine.occupied.append((x,y))
						engine.ai_hit(human_board, engine.occupied, engine.player_ships, engine.previous)
						if human_board.attack_positions[-1] not in human_board.occupied_positions:
							game.turn='player'
						elif set(human_board.occupied_positions).issubset(human_board.attack_positions):
							game_over=True
							break

				




	if button==mouse.RIGHT:
		if player.state =='set_ship_screen':
			for human_ship in human_ship_list:
				if engine.mouse_position_is_in(human_ship,x,y):

					if engine.mouse_position_is_in(human_board,x,y):
						setting_ships_in_grid('unset',human_ship)

					human_ship.switch_orientation()
					human_ship.x = x-human_ship.image.width//2
					human_ship.y = y-human_ship.image.height//2

					


		

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

	if symbol==key.R:
		if player.state=='set_ship_screen':
			engine.occupied = []
			human_board.occupied_positions=[]
			engine.ai_set_ships(human_board,human_ship_list)
			for coordinate in engine.occupied:
				y, x = coordinate
				human_board.occupied_positions.append((x,y))

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
		interface.set_ship_screen(chosen_hero, human_board, image_being_dragged, human_ship_list)

	elif player.state=='game_screen':
		interface.game_screen(player, chosen_hero,human_board,ai_board, human_ship_list, ai_ship_list, game, game_over)
		

@window.event
def update(dt):
	pass


if __name__ == "__main__":
	pyglet.clock.schedule_interval(update, 1/60)
	pyglet.app.run()