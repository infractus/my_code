import time, os
import pyinputplus as pyip
from pathlib import Path

import shinsai

p = Path(__file__).parent
os.chdir(p)


TRACK_FILE = 'tracking.json'
CARD_POINTS = {
'2 of Hearts': 1, '3 of Hearts': 1, '4 of Hearts': 1, '5 of Hearts': 1,
'6 of Hearts': 1, '7 of Hearts': 1, '8 of Hearts': 1, '9 of Hearts': 1, 
'10 of Hearts': 1, 'Jack of Hearts': 1, 'Queen of Hearts': 1,
'King of Hearts': 1, 'Ace of Hearts': 1, 'Queen of Spades': 13
	}
CARD_VALUES = {
'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
	}

def game_setup():
	"""Setup for game.
	
	Creates Player objects and assigns them positions around the board.
	Sets up dictionary for tracking points and a list of players.
	"""

	print("\n❤ ❤ ❤ Welcome to Shinsai's Hearts!! ❤ ❤ ❤")

	p1_name = select_player()

	if p1_name == 'Moony (Computer Player)':
		player_1 = shinsai.Player('Moony')
	else:
		player_1 = shinsai.Player(p1_name, is_computer=False)
	player_2 = shinsai.Player('Wendell')
	player_3 = shinsai.Player('Momo')
	player_4 = shinsai.Player('Kya')

	# Create a list of players to work with.
	players = [player_1, player_2, player_3, player_4]

	# Assign players their positions relative to other players.
	assign_positions(player_1, player_2, player_3, player_4)
	assign_positions(player_2, player_3, player_4, player_1)
	assign_positions(player_3, player_4, player_1, player_2)
	assign_positions(player_4, player_1, player_2, player_3)

	# Create dictionary for point tracking.
	point_tracking = {}
	for player in players:
		point_tracking[player] = 0

	return player_1, player_2, player_3, player_4, players, point_tracking


def select_player():
	"""Select Player 1."""
	returning = pyip.inputYesNo("\nHave you played before? ", blank=True)
	if returning == 'yes' or returning == '':
		human_players = ['Moony (Computer Player)']
		for player in tracking["player_stats"].keys():
			if not tracking["player_stats"][player]["is_computer"]:
				human_players.append(player)	
		name = pyip.inputMenu(human_players, blank=True, numbered=True)
	else:
		name = the_game.gather_names()
	return name


def assign_positions(player, player_left, player_across, player_right):
	"""Assign positions around table."""
	player.player_left = player_left
	player.player_across = player_across
	player.player_right = player_right


def set_up_tracking():
	"""Set up the tracking file."""
	for player in players:
		try:
			player_tracking = tracking['player_stats'][f'{player}']
		except:
			tracking['player_stats'][f'{player}'] = {
				'games_played': 0, 'games_won': 0, 'shot_moon': 0, 
				'hands_played': 0, 'total_score': 0, 'total_ties': 0
				}
		if player.is_computer:
			tracking['player_stats'][f'{player}']['is_computer'] = True
		else:
			tracking['player_stats'][f'{player}']['is_computer'] = False
	
	if tracking['game_stats'] == {}:
		tracking['game_stats'] = {
			'total_games': 0, 'total_hands': 0, 'shot_moon': 0,
			'winner_score': 0, 'total_ties': 0
			}

	the_game.write_to_tracking(TRACK_FILE, tracking)


def display_menu():
	"""Display the main menu."""
	while True:
		menu_choices = [
			'Start a game', 'View game stats', 'View players stats',
			'Switch player', 'Quit'
				]
		choice = pyip.inputMenu(menu_choices, numbered=True)
		if choice == 'Start a game':
			start_play()
		elif choice == 'View game stats':
			view_game_stats()
		elif choice == 'View players stats':
			view_player_stats()
		elif choice == 'Switch player':
			break
		else:
			print('\nThanks for playing!')
			the_game.playing = False
			break


def view_game_stats():
	"""View the stats of the game in general."""
	game_stats = tracking['game_stats']
	if game_stats["total_games"] == 0:
		print('There have been no games played yet.')
	else:
		print(f'Out of {game_stats["total_games"]} total games:')
		print(f'The moon was shot {game_stats["shot_moon"]} times.')
		print(f'There have been {game_stats["total_ties"]} tied games.')
		print(
			'The average number of hands per game: '
			f'{round(game_stats["total_hands"] / game_stats["total_games"], 2)}'
				)
		print(
			'The average winner score: '
			f'{round(game_stats["winner_score"] / game_stats["total_games"], 2)}'
				)
	input('\nPress ENTER to return to main menu.')


def view_player_stats():
	"""View stats for each current player."""
	for player in players:
		player_stats = tracking['player_stats'][f'{player}']
		total_games = player_stats['games_played']
		games_won = player_stats['games_won']
		if not total_games:
			print(f'\nNo stats for {player} - no games played.')
			input()
			continue
		print(f'\nStats for {player}:')
		print('------------------')
		print(f'Total games played - {total_games}')
		try:
			print(
				f'Won {games_won} games (including ties) - '
				f'{round(games_won / total_games * 100, 2)}%'
					)
		except:
			print(f'Won {games_won} games (including ties) - 0%')
		try:
			print(
				f'Tied {player_stats["total_ties"]} times - '
				f'{round(player_stats["total_ties"] / games_won * 100, 2)}% '
				'(of wins)'
					)
		except:
			print(f'Tied {player_stats["total_ties"]} times - 100% (of wins)')
		print(
			f'Average score (lower is better): '
			f'{round(player_stats["total_score"] / total_games, 1)}'
				)
		print(f'Shot the moon {player_stats["shot_moon"]} times.')
		print(
			'The average number of hands per game: '
			f'{round(player_stats["hands_played"] / total_games, 1)}'
				)
		input("Press ENTER to continue.")


def start_play():
	"""Starts the game loop."""
	while True:
		play_game()
		play_again = the_game.play_again()
		if play_again == 'no':
			print('\nThanks for playing! Returning to main menu.\n')
			break


def play_game():
	"""Set up a new game."""
	the_game.max_points = the_game.hand_num = 0
	the_game.hearts_broken = False
	for player in players:
		player.points = player.round_points = 0
	begin_hand()
	determine_winner()


def begin_hand():
	"""Start playing a hand."""
	while True:
		playing_hand = set_up_hand()
		if not playing_hand:
			break
		passing_cards()
		play_hand()


def set_up_hand():
	"""Sets up each hand."""
	the_game.hand_num += 1
	the_game.round_num = 0
	the_game.hearts_broken = False
	
	set_points()
	
	if the_game.max_points >= 100:
		# Stop playing the hand if someone breaks 100 points.
		return False
		
	for player in players:
		# Empty each players discard pile to start a new hand.
		player.discard = []

	print(f'\nThis is hand number {the_game.hand_num}.')
	
	deck = the_deck.build_decks(1)
	player_1.hand, player_2.hand, player_3.hand, player_4.hand = \
		the_deck.deal_hands(deck, 13, 4)

	for player in players:
		# Sort hands, show human players their cards.
		player.hand = sort_hand(player, player.hand)
		if not player.is_computer:
			the_deck.show_hand(player, player.hand)
	
	return True


def set_points():
	"""	Adds points for the round to total points for the hand."""
	print()
	for player in players:
		player.points += player.round_points
		print(f'{player} has {player.points} total points.')
	for player in players:
		if player.points > the_game.max_points:
			the_game.max_points = player.points


def sort_hand(player, hand):
	"""Sorts the hand first by suit then by rank."""
	new_hand, final_hand  = [], []

	# Sort hand by value and create new_hand list.
	for v in range(2, 11):
		for card in hand:
			if card.startswith(str(v)):
				new_hand.append(card)
	[new_hand.append(card) for card in hand
		if the_deck.get_value(card) == 'Jack']
	[new_hand.append(card) for card in hand
		if the_deck.get_value(card) == 'Queen']
	[new_hand.append(card) for card in hand
		if the_deck.get_value(card) == 'King']
	[new_hand.append(card) for card in hand
		if the_deck.get_value(card) == 'Ace']
		
	# Sort new_hand by suit to create final_hand.
	[final_hand.append(card) for card in new_hand
		if the_deck.get_suit(card) == 'Hearts']
	[final_hand.append(card) for card in new_hand
		if the_deck.get_suit(card) == 'Spades']
	[final_hand.append(card) for card in new_hand
		if the_deck.get_suit(card) == 'Diamonds']
	[final_hand.append(card) for card in new_hand
		if the_deck.get_suit(card) == 'Clubs']

	return final_hand


def passing_cards():
	"""Pass cards between players."""
	if the_game.hand_num % 4:
		# Passing cards if the game number is not divisible by 4.
		for player in players:
			# Determine which cards to pass for each player.
			player.hand = cards_to_pass(player, player.hand)
		for player in players:
			# Pass the cards between hands.
			pass_cards(player)
		
		for player in players:
			# Sort the hands again and show human players their cards.
			player.hand = sort_hand(player, player.hand)
			if not player.is_computer:
				the_deck.show_hand(player, player.hand)


def cards_to_pass(player, hand):
	"""Determines where each player will pass cards, then calls
	choose_pass() to choose which cards to pass between players.
	"""
	if not player.is_computer:
		if the_game.hand_num % 4 == 1:
			print(
				f'\nChoose 3 cards to pass left to {player.player_left}.'
					)
			new_hand = choose_pass(player, hand)
		if the_game.hand_num % 4 == 2:
			print(
				f'\nChoose 3 cards to pass right to '
				f'{player.player_right}.'
					)
			new_hand = choose_pass(player, hand)
		if the_game.hand_num % 4 == 3:
			print(
				'\nChoose 3 cards to pass across to '
				f'{player.player_across}.'
					)	
			new_hand = choose_pass(player, hand)
	else:
		if the_game.hand_num % 4 == 1:
			new_hand = choose_pass(player, hand, 'left')
		if the_game.hand_num % 4 == 2:
			new_hand = choose_pass(player, hand, 'right')
		if the_game.hand_num % 4 == 3:
			new_hand = choose_pass(player, hand, 'across')
	return new_hand


def choose_pass(player, hand, passing_to=None):
	"""Decide which cards to pass. Returns the players hand without the
	chosen cards.
	"""
	if not player.is_computer:
		new_hand, cards = pick_cards_prompts(hand)
	else:
		new_hand, cards = pick_cards_pc(hand, passing_to)
		
	player.cards_to_pass = cards
	new_hand = new_hand[::-1]
	return new_hand


def pick_cards_prompts(hand):
	"""Prompt human player to pick cards."""
	while True:
		new_hand = hand[:]
		cards = []
		print('\nFirst card:')
		choice = pyip.inputMenu(new_hand, numbered=True)
		new_hand.remove(str(choice))
		cards.append(choice)
		print('\nSecond card:')
		choice = pyip.inputMenu(new_hand, numbered=True)
		new_hand.remove(choice)
		cards.append(choice)
		print('\nThird card:')
		choice = pyip.inputMenu(new_hand, numbered=True)
		new_hand.remove(choice)
		cards.append(choice)
		print(f"\nThe cards you have chosen are: {', '.join(cards)}")
		verify = pyip.inputYesNo('Do you want to pass these cards? ')
		if verify == 'yes':
			break
	return new_hand, cards


def pick_cards_pc(hand, passing_to):
	"""Logic for computer to decide which cards to pass."""
	new_hand = hand[::-1]
	cards = []
	suits = {'Hearts': [], 'Clubs': [], 'Spades': [], 'Diamonds': []}
	for suit in suits.keys():
		# Create a dictionary of the cards in the hand to easily
		# determine how many of each suit is in the hand.
		[suits[suit].append(card)for card in new_hand if card.endswith(suit)]
	for card in new_hand:
		# Always pass the 2 of Clubs
		if card == '2 of Clubs':
			cards.append(card)
			new_hand.remove(card)
			suits['Clubs'].remove(card)
	if passing_to == 'right':
		# Always pass the Queen of Spades right.
		for card in new_hand:
			if card == 'Queen of Spades':
				cards.append(card)
				new_hand.remove(card)
				suits['Spades'].remove(card)
	while len(cards) < 3:
		[pick_3_cards(cards, suits, new_hand, card) \
			for card in new_hand[:] if len(cards) < 3]
								
	return new_hand, cards


def pick_3_cards(cards, suits, new_hand, card):
	"""Logic to pick 3 cards to pass."""
	
	def move_card():
		"""Moves the card between piles."""
		cards.append(card)
		new_hand.remove(card)

	clubs, hearts, diamonds, spades = \
		len(suits['Clubs']), len(suits['Hearts']), \
		len(suits['Diamonds']), len(suits['Spades'])
	if 1 < clubs < 5:
		# If less than 5 clubs void clubs keeping one for first round
		if card.endswith('Clubs'):
			move_card()
			suits['Clubs'].remove(card)
	elif 0 < diamonds < 4:
		# If less than 4 diamonds void diamonds.
		if card.endswith('Diamonds'):
			move_card()
			suits['Diamonds'].remove(card)
	elif 0 < spades < 4 and suits['Spades'] != ['Queen of Spades']:
			# If less than 4 spades void spades but keep the Queen
			if card.endswith('Spades'):
				move_card()
				suits['Spades'].remove(card)
	elif 0 < diamonds <= clubs:
		# If less or same diamonds to clubs and more than zero diamonds
		# use diamond
		if card.endswith('Diamonds'):
			move_card()
			suits['Diamonds'].remove(card)
	elif 1 < clubs <= diamonds:
		# If less or same clubs to diamonds and more than one clubs use
		# clubs
		if card.endswith('Clubs'):
			move_card()
			suits['Clubs'].remove(card)
	else:
		if clubs > 1:
			if card.endswith('Clubs'):
				move_card()
				suits['Clubs'].remove(card)
		elif diamonds > 0:
			if card.endswith('Diamonds'):
				move_card()
				suits['Diamonds'].remove(card)
		elif spades > 0:
			if spades > 1 and card == 'Queen of Spades':
				return
			else:
				if card.endswith('Spades'):
					move_card()
					suits['Spades'].remove(card)
		elif hearts > 0:
			if card.endswith('Hearts'):
				move_card()
				suits['Hearts'].remove(card)


def pass_cards(player):
	"""Pass the cards."""
	if the_game.hand_num % 4 == 1:
		pass_left(player)
		
	if the_game.hand_num % 4 == 2:
		pass_right(player)

	if the_game.hand_num % 4 == 3:
		pass_across(player)


def pass_left(player):
	"""Pass cards left and display results to human players."""
	player.player_left.hand.extend(player.cards_to_pass)
	if not player.is_computer:
		print(
			f'\n{player} passed the cards ' 
			f'{", ".join(player.cards_to_pass)} to {player.player_left}.'
				)
	if not player.player_left.is_computer:
		print(
			f'\n{player} passed the cards '
			f'{", ".join(player.cards_to_pass)} to {player.player_left}.'
				)


def pass_right(player):
	"""Pass cards right and display results to human players."""
	player.player_right.hand.extend(player.cards_to_pass)
	if not player.is_computer:
		print(
			f'\n{player} passed the cards '
			f'{", ".join(player.cards_to_pass)} to ' 
			f'{player.player_right}.'
				)
	if not player.player_right.is_computer:
		print(
			f'\n{player} passed the cards '
			f'{", ".join(player.cards_to_pass)} to '
			f'{player.player_right}.'
				)


def pass_across(player):
	"""Pass cards across and display results to human players."""
	player.player_across.hand.extend(player.cards_to_pass)
	if not player.is_computer:
		print(
			f'\n{player} passed the cards '
			f'{", ".join(player.cards_to_pass)} to '
			f'{player.player_across}.'
				)
	if not player.player_across.is_computer:
		print(
			f'\n{player} passed the cards '
			f'{", ".join(player.cards_to_pass)} to '
			f'{player.player_across}.'
				)


def play_hand():
	"""Play through a hand."""
	whose_turn = ''
	while True:
		# This is the round loop.
		the_game.round_num += 1
		the_game.on_table = []
		for player in players:
			# Reset the played_card variable.
			player.played_card = ''

		whose_turn, suit_led = lead_round(whose_turn)
		whose_turn = continue_round(whose_turn, suit_led)	
		whose_turn = resolve_round(suit_led)
		check_shoot_the_moon()

		if not player_1.hand:
			# If the hand is empty, stop playing the hand.
			break


def lead_round(whose_turn):
	"""The first turn of a round."""
	if the_game.round_num == 1:
		# Always play 2 of Clubs on first round.
		played_first = first_turn()
		the_game.on_table.append('2 of Clubs')
		played_first.hand.remove('2 of Clubs')
		whose_turn = played_first.player_left
		suit_led = 'Clubs'
		played_first.played_card = '2 of Clubs'
		if not player_1.is_computer:
			time.sleep(.5)
	else:
		print(f'\nIt is now {whose_turn}\'s turn.\n')
		card = take_turn(whose_turn, leading=True)
		suit_led = the_deck.get_suit(card)
		whose_turn = resolve_turn(whose_turn, card)
		if not player_1.is_computer:
			time.sleep(.5)
	return whose_turn, suit_led


def first_turn():
	"""2 of Clubs goes first in first round."""
	for player in players:
		if '2 of Clubs' in player.hand:
			print(
				f'\n{player} has the 2 of Clubs and will go first. ' 
				f'\n{player} lays the 2 of Clubs.'
					)
			return player


def take_turn(player, suit_led=None, leading=False, table=None):
	"""Take a turn."""
	viable_cards = choose_viable_cards(player, suit_led)
	
	if player.is_computer:
		card = take_turn_pc(suit_led, leading, viable_cards, table)
		
	else:
		card = take_turn_human(suit_led, leading, viable_cards)

	if card.endswith('Hearts'):
		if not the_game.hearts_broken:
			the_game.hearts_broken = True
			if not player_1.is_computer:
				print('\nHearts have been broken!')
				input('Press ENTER to continue.')
	return card


def choose_viable_cards(player, suit_led):
	"""Make a list of viable cards to play."""
	viable_cards = []
	for card in player.hand:
		if not the_game.hearts_broken:
			# Hearts not viable until broken.
			if card.endswith('Hearts'):
				continue
		if the_game.round_num == 1:
			# Cannot play Queen of Spades on first round.
			if card == 'Queen of Spades':
				continue
		if suit_led:
			# If a suit was led, only viable cards are suit.
			if card.endswith(suit_led):
				viable_cards.append(card)
		else:			
			# If player leading, all cards are viable.
			viable_cards.append(card)
	if not viable_cards:
		# If no possible cards, all cards are viable.
		for card in player.hand:
			if not player.is_computer:
				# All cards viable for human players.
				viable_cards.append(card)
			else:
				# Only points cards viable for computer players.
				if card.endswith('Hearts') or card == 'Queen of Spades':
					viable_cards.append(card)
				if not viable_cards:
					# If no points card in hand, all cards viable.
					viable_cards.append(card)
	return viable_cards


def take_turn_pc(suit_led, leading, viable_cards, table):
	"""Logic for choosing which card to play."""
	if len(viable_cards) == 1:
		card = viable_cards[0]
		return card
	if leading:
		card = pc_leading(viable_cards)
	else:
		card = pc_not_leading(suit_led, viable_cards, table)		
	return card		


def pc_leading(viable_cards):
	"""Choose which card to play if leading."""
	card_vals = ('2', '3', '4')
	for choice in viable_cards:
		# Lead first with low value hearts.
		if choice.endswith('Hearts') and choice.startswith(card_vals):
			card = choice
			return card
	else:
		current_lowest = 15
		lowest_card, choice = '', ''	
		for choice in viable_cards[::-1]:
			val = int(CARD_VALUES[the_deck.get_value(choice)])
			if not choice.endswith('Hearts') and choice != 'Queen of Spades':
				# Play lowest non-heart card.
				if val < current_lowest:
					current_lowest = val
					lowest_card = choice
			if lowest_card == '' or lowest_card.endswith('Hearts')\
					and choice != 'Queen of Spades':
				# If there are only hearts cards, play the lowest.
				if val < current_lowest:
					current_lowest = val
					lowest_card = choice
		card = lowest_card				
		return card


def pc_not_leading(suit_led, viable_cards, table):
	"""Determine card to play if not leading."""
	if 'Queen of Spades' in viable_cards and suit_led != 'Spades':
		return 'Queen of Spades'

	if suit_led != 'Hearts':
		# Break hearts if no other choice, playing highest.
		if viable_cards[-1].endswith('Hearts'):
			if not the_game.hearts_broken:
				the_game.hearts_broken = True
				if not player_1.is_computer:
					print('\nHearts have been broken!')
					input('Press ENTER to continue.')
			return viable_cards[-1]
	
	card = determine_highest_card(suit_led, viable_cards, table)
	
	return card


def determine_highest_card(suit_led, viable_cards, table):
	"""
	Determines the highest card on the table and chooses what card to play.
	"""
	current_highest = 0
	for crd in table:
		# Determine highest value of cards on table with led suit.
		val = int(CARD_VALUES[the_deck.get_value(crd)])
		if crd.endswith(suit_led):
			if val > current_highest:
				current_highest = val

	highest_card, choice = '', ''
	for choice in viable_cards:
		# Play the next lowest card of led suit without going over.
		val = int(CARD_VALUES[the_deck.get_value(choice)]) 
		if current_highest > val:
			highest_card = choice
		if highest_card:
			high_val = int(CARD_VALUES[the_deck.get_value(highest_card)])
			if current_highest > val > high_val:	
				highest_card = choice
		card = highest_card
	if not highest_card:
		# Play the next lowest, but not Queen of Spades.
		for choice in viable_cards:	
			if choice != 'Queen of Spades':
				card = viable_cards[0]
				return card
			else:
				card = viable_cards[1]
				return card
	return card


def take_turn_human(suit_led, leading, viable_cards):
	"""	Prompts to choose from viable cards for human players."""
	if leading == True:
		print('Choose a card to lead:')
	else:
		print('Choose a card to play:')
		print(f'{suit_led} is the leading suit.\n')
	if len(viable_cards) == 1:
		print(f'\nOnly one card in viable cards: {viable_cards[0]}')
		input()
		card = viable_cards[0]
	else:	
		card = pyip.inputMenu(viable_cards, numbered=True)
	return card


def resolve_turn(whose_turn, card):
	"""Resolves a turn, returns whose turn is next."""
	print(f'{whose_turn} played the {card}.')
	the_game.on_table.append(card)
	whose_turn.hand.remove(card)
	whose_turn.played_card = card
	whose_turn = whose_turn.player_left
	return whose_turn


def continue_round(whose_turn, suit_led):
	"""The remaining turns of a round."""
	while len(the_game.on_table) < 4:
		if len(the_game.on_table) > 0:
			the_deck.show_table(the_game.on_table)
		print(f'\nIt is now {whose_turn}\'s turn.')
		card = take_turn(whose_turn, suit_led, table=the_game.on_table)
		whose_turn = resolve_turn(whose_turn, card)
		if not player_1.is_computer:
			time.sleep(.5)
	return whose_turn


def resolve_round(suit_led):
	"""Resolve a round."""
	winning_value, winning_card = 0, ''
	the_deck.show_table(the_game.on_table)
	for card in the_game.on_table:
		# Determine which card of the suit led is highest.
		if card.endswith(suit_led):
			if CARD_VALUES[the_deck.get_value(card)] > winning_value:
				winning_value = CARD_VALUES[the_deck.get_value(card)]
				winning_card = card
	for player in players:
		# The player with the highest card "wins" the round.
		if winning_card == player.played_card:
			winner = player
			if not player_1.is_computer:
				print(f'\n{winner} takes the cards with the {winning_card}.')
				time.sleep(.5)

	whose_turn = winner
	winner.discard.extend(the_game.on_table)
	the_game.on_table = []
	
	add_points()

	return whose_turn


def add_points():
	"""Adds points for each card player has taken this hand."""
	for player in players:
		player.round_points = 0
		for card in player.discard:
			if card in CARD_POINTS.keys():
				player.round_points += CARD_POINTS[card]
		if not player.is_computer:				
			print(
				f'\n{player} has {player.round_points} points in their '
				'discard pile.'
					)


def check_shoot_the_moon():
	"""Check if any players shot the moon."""
	for player in players:
		if player.round_points == 26:
			player.round_points = 0
			player.player_across.round_points = 26
			player.player_left.round_points = 26
			player.player_right.round_points = 26
			if not player_1.is_computer:
				print(f'\n{player} SHOT THE MOON!!!')
				input('Press ENTER to continue.')
			tracking['player_stats'][f'{player}']['shot_moon'] += 1
			tracking['game_stats']['shot_moon'] += 1
			the_game.write_to_tracking(TRACK_FILE, tracking)
			return True


def determine_winner():
	"""Determine who won the game and displays results."""
	update_stats()
	
	low_points, winner = 100, None
	for player in players:
		if player.points < low_points:
			low_points, winner = player.points, player
	winners = [winner]
	for player in players:
		# Check for ties.
		if player != winner:
			if player.points == winner.points:
				winners.append(player)

	if len(winners) == 1:
		# Display the winner if no tie.
		print(
			f'\nAfter {the_game.hand_num} hands, {winner} has won with '
			f'{low_points} points.'
				)
		pass
	else:
		# Display the winners if tie.
		winner_list = []
		for won in winners:
			winner_list.append(str(won))
		winner_str = ', '.join(winner_list)
		print(
			f'\nAfter {the_game.hand_num} hands, the following players have '
			f'won with {low_points} points:\n{winner_str}'
				)
		for winner in winners:
			tracking['player_stats'][f'{winner}']['total_ties'] += 1
		tracking['game_stats']['total_ties'] += 1

	tracking['game_stats']['winner_score'] += winner.points
	for winner in winners:
		tracking['player_stats'][f'{winner}']['games_won'] += 1
	the_game.write_to_tracking(TRACK_FILE, tracking)


def update_stats():
	"""Updates game-level stats for tracking."""	
	tracking['game_stats']['total_games'] += 1
	tracking['game_stats']['total_hands'] += the_game.hand_num
	for player in players:
		tracking['player_stats'][f'{player}']['games_played'] += 1
		tracking['player_stats'][f'{player}']['hands_played'] \
			+= the_game.hand_num
		tracking['player_stats'][f'{player}']['total_score'] += player.points
	the_game.write_to_tracking(TRACK_FILE, tracking)


the_deck, the_game = shinsai.Deck(), shinsai.Game()
tracking = the_game.get_stored_tracking(TRACK_FILE)
while the_game.playing:
	player_1, player_2, player_3, player_4, players, point_tracking = \
		game_setup()
	set_up_tracking()
	display_menu()