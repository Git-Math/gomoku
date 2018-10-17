try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
import copy
import time

## todo
# Speed up a little at high depth
# bonus ?
# get entire move list first

# constants
DEBUG_MODE = True
LINE_NUMBER = 19	# do not change line number without changing center eval
SQUARE_SIZE = 37
GRID_SIZE = (LINE_NUMBER - 1) * SQUARE_SIZE
GRID_START = 50
GRID_END = GRID_START + GRID_SIZE
TEXT_SIZE = 16
TEXT_WIDTH = 100
TEXT_FONT = "Helvetica"
WINDOW_BACKGROUND_COLOR = "sienna4"
WINDOW_LINE_WIDTH = 4
WINDOW_LINE_COLOR = "black"
WINDOW_WIDTH = GRID_START + GRID_SIZE + 50 + TEXT_WIDTH + GRID_START
WINDOW_HEIGHT = GRID_START + GRID_SIZE + GRID_START 
TEXT_START = GRID_END + (WINDOW_WIDTH - GRID_END) / 2
PLAYER_1_COLOR = "black"
PLAYER_2_COLOR = "white"
PIECE_RADIUS = int(SQUARE_SIZE / 2.3)
MIN_VALUE = -1000000
MAX_VALUE = 1000000
PROXIMITY_MAX = 1
ILLEGAL_MOVE = 0
OK_MOVE = 1
GOOD_MOVE = 2
TOP_MOVE = 3
WIN_MOVE = 4


# function used for debug log
def debug_log(message):
	if DEBUG_MODE:
		print(message)


## ai functions
def fast_check_eat(grid, player, line, column, win_eat, is_continue):
	if fast_check_eat_direction(grid, player, line, column, 0, 1, win_eat, is_continue)		\
	or fast_check_eat_direction(grid, player, line, column, 1, 0, win_eat, is_continue)		\
	or fast_check_eat_direction(grid, player, line, column, 1, 1, win_eat, is_continue)		\
	or fast_check_eat_direction(grid, player, line, column, 0, -1, win_eat, is_continue)	\
	or fast_check_eat_direction(grid, player, line, column, -1, 0, win_eat, is_continue)	\
	or fast_check_eat_direction(grid, player, line, column, -1, -1, win_eat, is_continue)	\
	or fast_check_eat_direction(grid, player, line, column, 1, - 1, win_eat, is_continue)	\
	or fast_check_eat_direction(grid, player, line, column, -1, 1, win_eat, is_continue):
		return True
	return False

def fast_check_eat_direction(grid, player, line, column, direction_line, direction_column, win_eat, is_continue):
	line_plus_one = line + direction_line
	column_plus_one = column + direction_column
	line_plus_two = line_plus_one + direction_line
	column_plus_two = column_plus_one + direction_column
	line_plus_three = line_plus_two + direction_line
	column_plus_three = column_plus_two + direction_column
	
	if line_plus_three < 0										\
	or line_plus_three >= LINE_NUMBER							\
	or column_plus_three < 0									\
	or column_plus_three >= LINE_NUMBER:
		return False

	other_player = 2 if player == 1 else 1
	if grid[line_plus_one][column_plus_one] == other_player		\
	and grid[line_plus_two][column_plus_two] == other_player	\
	and grid[line_plus_three][column_plus_three] == player:
		return True

	if not win_eat and not is_continue							\
	and grid[line_plus_one][column_plus_one] == player			\
	and grid[line_plus_two][column_plus_two] == player			\
	and grid[line_plus_three][column_plus_three] == other_player:
		return True
	
	return False

def check_four(grid, line, column, player):
	top_move = False

	move_power = check_four_direction(grid, line, column, 0, 1, player)
	if move_power == WIN_MOVE:
		return WIN_MOVE
	elif move_power == TOP_MOVE:
		top_move = True
	
	move_power = check_four_direction(grid, line, column, 1, 0, player)
	if move_power == WIN_MOVE:
		return WIN_MOVE
	elif move_power == TOP_MOVE:
		top_move = True
	
	move_power = check_four_direction(grid, line, column, 1, 1, player)
	if move_power == WIN_MOVE:
		return WIN_MOVE
	elif move_power == TOP_MOVE:
		top_move = True
	
	move_power = check_four_direction(grid, line, column, -1, 1, player)
	if move_power == WIN_MOVE:
		return WIN_MOVE
	elif move_power == TOP_MOVE:
		top_move = True
	
	if top_move:
		return TOP_MOVE
	return 0
	 
def check_four_direction(grid, line, column, direction_line, direction_column, player):
	top_move = False
	other_player = 2 if player == 1 else 1

	empty_square = False
	max_alignment = 0
	current_line = line + direction_line
	current_column = column + direction_column
	while current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == player:
		max_alignment += 1
		current_line += direction_line
		current_column += direction_column
	if current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == 0:
		empty_square = True
	
	current_line = line - direction_line
	current_column = column - direction_column
	while current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == player:
		max_alignment += 1
		current_line -= direction_line
		current_column -= direction_column
	if current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == 0:
		empty_square = True
	
	if max_alignment == 4:
		return WIN_MOVE
	if max_alignment == 3 and empty_square:
		top_move = True

	empty_square = False
	max_alignment = 0
	current_line = line + direction_line
	current_column = column + direction_column
	while current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == other_player:
		max_alignment += 1
		current_line += direction_line
		current_column += direction_column
	if current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == 0:
		empty_square = True
	
	current_line = line - direction_line
	current_column = column - direction_column
	while current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == other_player:
		max_alignment += 1
		current_line -= direction_line
		current_column -= direction_column
	if current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == 0:
		empty_square = True

	if max_alignment == 4 or (max_alignment == 3 and empty_square):
		top_move = True
	if top_move:
		return TOP_MOVE
	return 0

def check_two(grid, line, column):
	if cheat_two_direction(grid, line, column, 0, 1):
		return True
	if cheat_two_direction(grid, line, column, 1, 0):
		return True
	if cheat_two_direction(grid, line, column, 1, 1):
		return True
	if cheat_two_direction(grid, line, column, -1, 1):
		return True
	return False

def cheat_two_direction(grid, line, column, direction_line, direction_column):
	line_plus_one = line + direction_line
	column_plus_one = column + direction_column
	line_plus_two = line_plus_one + direction_line
	column_plus_two = column_plus_one + direction_column
	line_minus_one = line - direction_line
	column_minus_one = column - direction_column
	line_minus_two = line_minus_one - direction_line
	column_minus_two = column_minus_one - direction_column

	if line_minus_two >= 0 and line_minus_two < LINE_NUMBER and column_minus_two >= 0 and column_minus_two < LINE_NUMBER and grid[line_minus_one][column_minus_one] != 0 and grid[line_minus_one][column_minus_one] == grid[line_minus_two][column_minus_two]		\
	or line_plus_two >= 0 and line_plus_two < LINE_NUMBER and column_plus_two >= 0 and column_plus_two < LINE_NUMBER and grid[line_plus_one][column_plus_one] != 0 and grid[line_plus_one][column_plus_one] == grid[line_plus_two][column_plus_two]					\
	or line_minus_one >= 0 and line_minus_one < LINE_NUMBER and column_minus_one >= 0 and column_minus_one < LINE_NUMBER and line_plus_one >= 0 and line_plus_one < LINE_NUMBER and column_plus_one >= 0 and column_plus_one < LINE_NUMBER and grid[line_minus_one][column_minus_one] != 0 and grid[line_minus_one][column_minus_one] == grid[line_plus_one][column_plus_one]:
		return True

	return False

def move_power(grid, line, column, player, win_eat, is_continue):
	if fast_check_eat(grid, player, line, column, win_eat, is_continue):
		if win_eat:
			return WIN_MOVE
		else:
			return TOP_MOVE
	if is_continue:
		return ILLEGAL_MOVE
	four = check_four(grid, line, column, player)
	if four != 0:
		return four
	if check_two(grid, line, column):
		return GOOD_MOVE
	return OK_MOVE

def get_move_list(grid, player, score, is_continue):
	move_list = []
	ok_move_list = []
	good_move_list = []
	top_move_list = []
	win_eat = True if score == 8 else False
		

	i = 0
	while i < LINE_NUMBER:
		j = 0
		while j < LINE_NUMBER:
			if grid[i][j] != 0:
				line = i - 1
				column = j - 1
				if line >= 0 and column >= 0 and line < LINE_NUMBER and column < LINE_NUMBER		\
				and grid[line][column] == 0															\
				and not check_double_three(grid, player, line, column):
					move_list.append((line, column))

				line = i - 1
				column = j
				if line >= 0 and column >= 0 and line < LINE_NUMBER and column < LINE_NUMBER		\
				and grid[line][column] == 0															\
				and not check_double_three(grid, player, line, column):
					move_list.append((line, column))
				
				line = i
				column = j - 1
				if line >= 0 and column >= 0 and line < LINE_NUMBER and column < LINE_NUMBER		\
				and grid[line][column] == 0															\
				and not check_double_three(grid, player, line, column):
					move_list.append((line, column))
					
				line = i - 1
				column = j + 1
				if line >= 0 and column >= 0 and line < LINE_NUMBER and column < LINE_NUMBER		\
				and grid[line][column] == 0															\
				and not check_double_three(grid, player, line, column):
					move_list.append((line, column))

				line = i + 1
				column = j - 1
				if line >= 0 and column >= 0 and line < LINE_NUMBER and column < LINE_NUMBER		\
				and grid[line][column] == 0															\
				and not check_double_three(grid, player, line, column):
					move_list.append((line, column))

				line = i + 1
				column = j + 1
				if line >= 0 and column >= 0 and line < LINE_NUMBER and column < LINE_NUMBER		\
				and grid[line][column] == 0															\
				and not check_double_three(grid, player, line, column):
					move_list.append((line, column))

				line = i + 1
				column = j
				if line >= 0 and column >= 0 and line < LINE_NUMBER and column < LINE_NUMBER		\
				and grid[line][column] == 0															\
				and not check_double_three(grid, player, line, column):
					move_list.append((line, column))

				line = i
				column = j + 1
				if line >= 0 and column >= 0 and line < LINE_NUMBER and column < LINE_NUMBER		\
				and grid[line][column] == 0															\
				and not check_double_three(grid, player, line, column):
					move_list.append((line, column))
			
			j += 1
		i += 1

	move_list = list(set(move_list))
	for move in move_list:
		line = move[0]
		column = move[1]
		power = move_power(grid, line, column, player, win_eat, is_continue)
		if power == OK_MOVE:
			ok_move_list.append((line, column))
		elif power == GOOD_MOVE:
			good_move_list.append((line, column))
		elif power == TOP_MOVE:
			top_move_list.append((line, column))
		elif power == WIN_MOVE:
			return [(line, column)]

	ret_move_list = top_move_list + good_move_list + ok_move_list
	return ret_move_list[:ai_move_number]


def ai(score, grid, player, is_continue, continue_line, continue_column, depth):
	alpha = MIN_VALUE - 1
	beta = MAX_VALUE + 1
	max_line = -1
	max_column = -1
	other_player = 2 if player == 1 else 1

	move_list = get_move_list(grid, player, score[player], is_continue)
	for move in move_list:
		line = move[0]
		column = move[1]
		move_success, eat = play_move(False, score, grid, player, line, column)
		if move_success:
			if score[player] >= 10:
				current_value = MAX_VALUE
			elif is_continue and check_alignment(grid, other_player, continue_line, continue_column):
				current_value = MIN_VALUE
			elif check_alignment(grid, player, line, column):
				current_value = ai_min(score, grid, player, True, line, column, depth - 1, alpha, beta)
			else:
				current_value = ai_min(score, grid, player, False, continue_line, continue_column, depth - 1, alpha, beta)
			if current_value >= alpha:
				alpha = current_value
				max_line = line
				max_column = column
			cancel_move(score, grid, player, line, column, eat)

	debug_log(alpha)
	return max_line, max_column

def ai_min(score, grid, player, is_continue, continue_line, continue_column, depth, alpha, beta):
	min_value = MAX_VALUE + 1
	other_player = 2 if player == 1 else 1

	if depth == 0:
		if is_continue:
			return MAX_VALUE / 2 - (ai_depth - depth)
		return heuristic(score, grid, player)

	move_list = get_move_list(grid, other_player, score[other_player], is_continue)
	for move in move_list:
		line = move[0]
		column = move[1]
		move_success, eat = play_move(False, score, grid, other_player, line, column)
		if move_success:
			if score[other_player] >= 10:
				current_value = MIN_VALUE + (ai_depth - depth)
			elif is_continue and check_alignment(grid, player, continue_line, continue_column):
				current_value = MAX_VALUE - (ai_depth - depth)
			elif check_alignment(grid, other_player, line, column):
				current_value = ai_max(score, grid, player, True, line, column, depth - 1, alpha, beta)
			else:
				current_value = ai_max(score, grid, player, False, continue_line, continue_column, depth - 1, alpha, beta)
			min_value = min(current_value, min_value)
			cancel_move(score, grid, other_player, line, column, eat)
			if alpha >= min_value:
				return min_value
			beta = min(min_value, beta)

	return min_value

def ai_max(score, grid, player, is_continue, continue_line, continue_column, depth, alpha, beta):
	max_value = MIN_VALUE - 1
	other_player = 2 if player == 1 else 1

	if depth == 0:
		if is_continue:
			return MIN_VALUE / 2 + (ai_depth - depth)
		return heuristic(score, grid, player)

	move_list = get_move_list(grid, player, score[player], is_continue)
	for move in move_list:
		line = move[0]
		column = move[1]
		move_success, eat = play_move(False, score, grid, player, line, column)
		if move_success:
			if score[player] >= 10:
				current_value = MAX_VALUE - (ai_depth - depth)
			elif is_continue and check_alignment(grid, other_player, continue_line, continue_column):
				current_value = MIN_VALUE + (ai_depth - depth)
			elif check_alignment(grid, player, line, column):
				current_value = ai_min(score, grid, player, True, line, column, depth - 1, alpha, beta)
			else:
				current_value = ai_min(score, grid, player, False, continue_line, continue_column, depth - 1, alpha, beta)
			max_value = max(current_value, max_value)
			cancel_move(score, grid, player, line, column, eat)
			if beta <= max_value:
				return max_value
			alpha = max(max_value, alpha)

	return max_value


def check_proximity(grid, line, column):
	if check_proximity_direction(grid, line, column, 0, 1):
		return True
	if check_proximity_direction(grid, line, column, 1, 0):
		return True
	if check_proximity_direction(grid, line, column, 1, 1):
		return True
	if check_proximity_direction(grid, line, column, 0, -1):
		return True
	if check_proximity_direction(grid, line, column, -1, 0):
		return True
	if check_proximity_direction(grid, line, column, -1, -1):
		return True
	if check_proximity_direction(grid, line, column, 1, - 1):
		return True
	if check_proximity_direction(grid, line, column, -1, 1):
		return True
	return False

def check_proximity_direction(grid, line, column, direction_line, direction_column):
	i = 1
	current_line = line + direction_line
	current_column = column + direction_column
	while i <= PROXIMITY_MAX										\
	and current_line >= 0											\
	and current_line < LINE_NUMBER                                  \
	and current_column >= 0											\
	and current_column < LINE_NUMBER:
		if grid[current_line][current_column] != 0:
			return True
		i += 1
		current_line += direction_line
		current_column += direction_column

	return False
		

def heuristic(score, grid, player):
	line = 0
	eval = 0
	w_score = 4096
	other_player = 2 if player == 1 else 1

	# wins are check in min/max functions

	# add square eval
	while line < LINE_NUMBER:
		column = 0
		while column < LINE_NUMBER:
			if grid[line][column] == player:
				eval += eval_square(grid, player, line, column)
			elif grid[line][column] == other_player:
				eval -= eval_square(grid, other_player, line, column)
			column += 1
		line += 1

	# add score eval
	eval += score[player] * w_score
	eval -= score[other_player] * w_score

	return eval

def eval_square(grid, player, line, column):
	eval = 0

	eval += eval_square_direction(grid, player, line, column, 0, 1)
	eval += eval_square_direction(grid, player, line, column, 1, 0)
	eval += eval_square_direction(grid, player, line, column, 1, 1)
	eval += eval_square_direction(grid, player, line, column, 1, - 1)

	return eval

def eval_square_direction(grid, player, line, column, direction_line, direction_column):
	square_number = 1
	player_square_number = 1
	w_center_eval = 1
	w_bonus_square = 2
	w_player_square_number = 8
	other_player = 2 if player == 1 else 1
	line_plus_one = line + direction_line
	column_plus_one = column + direction_column
	line_plus_two = line_plus_one + direction_line
	column_plus_two = column_plus_one + direction_column
	line_plus_three = line_plus_two + direction_line
	column_plus_three = column_plus_two + direction_column
	line_minus_one = line - direction_line
	column_minus_one = column - direction_column
	line_minus_two = line_minus_one - direction_line
	column_minus_two = column_minus_one - direction_column
	line_minus_three = line_minus_two - direction_line
	column_minus_three = column_minus_two - direction_column
	eval = 0
	
	# add possible eat eval
	if line_plus_three >= 0                                         \
	and line_plus_three < LINE_NUMBER                               \
	and column_plus_three >= 0										\
	and column_plus_three < LINE_NUMBER								\
	and	grid[line_plus_one][column_plus_one] == other_player		\
	and grid[line_plus_two][column_plus_two] == other_player		\
	and grid[line_plus_three][column_plus_three] == 0:
		eval += 4096

	if line_minus_three >= 0                                        \
	and line_minus_three < LINE_NUMBER                              \
	and column_minus_three >= 0										\
	and column_minus_three < LINE_NUMBER							\
	and	grid[line_minus_one][column_minus_one] == other_player		\
	and grid[line_minus_two][column_minus_two] == other_player		\
	and grid[line_minus_three][column_minus_three] == 0:
		eval += 4096

	# add center eval
	eval += ((10 - abs(10 - (line + 1))) + (10 - abs(10 - (column + 1)))) * w_center_eval

	i = -1
	current_line = line - direction_line
	current_column = column - direction_column
	while i > -5												\
	and current_line >= 0											\
	and current_line < LINE_NUMBER										\
	and current_column >= 0											\
	and current_column < LINE_NUMBER									\
	and grid[current_line][ current_column] != other_player:
		if grid[current_line][ current_column] == player:
			square_number += 1
			player_square_number += 1
		else:
			square_number += 1
		i -= 1
		current_line -= direction_line
		current_column -= direction_column

	i = 1
	current_line = line + direction_line
	current_column = column + direction_column
	while i < 5												\
	and current_line >= 0											\
	and current_line < LINE_NUMBER										\
	and current_column >= 0											\
	and current_column < LINE_NUMBER									\
	and grid[current_line][current_column] != other_player:
		if grid[current_line][current_column] == player:
			square_number += 1
			player_square_number += 1
		else:
			square_number += 1
		i += 1
		current_line += direction_line
		current_column += direction_column

	if square_number >= 5:
		bonus_square = square_number - 5
		eval += ((bonus_square + 1)  ** player_square_number) * w_bonus_square + (player_square_number ** player_square_number) * w_player_square_number

	return eval



## game functions
# function called on left click
def left_click(event):
	global game_window, player, score, grid, grid_canvas, is_game_finished, is_continue, continue_line, continue_column

	# check if the click was on a button
	current = game_canvas.gettags(event.widget.find_withtag("current"))

	if current != ():
		if current[0] == "restart":
			game_canvas.delete("all")
			print_game()
			return
		elif current[0] == "ai_level":
			game_canvas.delete("all")
			print_ai_level()
			return
		elif current[0] == "menu":
			game_canvas.delete("all")
			print_menu()
			return
		elif current[0] == "help":
			if is_game_finished:
				return
			
			# find help move
			line, column = ai(score, grid, player, is_continue, continue_line, continue_column, 4)
			if line == -1 and column == -1:
				if grid[9][9] == 0:
					line = 9
					column = 9
				else:
					debug_log("no move found")
					return
			
			# calc piece_center
			piece_center_x = column * SQUARE_SIZE + GRID_START
			piece_center_y = line * SQUARE_SIZE + GRID_START
			debug_log("piece_center_x " + str(piece_center_x) + " piece_center_y " + str(piece_center_y))
			
			# print piece
			help_piece = game_canvas.create_oval(piece_center_x - PIECE_RADIUS, piece_center_y - PIECE_RADIUS, piece_center_x + PIECE_RADIUS, piece_center_y + PIECE_RADIUS, fill = PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR)
		
			# update Canvas
			game_window.update()
		
			# wait
			time.sleep(1)
			
			# remove help piece
			game_canvas.delete(help_piece)
			return

	# check if the game is finished
	if is_game_finished or (player_number == 1 and ((ai_first and player == 1) or (not ai_first and player == 2))):
		return

	# get click position
	click_x = event.x
	click_y = event.y
	debug_log("click_x " + str(click_x) + " click_y " + str(click_y))

	# check if the click was out of the grid
	if click_x < GRID_START - PIECE_RADIUS or click_x > GRID_END + PIECE_RADIUS or click_y < GRID_START - PIECE_RADIUS or click_y > GRID_END + PIECE_RADIUS:
		debug_log("out of the grid")
		return

	## check if the click was on a piece
	# check click_x
	if (click_x - GRID_START) % SQUARE_SIZE <= PIECE_RADIUS or click_x < GRID_START:
		# calc column
		column = int ((click_x - GRID_START) / SQUARE_SIZE);
	elif (click_x - GRID_START) % SQUARE_SIZE >= SQUARE_SIZE - PIECE_RADIUS:
		# calc column
		column = int ((click_x - GRID_START) / SQUARE_SIZE) + 1;
	else:
		# click_x is not on a piece
		debug_log("click_x is not on a piece")
		return
	debug_log("column " + str(column))

	#print_grid(grid)

	# check clic_y
	if (click_y - GRID_START) % SQUARE_SIZE <= PIECE_RADIUS or click_y < GRID_START:
		# calc line
		line = int ((click_y - GRID_START) / SQUARE_SIZE);
	elif (click_y - GRID_START) % SQUARE_SIZE >= SQUARE_SIZE - PIECE_RADIUS:
		# calc line
		line = int ((click_y - GRID_START) / SQUARE_SIZE) + 1;
	else:
		# click_y is not on a piece
		debug_log("click_y is not on a piece")
		return
	debug_log("line " + str(line))

	# play the move
	move_success, eat = play_move(True, score, grid, player, line, column)
	if not move_success:
		return

	if is_continue:
		other_player = 2 if player == 1 else 1
		if check_alignment(grid, other_player, continue_line, continue_column):
			player_win(other_player)
		else:
			is_continue = False

	# check if player wins with alignment
	if check_alignment(grid, player, line, column):
		if not check_continue(score, grid, player, line, column):
			player_win(player)
		else:
			is_continue = True
			continue_line = line
			continue_column = column

	# calc piece_center
	piece_center_x = column * SQUARE_SIZE + GRID_START
	piece_center_y = line * SQUARE_SIZE + GRID_START
	debug_log("piece_center_x " + str(piece_center_x) + " piece_center_y " + str(piece_center_y))
	# print piece
	grid_canvas[line][column] = game_canvas.create_oval(piece_center_x - PIECE_RADIUS, piece_center_y - PIECE_RADIUS, piece_center_x + PIECE_RADIUS, piece_center_y + PIECE_RADIUS, fill = PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR)

	# change player for next move
	player = 2 if player == 1 else 1

	# if against ai, call ai
	if player_number == 1:
		# check if game is finish
		if is_game_finished:
			return
		
		# update Canvas
		game_window.update()

		# find ai move
		start_time = time.time()
		line, column = ai(score, grid, player, is_continue, continue_line, continue_column, ai_depth)
		end_time = time.time()
		game_canvas.itemconfigure(ai_timer, text = "AI timer:\n" + str(int((end_time - start_time) * 1000)) + "ms")
		if line == -1 and column == -1:
			debug_log("no move found")
			line = 0
			column = 0

		# play the move
		move_success, eat = play_move(True, score, grid, player, line, column)
		if not move_success:
			return

		if is_continue:
			other_player = 2 if player == 1 else 1
			if check_alignment(grid, other_player, continue_line, continue_column):
				player_win(other_player)
			else:
				is_continue = False

		# check if player wins with alignment
		if check_alignment(grid, player, line, column):
			if not check_continue(score, grid, player, line, column):
				player_win(player)
			else:
				is_continue = True
				continue_line = line
				continue_column = column

		# calc piece_center
		piece_center_x = column * SQUARE_SIZE + GRID_START
		piece_center_y = line * SQUARE_SIZE + GRID_START
		debug_log("piece_center_x " + str(piece_center_x) + " piece_center_y " + str(piece_center_y))
		# print piece
		grid_canvas[line][column] = game_canvas.create_oval(piece_center_x - PIECE_RADIUS, piece_center_y - PIECE_RADIUS, piece_center_x + PIECE_RADIUS, piece_center_y + PIECE_RADIUS, fill = PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR)

		# change player for next move
		player = 2 if player == 1 else 1

def player_win(player):
	global is_game_finished, is_continue

	if is_game_finished:
		return
	debug_log(str(PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR) + " win")
	game_canvas.create_text(TEXT_START, GRID_START + GRID_SIZE / 2, anchor = CENTER, font = (TEXT_FONT, TEXT_SIZE, "bold"), width = TEXT_WIDTH, text = str(PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR) + "\nwin !")
	is_game_finished = True
	is_continue = False

def play_move(update_canvas, score, grid, player, line, column):
	# check if the move can be played
	if line < 0 or column < 0 or line >= LINE_NUMBER or column >= LINE_NUMBER or grid[line][column] != 0:
		return False, 0

	# create piece
	grid[line][column] = player

	# check if the move eats something
	eat = check_eat(update_canvas, score, grid, player, line, column)
	if eat == 0:
		# if the move eats nothing, check if the move makes a double_three
		if check_double_three(grid, player, line, column):
			# cancel move
			grid[line][column] = 0
			# debug_log("double_three")
			return False, 0

	return True, eat

def cancel_move(score, grid, player, line, column, eat):
	grid[line][column] = 0
	cancel_eat(score, grid, player, line, column, eat)

def cancel_eat(score, grid, player, line, column, eat):
	# must be aligned with check_eat
	if eat & 1 == 1:
		cancel_eat_direction(score, grid, player, line, column, 0, 1)
	if (eat >> 1) & 1 == 1:
		cancel_eat_direction(score, grid, player, line, column, 1, 0)
	if (eat >> 2) & 1 == 1:
		cancel_eat_direction(score, grid, player, line, column, 1, 1)
	if (eat >> 3) & 1 == 1:
		cancel_eat_direction(score, grid, player, line, column, 0, -1)
	if (eat >> 4) & 1 == 1:
		cancel_eat_direction(score, grid, player, line, column, -1, 0)
	if (eat >> 5) & 1 == 1:
		cancel_eat_direction(score, grid, player, line, column, -1, -1)
	if (eat >> 6) & 1 == 1:
		cancel_eat_direction(score, grid, player, line, column, 1, -1)
	if (eat >> 7) & 1 == 1:
		cancel_eat_direction(score, grid, player, line, column, -1, 1)

def cancel_eat_direction(score, grid, player, line, column, direction_line, direction_column):
	other_player = 2 if player == 1 else 1
	score[player] -= 2
	grid[line + direction_line][column + direction_column] = other_player
	grid[line + 2 * direction_line][column + 2 * direction_column] = other_player
	
def check_eat(update_canvas, score, grid, player, line, column):
	eat = 0
	if check_eat_direction(update_canvas, score, grid, player, line, column, 0, 1):
		eat += 1
	if check_eat_direction(update_canvas, score, grid, player, line, column, 1, 0):
		eat += 1 << 1
	if check_eat_direction(update_canvas, score, grid, player, line, column, 1, 1):
		eat += 1 << 2
	if check_eat_direction(update_canvas, score, grid, player, line, column, 0, -1):
		eat += 1 << 3
	if check_eat_direction(update_canvas, score, grid, player, line, column, -1, 0):
		eat += 1 << 4
	if check_eat_direction(update_canvas, score, grid, player, line, column, -1, -1):
		eat += 1 << 5
	if check_eat_direction(update_canvas, score, grid, player, line, column, 1, - 1):
		eat += 1 << 6
	if check_eat_direction(update_canvas, score, grid, player, line, column, -1, 1):
		eat += 1 << 7
	return eat

def check_eat_direction(update_canvas, score, grid, player, line, column, direction_line, direction_column):
	global grid_canvas

	line_plus_one = line + direction_line
	column_plus_one = column + direction_column
	line_plus_two = line_plus_one + direction_line
	column_plus_two = column_plus_one + direction_column
	line_plus_three = line_plus_two + direction_line
	column_plus_three = column_plus_two + direction_column
	
	if line_plus_three < 0                                          \
	or line_plus_three >= LINE_NUMBER                               \
	or column_plus_three < 0                                        \
	or column_plus_three >= LINE_NUMBER:
		return False

	other_player = 2 if player == 1 else 1
	if grid[line_plus_one][column_plus_one] == other_player		\
	and grid[line_plus_two][column_plus_two] == other_player	\
	and grid[line_plus_three][column_plus_three] == player:
		grid[line_plus_one][column_plus_one] = 0
		grid[line_plus_two][column_plus_two] = 0
		if update_canvas:
			game_canvas.delete(grid_canvas[line_plus_one][column_plus_one])
			game_canvas.delete(grid_canvas[line_plus_two][column_plus_two])
		score[player] += 2
		if player == 1:
			if update_canvas:
				game_canvas.itemconfigure(player_1_score_text, text = PLAYER_1_COLOR + "\nscore: " + str(score[player]))
				if score[player] >= 10:
					player_win(player)
		else:
			if update_canvas:
				game_canvas.itemconfigure(player_2_score_text, text = PLAYER_2_COLOR + "\nscore: " + str(score[player]))
				if score[player] >= 10:
					player_win(player)
		return True
	return False

def check_double_three(grid, player, line, column):
	three_number = 0
	if check_double_three_direction(grid, player, line, column, 0, 1):
		three_number += 1
	if check_double_three_direction(grid, player, line, column, 1, 0):
		three_number += 1
	if check_double_three_direction(grid, player, line, column, 1, 1):
		three_number += 1
	if check_double_three_direction(grid, player, line, column, 1, - 1):
		three_number += 1
	if three_number >= 2:
		return True
	return False
# .oooo o.ooo
# possible three: .ooo.. ..ooo. .oo.o. .o.oo.
def check_double_three_direction(grid, player, line, column, direction_line, direction_column):
	# start one before
	start_line = line - 5 * direction_line
	start_column = column - 5 * direction_column
	i = 0
	while i < 4:
		start_line += direction_line
		start_column += direction_column
		end_line = start_line + 5 * direction_line
		end_column = start_column + 5 * direction_column

		if start_line < 0 or start_column < 0 or start_line >= LINE_NUMBER or start_column >= LINE_NUMBER:
			i += 1
			continue

		if end_line < 0 or end_column < 0 or end_line >= LINE_NUMBER  or end_column >= LINE_NUMBER:
			break

		# a three is composed of 3 player square and one empty square surrounded by 1 empty square on each side
		if grid[start_line][start_column] != 0 or grid[end_line][end_column] != 0:
			i += 1
			continue

		current_line = start_line
		current_column = start_column
		empty_square = False
		j = 0
		while j < 4:
			current_line += direction_line
			current_column += direction_column
			if current_line == line and current_column == column:
				j += 1
				continue
			elif grid[current_line][current_column] == 0:
				if empty_square:
					empty_square = False
					break
				else:
					empty_square = True
			elif grid[current_line][current_column] != player:
				empty_square = False
				break
			
			j += 1
		if empty_square:
			return True
		
		i += 1
		
	return False

def check_alignment(grid, player, line, column):	
	if check_alignment_direction(grid, player, line, column, 0, 1)						\
	or check_alignment_direction(grid, player, line, column, 1, 0)						\
	or check_alignment_direction(grid, player, line, column, 1, 1)						\
	or check_alignment_direction(grid, player, line, column, 1, - 1):
		return True
	return False
	 
def check_alignment_direction(grid, player, line, column, direction_line, direction_column):
	max_alignment = 0
	i = 0
	current_line = line
	current_column = column
	while current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == player:
		max_alignment += 1
		i += 1
		current_line += direction_line
		current_column += direction_column
	i = -1
	current_line = line - direction_line
	current_column = column - direction_column
	while current_line >= 0											\
	and current_line < LINE_NUMBER									\
	and current_column >= 0											\
	and current_column < LINE_NUMBER								\
	and grid[current_line][current_column] == player:
		max_alignment += 1
		i -= 1
		current_line -= direction_line
		current_column -= direction_column
	
	if max_alignment >= 5:
		return True

	return False

def check_continue(score, grid, player, line, column):
	other_player = 2 if player == 1 else 1
	current_line = 0
	while current_line < LINE_NUMBER:
		current_column = 0
		while current_column < LINE_NUMBER:
			if not check_proximity(grid, current_line, current_column):
				current_column += 1
				continue
			move_success, eat = play_move(False, score, grid, other_player, current_line, current_column)
			if move_success:
				if score[other_player] >= 10								\
				or not check_alignment(grid, player, line, column):
					cancel_move(score, grid, other_player, current_line, current_column, eat)
					return True
				cancel_move(score, grid, other_player, current_line, current_column, eat)
			current_column += 1
		current_line += 1

	return False


## ai_level
def ai_level(event):
	global ai_depth, ai_move_number

	current = game_canvas.gettags(event.widget.find_withtag("current"))

	if current == ():
		return
	elif current[0].isdigit():
		ai_depth = int(current[0])
		if ai_depth == 1:
			ai_move_number = 1000
		elif ai_depth == 2:
			ai_move_number = 50
		elif ai_depth == 3:
			ai_move_number = 15
		elif ai_depth == 4:
			ai_move_number = 7
		elif ai_depth == 5:
			ai_move_number = 5
		elif ai_depth == 6:
			ai_move_number = 4
		elif ai_depth == 7:
			ai_move_number = 3
		elif ai_depth == 8:
			ai_move_number = 2
		elif ai_depth == 9:
			ai_move_number = 2
		elif ai_depth == 10:
			ai_move_number = 2

		debug_log("ai_depth: " + str(ai_depth))
		game_canvas.delete("all")
		print_game()
	else:
		return
	

def print_ai_level():
	game_canvas.create_text(WINDOW_WIDTH / 2, 200, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE * 4, "bold"), text = "Chose AI level")

	i = 1
	shift_y = 0
	while i <= 10:
		shift_x = ((i - 1) % 5 - 2) * 75
		if i == 6:
			shift_y = 75
		game_canvas.create_rectangle(WINDOW_WIDTH / 2 - 30 + shift_x, 370 + shift_y, WINDOW_WIDTH /2 + 30 + shift_x, 430 + shift_y, width = 5, tags = str(i), fill = WINDOW_BACKGROUND_COLOR)
		game_canvas.create_text(WINDOW_WIDTH / 2 + shift_x, 400 + shift_y, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE * 2, "bold"), text = str(i), tags = str(i))
		i += 1

	game_canvas.bind("<Button-1>", ai_level)


## menu
def start(event):
	global player_number, ai_move_number

	current = game_canvas.gettags(event.widget.find_withtag("current"))

	if current == ():
		return
	elif current[0] == "start_ai":
		player_number = 1
		game_canvas.delete("all")
		print_ai_level()
	elif current[0] == "start_player":
		player_number = 2
		ai_move_number = 7
		game_canvas.delete("all")
		print_game()
	else:
		return
	

def print_menu():
	game_canvas.create_text(WINDOW_WIDTH / 2, 200, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE * 5, "bold"), text = "Gomoku")

	game_canvas.create_rectangle(WINDOW_WIDTH / 2 - 160, 370, WINDOW_WIDTH /2 + 160, 430, width = 5, tags = "start_ai", fill = WINDOW_BACKGROUND_COLOR)
	game_canvas.create_text(WINDOW_WIDTH / 2, 400, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE * 2, "bold"), text = "Play against ai", tags = "start_ai")        

	game_canvas.create_rectangle(WINDOW_WIDTH / 2 - 160, 470, WINDOW_WIDTH /2 + 160, 530, width = 5, tags = "start_player", fill = WINDOW_BACKGROUND_COLOR)
	game_canvas.create_text(WINDOW_WIDTH / 2, 500, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE * 2, "bold"), text = "2 Players", tags = "start_player")

	game_canvas.bind("<Button-1>", start)


## game
def init_game():
	global grid, grid_canvas, player, score, is_continue, is_game_finished

	grid = [[0 for i in range(LINE_NUMBER)] for i in range(LINE_NUMBER)]
	grid_canvas = [[0 for i in range(LINE_NUMBER)] for i in range(LINE_NUMBER)]
	score = {1: 0, 2: 0}
	player = 1
	is_continue = False
	is_game_finished = False


def print_game():
	global player_1_score_text, player_2_score_text, ai_timer, ai_first, player

	# init game
	init_game()

	# board lines
	i = 0
	while i < LINE_NUMBER:
		# verticle lines
		game_canvas.create_line(GRID_START, GRID_START + i * SQUARE_SIZE, GRID_START + GRID_SIZE, GRID_START + i * SQUARE_SIZE, fill = WINDOW_LINE_COLOR, width = WINDOW_LINE_WIDTH)
		# horizontal lines
		game_canvas.create_line(GRID_START + i * SQUARE_SIZE, GRID_START, GRID_START + i * SQUARE_SIZE, GRID_START + GRID_SIZE, fill = WINDOW_LINE_COLOR, width = WINDOW_LINE_WIDTH)
		i += 1

	# scores
	player_1_score_text = game_canvas.create_text(TEXT_START, GRID_START, anchor = CENTER, font = (TEXT_FONT, TEXT_SIZE, "bold"), width = TEXT_WIDTH, text = PLAYER_1_COLOR + "\nscore: 0")
	player_2_score_text = game_canvas.create_text(TEXT_START, GRID_END, anchor = CENTER, font = (TEXT_FONT, TEXT_SIZE, "bold"), width = TEXT_WIDTH, text = PLAYER_2_COLOR + "\nscore: 0")

	# buttons
	base_shift_y = 135

	game_canvas.create_rectangle(TEXT_START - 50, GRID_START + base_shift_y - 15, TEXT_START + 50, GRID_START + base_shift_y + 15, width = 5, tags = "restart", fill = WINDOW_BACKGROUND_COLOR)
	game_canvas.create_text(TEXT_START, GRID_START + base_shift_y, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE, "bold"), text = "Restart", tags = "restart")

	shift_y = 40
	
	game_canvas.create_rectangle(TEXT_START - 50, GRID_START + base_shift_y - 15 + shift_y, TEXT_START + 50, GRID_START + base_shift_y + 15 + shift_y, width = 5, tags = "ai_level", fill = WINDOW_BACKGROUND_COLOR)
	game_canvas.create_text(TEXT_START, GRID_START + base_shift_y + shift_y, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE, "bold"), text = "AI level", tags = "ai_level")

	game_canvas.create_rectangle(TEXT_START - 50, GRID_START + base_shift_y - 15 + 2 * shift_y, TEXT_START + 50, GRID_START + base_shift_y + 15 + 2 * shift_y, width = 5, tags = "menu", fill = WINDOW_BACKGROUND_COLOR)
	game_canvas.create_text(TEXT_START, GRID_START + base_shift_y + 2 * shift_y, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE, "bold"), text = "Menu", tags = "menu")

	game_canvas.create_rectangle(TEXT_START - 50, GRID_END - base_shift_y - shift_y - 15, TEXT_START + 50, GRID_END - base_shift_y - shift_y + 15, width = 5, tags = "help", fill = WINDOW_BACKGROUND_COLOR)
	game_canvas.create_text(TEXT_START, GRID_END - base_shift_y - shift_y, anchor = CENTER,  font = (TEXT_FONT, TEXT_SIZE, "bold"), text = "Help", tags = "help")

	# ai timer
	if player_number == 1:
		ai_timer = game_canvas.create_text(TEXT_START, GRID_END - 80, anchor = CENTER, font = (TEXT_FONT, TEXT_SIZE, "bold"), width = TEXT_WIDTH, text = "AI timer:\n0ms")
		if not ai_first:
			# play the first move
			line = 9
			column = 9
			play_move(True, score, grid, player, line, column)
			
			# calc piece_center
			piece_center_x = column * SQUARE_SIZE + GRID_START
			piece_center_y = line * SQUARE_SIZE + GRID_START
			debug_log("piece_center_x " + str(piece_center_x) + " piece_center_y " + str(piece_center_y))
			
			# print piece
			grid_canvas[line][column] = game_canvas.create_oval(piece_center_x - PIECE_RADIUS, piece_center_y - PIECE_RADIUS, piece_center_x + PIECE_RADIUS, piece_center_y + PIECE_RADIUS, fill = PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR)
		
			# change player for next move
			player = 2 if player == 1 else 1
			ai_first = True
		else:
			ai_first = False
	
	# call the click function on left click
	game_canvas.bind("<Button-1>", left_click)


## Main ##
# init
grid = [[0 for i in range(LINE_NUMBER)] for i in range(LINE_NUMBER)]
grid_canvas = [[0 for i in range(LINE_NUMBER)] for i in range(LINE_NUMBER)]
player = 1
score = {1: 0, 2: 0}
is_continue = False
continue_line = 0
continue_column = 0
is_game_finished = False
game_canvas = 0
player_1_score_text = 0
player_2_score_text = 0
player_number = 1
ai_depth = 1
ai_move_number = 2
ai_timer = 0
ai_first = False

# game_window
game_window = Tk()

# game_window title
game_window.title("Gomoku")

# game_window size
game_window.geometry(str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT))

# fix game_window size
game_window.resizable(0,0)

# game_canvas
game_canvas = Canvas(game_window, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, background = WINDOW_BACKGROUND_COLOR)
game_canvas.pack()

print_menu()

game_window.mainloop()
