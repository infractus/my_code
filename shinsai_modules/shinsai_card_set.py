from shinsai_pygame import Images

"""Module for a set of cards, and images of individual cards."""

class CardSet:
	"""Represents a set of cards.
	Each card is an object of the Card class.
	"""

	def __init__(self, card_game):
		"""
		Initialize attributes to represent the overall set of cards.
		"""
		self.card_game = card_game
		self.cards = []
		self.card_back = []
		self._load_cards()
		
	def _load_cards(self):
		"""Builds the overall set:
		- Loads images from the sprite sheet.
		- Creates a Card object, and sets appropriate attributes for
			that card.
		- Adds each card to the list self.cards.
		"""
		filename = 'images/playing_cards.bmp'
		card_ss = Images(self.card_game, filename)

		# Load all card images.
		card_images = card_ss.load_grid_images(5, 13, 0, 1, 0, 0)

		# Create a new card for each image.
		suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
		faces = ['Jack','Queen', 'King']
		names = []
		names.append('Ace')
		[names.append(str(n)) for n in range(2, 11)]
		[names.append(face) for face in faces]

		card_num = 0
		for suit in suits:
			for name in names:
				card = Card(self.card_game)
				card.name = f'{name} of {suit}'
				card.suit = suit
				card.value = name
				if suit in ['Clubs', 'Spades']:
					card.color = 'black'
				else:
					card.color = 'red'
				card.image = card_images[card_num]
				self.cards.append(card)
				card_num += 1

		card = Card(self.card_game)
		card.name = 'card_back'
		card.image = card_images[card_num + 2]
		self.card_back.append(card)


class Card:
	"""Represents a card."""
	def __init__(self, card_game):
		"""Initialize attributes to represent a card."""
		self.image = None
		self.name = ''
		self.color = ''
		self.pressed = False
		self.selected = False

		self.screen = card_game.screen

		# Start each card off at the top left corner.
		self.x, self.y = 0.0, 0.0

	def blitme(self):
		"""Draw the card at it's current location."""
		self.rect = self.image.get_rect()
		self.rect.topleft = self.x, self.y
		self.screen.blit(self.image, self.rect)

	def __str__(self):
		return self.name