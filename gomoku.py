try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
import copy

# constants
DEBUG_MODE = True
LINE_NUMBER = 19	# do not change line number without changing center eval
SQUARE_SIZE = 37
GRID_SIZE = (LINE_NUMBER - 1) * SQUARE_SIZE
GRID_START = 50
GRID_END = GRID_START + GRID_SIZE
TEXT_START = GRID_END + 50
TEXT_SIZE = 16
TEXT_WIDTH = 100
TEXT_FONT = "Helvetica"
WINDOW_BACKGROUND_COLOR = "brown"
WINDOW_LINE_WIDTH = 4
WINDOW_LINE_COLOR = "black"
WINDOW_WIDTH = GRID_START + GRID_SIZE + TEXT_START - GRID_END + TEXT_WIDTH + GRID_START
WINDOW_HEIGHT = GRID_START + GRID_SIZE + GRID_START 
PLAYER_1_COLOR = "black"
PLAYER_2_COLOR = "white"
PIECE_RADIUS = int(SQUARE_SIZE / 2.3)
IA_DEPTH = 10
MIN_VALUE = -100000
MAX_VALUE = 100000
PLAYER_NUMBER = 1
PROXIMITY_MAX = 1
COUNT_MAX = 3


# function used for debug log
def debug_log(message):
	if DEBUG_MODE:
		print(message)

## IA functions
def ia(score, grid, player, is_continue, continue_line, continue_column, depth):
	count = 0
	alpha = MIN_VALUE - 1
	beta = MAX_VALUE + 1
	max_line = 0
	max_column = 0
	line = 0
	is_second_turn = False
	other_player = 2 if player == 1 else 1

	while line < LINE_NUMBER:
		column = 0
		while column < LINE_NUMBER:
			if not is_second_turn and not check_ia_move(grid, line, column)		\
			or is_second_turn and not check_proximity(grid, line, column):
				column += 1
				continue
			move_success, eat = play_move(False, score, grid, player, line, column)
			if move_success:
				if score[player] >= 10:
					current_value = MAX_VALUE
				elif is_continue and check_alignment(grid, other_player, continue_line, continue_column):
					current_value = MIN_VALUE
				elif check_alignment(grid, player, line, column):
					current_value = ia_min(score, grid, player, True, line, column, depth - 1, alpha, beta)
				elif count < COUNT_MAX:
					count += 1
					current_value = ia_min(score, grid, player, False, continue_line, continue_column, depth - 1, alpha, beta)
				else:
					cancel_move(score, grid, player, line, column, eat)
					column += 1
					continue
				if current_value > alpha:
					alpha = current_value
					max_line = line
					max_column = column
				cancel_move(score, grid, player, line, column, eat)
			column += 1
		line += 1
		# if no possible move is found
		if line == LINE_NUMBER and column == LINE_NUMBER and alpha == MIN_VALUE - 1:
			line = 0
			column = 0
			is_second_turn = True

	debug_log(alpha)
	return max_line, max_column

def ia_min(score, grid, player, is_continue, continue_line, continue_column, depth, alpha, beta):
	min_value = MAX_VALUE + 1
	line = 0
	is_second_turn = False
	other_player = 2 if player == 1 else 1
	count = 0

	if depth == 0:
		if is_continue:
			return MAX_VALUE / 2 - (IA_DEPTH - depth)
		return heuristic(score, grid, player)

	while line < LINE_NUMBER:
		column = 0
		while column < LINE_NUMBER:
			if not is_second_turn and not check_ia_move(grid, line, column)		\
			or is_second_turn and not check_proximity(grid, line, column):
				column += 1
				continue
			move_success, eat = play_move(False, score, grid, other_player, line, column)
			if move_success:
				if score[other_player] >= 10:
					current_value = MIN_VALUE + (IA_DEPTH - depth)
				elif is_continue and check_alignment(grid, player, continue_line, continue_column):
					current_value = MAX_VALUE - (IA_DEPTH - depth)
				elif check_alignment(grid, other_player, line, column):
					current_value = ia_max(score, grid, player, True, line, column, depth - 1, alpha, beta)
				elif count < COUNT_MAX:
					count += 1
					current_value = ia_max(score, grid, player, False, continue_line, continue_column, depth - 1, alpha, beta)
				else:
					cancel_move(score, grid, player, line, column, eat)
					column += 1
					continue
				min_value = min(current_value, min_value)
				cancel_move(score, grid, other_player, line, column, eat)
				if alpha >= current_value:
					return current_value
				beta = min(min_value, beta)
			column += 1
		line += 1
		# if no possible move is found
		if line == LINE_NUMBER and column == LINE_NUMBER and min_value == MAX_VALUE + 1:
			line = 0
			column = 0
			is_second_turn = True

	return beta

def ia_max(score, grid, player, is_continue, continue_line, continue_column, depth, alpha, beta):
	max_value = MIN_VALUE - 1
	line = 0
	is_second_turn = False
	other_player = 2 if player == 1 else 1
	count = 0

	if depth == 0:
		if is_continue:
			return MIN_VALUE / 2 + (IA_DEPTH - depth)
		return heuristic(score, grid, player)

	while line < LINE_NUMBER:
		column = 0
		while column < LINE_NUMBER:
			if not is_second_turn and not check_ia_move(grid, line, column)		\
			or is_second_turn and not check_proximity(grid, line, column):
				column += 1
				continue
			move_success, eat = play_move(False, score, grid, player, line, column)
			if move_success:
				if score[player] >= 10:
					current_value = MAX_VALUE - (IA_DEPTH - depth)
				elif is_continue and check_alignment(grid, other_player, continue_line, continue_column):
					current_value = MIN_VALUE + (IA_DEPTH - depth)
				elif check_alignment(grid, player, line, column):
					current_value = ia_min(score, grid, player, True, line, column, depth - 1, alpha, beta)
				elif count < COUNT_MAX:
					count += 1;
					current_value = ia_min(score, grid, player, False, continue_line, continue_column, depth - 1, alpha, beta)
				else:
					cancel_move(score, grid, player, line, column, eat)
					column += 1
					continue
				max_value = max(current_value, max_value)
				cancel_move(score, grid, player, line, column, eat)
				if beta <= current_value:
					return current_value
				alpha = max(max_value, alpha)
			column += 1
		line += 1
		# if no possible move is found
		if line == LINE_NUMBER and column == LINE_NUMBER and max_value == MIN_VALUE - 1:
			line = 0
			column = 0
			is_second_turn = True

	return alpha

def check_ia_move(grid, line, column):
	if check_ia_move_direction(grid, line, column, 0, 1):
		return True
	if check_ia_move_direction(grid, line, column, 1, 0):
		return True
	if check_ia_move_direction(grid, line, column, 1, 1):
		return True
	if check_ia_move_direction(grid, line, column, -1, 1):
		return True
	return False

def check_ia_move_direction(grid, line, column, direction_line, direction_column):
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



	return False

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
	and current_line < LINE_NUMBER                                                                          \
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
	eval = 0

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

	if is_game_finished or (PLAYER_NUMBER == 1 and player == 2):
		return

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

	# if against ia, call ia
	if PLAYER_NUMBER == 1:
		# check if game is finish
		if is_game_finished:
			return
		
		# update Canvas
		game_window.update()

		# find ia move
		line, column = ia(score, grid, player, is_continue, continue_line, continue_column, IA_DEPTH)
		
		# play the move
		move_success, eat = play_move(True, score, grid, player, line, column)
		if not move_success:
			return # TEMP fatal error

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

	debug_log(str(PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR) + " win")
	game_canvas.create_text(TEXT_START, GRID_START + GRID_SIZE / 2, anchor = W, font = (TEXT_FONT, TEXT_SIZE, "bold"), width = TEXT_WIDTH, text = str(PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR) + "\nwin !")
	is_game_finished = True
	is_continue = False

def play_move(update_canvas, score, grid, player, line, column):
	# check if the move can be played
	if grid[line][column] != 0:
		# debug_log("there is already a piece here")
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
			if grid[current_line][current_column] == 0:
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
		# debug_log("alignment")
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

## Main ##
# init game
grid = [[0 for i in range(LINE_NUMBER)] for i in range(LINE_NUMBER)]
grid_canvas = [[0 for i in range(LINE_NUMBER)] for i in range(LINE_NUMBER)]
player = 1
score = {1: 0, 2: 0}
is_continue = True
continue_line = 0
continue_column = 0
is_game_finished = False

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

# call the click function on left click
game_canvas.bind("<Button-1>", left_click)

# board lines
i = 0
while i < LINE_NUMBER:
	# verticle lines
	game_canvas.create_line(GRID_START, GRID_START + i * SQUARE_SIZE, GRID_START + GRID_SIZE, GRID_START + i * SQUARE_SIZE, fill = WINDOW_LINE_COLOR, width = WINDOW_LINE_WIDTH)
	# horizontal lines
	game_canvas.create_line(GRID_START + i * SQUARE_SIZE, GRID_START, GRID_START + i * SQUARE_SIZE, GRID_START + GRID_SIZE, fill = WINDOW_LINE_COLOR, width = WINDOW_LINE_WIDTH)
	i += 1

# scores
player_1_score_text = game_canvas.create_text(TEXT_START, GRID_START, anchor = NW, font = (TEXT_FONT, TEXT_SIZE, "bold"), width = TEXT_WIDTH, text = PLAYER_1_COLOR + "\nscore: 0")
player_2_score_text = game_canvas.create_text(TEXT_START, GRID_END, anchor = SW, font = (TEXT_FONT, TEXT_SIZE, "bold"), width = TEXT_WIDTH, text = PLAYER_2_COLOR + "\nscore: 0")

game_window.mainloop()
