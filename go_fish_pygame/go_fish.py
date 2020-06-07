#! python3
# Go Fish done for "Challenges" for Python Crash Course -
# https://ehmatthes.github.io/pcc_2e/challenges/playing_cards/
# Some of the code is copied or adapted from Python Crash Course.


import random, os
from pathlib import Path

import shinsai, shinsai_pygame, shinsai_card_set

p = Path(__file__).parent
os.chdir(p)

class GoFish:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize a game of Go Fish."""
        self.the_game = shinsai_pygame.GUIGame("Go Fish!")
        self.card_set = shinsai_card_set.CardSet(self.the_game)
        self.the_deck = shinsai_pygame.GUIDeck(self.card_set)
        self.tracking = self.the_game.get_stored_tracking(
            self.the_game.settings.track_file
        )
        self.menu_sound = self.the_game.create_sound('sounds/switch7.wav')
        self.the_game.settings.bg_color = (0, 100, 40)
        self.the_game.settings.board_text_color = self.the_game.settings.black
        self.the_game.settings.menu_text_color = self.the_game.settings.green

    def run_game(self):
        """Start the main loop for the game."""
        while the_game.playing:
            self.game_setup()
            self.check_tracking()
            self.display_menu()

    def game_setup(self):
        """Set up the game."""
        while True:
            button_clicked = self.display_welcome_screen()

            while True:
                # Wait for player to click on the button.
                pressed = the_game.wait_for_input()
                if button_clicked.rect.collidepoint(the_game.x, the_game.y):
                    the_game.x = the_game.y = -5
                    the_game.play_sound(self.menu_sound)
                    break
                elif pressed == 'Esc':
                    the_game.terminate(True)
                else:
                    the_game.play_sound(self.menu_sound)
                    break
            p1_name = self.select_player()
            the_game.update_display()

            if p1_name:
                if p1_name == 'Marina (PC)':
                    self.player_1 = shinsai.Player('Marina')
                else:
                    self.player_1 = shinsai.Player(p1_name, is_computer=False)

                self.player_2 = shinsai.Player('Luna')

                self.players = [self.player_1, self.player_2]
                self.player_1.opponent = self.player_2
                self.player_2.opponent = self.player_1

                the_game.round_num = 0
                the_game.game_over = False
                break

    def display_welcome_screen(self):
        """The first screen the player sees."""
        the_game.screen.fill(settings.black)
        fish = shinsai_pygame.Images(the_game, 'images/fish.png')
        fish_rect = fish.sheet.get_rect()
        fish_image = fish.image_at(fish_rect)
        fish.display_image(fish_image, fish_rect, fish_rect.width / 2, 25)
        the_game.draw_text(
            "Welcome to Shinsai's Go Fish!", the_game.screen,
            screen_rect.width / 2, screen_rect.height / 2 + 100,
            settings.large_font, settings.menu_text_color
        )
        the_game.draw_bottom_text(
            "Press ESC to quit.", settings.menu_text_color
        )

        button = shinsai_pygame.Button(
            the_game, "Press to Begin", settings.green, settings.blue, 240,
            coords=(
                settings.screen_width / 2, settings.screen_height / 2 + 200
            )
        )
        shinsai_pygame.Button.draw_button(button)
        the_game.update_display()
        return button

    def select_player(self):
        """Choose a player."""
        pressed = the_game.yes_no_buttons(
            "Have you played before?", the_game, settings.menu_text_color,
            settings.green, settings.blue, settings.black,
            "Press ESC to return to title screen."
        )

        if pressed == 'Esc':
            the_game.play_sound(self.menu_sound)
            return
        if pressed == 'y':
            the_game.x = the_game.y = -5
            the_game.play_sound(self.menu_sound)
            name = self.returning_user()
            return name
        if pressed == 'n':
            the_game.x = the_game.y = -5
            the_game.play_sound(self.menu_sound)
            name = the_game.gather_names()
            return name

    def returning_user(self):
        """Select a returning user."""
        the_game.screen.fill(settings.black)
        human_players = ['Marina (PC)']
        players = tracking["player_stats"].keys()
        for player in players:
            if not tracking["player_stats"][f'{player}']["is_computer"]:
                human_players.append(player)
        the_game.draw_text(
            "Select a player using the number listed:", the_game.screen,
            screen_rect.width / 2, 100, settings.large_font,
            settings.menu_text_color
        )

        text_y = 200
        buttons = []
        for i, choice in enumerate(human_players):
            text_y += 50
            button = shinsai_pygame.Button(
                the_game, f"{i+1}) {choice}", color=settings.lightblue,
                width = 400, height=40, coords=(screen_rect.width / 2, text_y)
            )
            button.draw_button()
            buttons.append(button)

        the_game.draw_bottom_text(
            "Press ESC to return to title screen.", settings.menu_text_color
        )
        name = self.select_name(buttons, human_players)
        return name

    def select_name(self, buttons, human_players):
        """Select a name from existing user list."""
        while True:
            the_game.update_display()
            pressed = the_game.wait_for_input(numbered=True)
            if pressed:
                if pressed == 'Esc':
                    the_game.play_sound(self.menu_sound)
                    break
                if pressed == 'button':
                    for button in buttons:
                        if button.rect.collidepoint(the_game.x, the_game.y):
                            the_game.x = the_game.y = -5
                            the_game.play_sound(self.menu_sound)
                            name = f'{button}'.split(None, 1)[1]
                            return name
                try:
                    name = human_players[pressed-1]
                    the_game.play_sound(self.menu_sound)
                    return name
                except:
                    pressed = None

    def check_tracking(self):
        """Creates appropriate key/value pairs in tracking file."""
        player_stats = tracking['player_stats']
        game_stats = tracking['game_stats']

        for player in self.players:
            if f'{player}' in player_stats.keys():
                continue
            player_stats[f'{player}'] = {}
            player_stats[f'{player}'][f'{player.opponent}'] = [0, 0]
            player_stats[f'{player}']['is_computer'] = player.is_computer
            player_stats[f'{player}']['total_games'] = 0
            player_stats[f'{player}']['total_pairs'] = 0
            player_stats[f'{player}']['total_wins'] = 0
            player_stats[f'{player}']['total_losses'] = 0
            player_stats[f'{player}']['total_rounds'] = 0

        for player in self.players:
            if f'{player.opponent}' in player_stats[f'{player}'].keys():
                continue
            player_stats[f'{player}'][f'{player.opponent}'] = [0,0]

        if game_stats == {}:
            game_stats.update(
                {'total_games': 0, 'total_rounds': 0, 'num_ties': 0}
            )

        the_game.write_to_tracking(settings.track_file, tracking)

    def display_menu(self):
        """Display the main menu."""
        while True:
            the_game.screen.fill(settings.black)
            the_game.draw_text(
                f"Welcome, {self.player_1}!", the_game.screen,
                screen_rect.width / 2, 100, settings.large_font,
                settings.menu_text_color
            )
            the_game.draw_text(
                "Select an option:", the_game.screen, screen_rect.width / 2,
                200, settings.large_font, settings.menu_text_color
            )
            menu_choices = [
                'Start a game', 'View game stats', 'View players stats',
                'Switch player', 'Quit'
            ]
            the_game.draw_bottom_text(
                "Press ESC to return to title screen.",
                settings.menu_text_color
            )

            text_y = 300
            buttons = []
            for i, choice in enumerate(menu_choices):
                text_y += 50
                button = shinsai_pygame.Button(
                    the_game, f"{i+1}) {choice}", color=settings.lightblue,
                    width = 400, height=40, coords=(
                        screen_rect.width / 2, text_y
                    )
                )
                button.draw_button()
                buttons.append(button)

            choice = None
            the_game.update_display()
            pressed = the_game.wait_for_input(numbered=True)
            if pressed == 'Esc':
                the_game.play_sound(self.menu_sound)
                break
            if pressed == 'button':
                for i, button in enumerate(buttons):
                    if button.rect.collidepoint(the_game.x, the_game.y):
                        the_game.x = the_game.y = -5
                        the_game.play_sound(self.menu_sound)
                        choice = menu_choices[i]
            else:
                try:
                    for i in menu_choices:
                        choice = menu_choices[pressed-1]
                        the_game.play_sound(self.menu_sound)
                except:
                    pressed = None
            if pressed:
                if choice == 'Start a game':
                    the_game.game_over = False
                    self.start_play()
                elif choice == 'View game stats':
                    self.view_game_stats()
                elif choice == 'View players stats':
                    self.view_player_stats()
                elif choice == 'Switch player':
                    break
                elif choice == 'Quit':
                    the_game.playing = False
                    break

    def start_play(self):
        """Starts the game loop."""
        while True:
            if not the_game.game_over:
                self.new_game()
            else:
                play_again = the_game.yes_no_buttons(
                    "Would you like to play again?", the_game,
                    settings.menu_text_color, settings.green, settings.blue,
                    settings.black
                )
                if play_again == 'n':
                    self.show_record()
                    break
                else:
                    self.new_game()

    def new_game(self):
        """Create new game."""
        the_game.round_num = 0
        the_game.game_over = False
        the_game.deck = self.the_deck.build_decks(1)
        the_game.x = the_game.y = -5
        self.player_1.hand, self.player_2.hand = \
            self.the_deck.deal_hands(the_game.deck, 7, 2)
        for player in self.players:
            player.table, player.wait_list = [], []
            player.drew_match = False

        the_game.turn = the_game.who_goes_first()
        self.show_record()
        self.show_who_first()
        self.check_for_pairs()
        self.play_game()

    def show_record(self):
        """Shows the record of wins/losses."""
        the_game.screen.fill(settings.black)

        track_list = tracking["player_stats"][f"{self.player_1}"]\
            [f"{self.player_2}"]
        the_game.draw_center_text(
            f'{self.player_1} has {track_list[0]} wins and {track_list[1]}'
            f' losses against {self.player_2}.', settings.menu_text_color
                )

        the_game.press_any_key(self.menu_sound)

    def show_who_first(self):
        """Display who is going first."""
        the_game.screen.fill(settings.black)
        if the_game.turn == 1:
            the_game.turn = {self.player_1}
            the_game.draw_center_text(
                f'{self.player_1} goes first.', settings.menu_text_color
                    )
        else:
            the_game.turn = {self.player_2}
            the_game.draw_center_text(
                f'{self.player_2} goes first.', settings.menu_text_color
                    )
        the_game.press_any_key(self.menu_sound)

    def check_for_pairs(self):
        """Checks each hand for pairs.
        Places them in the appropriate table.
        Returns True if either player had a pair.
        """
        same = False
        for player in self.players:
            player.same = False
            pairs = {}
            for card in player.hand:
                pairs[card.value] = []
            for card in player.hand:
                pairs[card.value].append(card)
            for value in pairs.values():
                if len(value) == 2 or len(value) == 3:
                    player.same = True
                    player.table.append(value[0])
                    player.hand.remove(value[0])
                    player.table.append(value[1])
                    player.hand.remove(value[1])
                if len(value) == 4:
                    player.same = True
                    for card in value:
                        player.table.append(card)
                        player.hand.remove(card)
        for player in self.players:
            if player.same:
                same = True
        return same

    def play_game(self):
        """The main game loop."""
        while True:
            while not the_game.game_over:
                the_game.check_for_input()
                self.update_screen()
                the_game.round_num += 1

                for player in self.players:
                    while the_game.turn == {player}:
                        self.take_turn(player)
                        self.update_screen()
                        if the_game.game_over:
                            break
            if the_game.game_over:
                break

    def update_screen(self):
        """Updates the screen."""
        self.check_for_clicks()
        self.draw_board()
        self.draw_hands()
        self.draw_tables()
        the_game.update_display()

    def check_for_clicks(self):
        """Checks if a button has been clicked."""
        try:
            for card in self.player_1.hand:
                if card.button_rect.collidepoint(the_game.x, the_game.y):
                    card.pressed = True
                    the_game.x = the_game.y = -5
                if the_game.exit_button.rect.collidepoint(
                    the_game.x, the_game.y
                ):
                    the_game.terminate(True)
        except:
            return

    def draw_board(self):
        """Draw the board."""
        the_game.screen.fill(settings.bg_color)
        the_game.draw_line(the_game.screen, (190, 200), (190, 600), 10)
        the_game.draw_line(the_game.screen, (1000, 200), (1000, 600), 10)
        the_game.draw_text(
            f'Round: {the_game.round_num}', the_game.screen, 120, 50,
            settings.medium_font, settings.board_text_color
        )
        the_game.draw_text(
            f'{self.player_1}', the_game.screen, screen_rect.width / 2, 770,
            settings.medium_font, settings.board_text_color
        )
        the_game.draw_text(
            f"{self.player_1}'s", the_game.screen, 105, 140,
            settings.basic_font, settings.board_text_color
        )
        the_game.draw_text(
            f"pairs:", the_game.screen, 105, 160, settings.basic_font,
            settings.board_text_color
        )
        the_game.draw_text(
            f'{self.player_2}', the_game.screen, screen_rect.width / 2, 30,
            settings.medium_font, settings.board_text_color
        )
        the_game.draw_text(
            f"{self.player_2}'s", the_game.screen, 1070, 140,
            settings.basic_font, settings.board_text_color
        )
        the_game.draw_text(
            f"pairs:", the_game.screen, 1070, 160, settings.basic_font,
            settings.board_text_color
        )
        the_game.exit_button = shinsai_pygame.Button(
            the_game, "Quit (ESC)", settings.black, settings.red,
            coords=(1050, 50)
        )
        the_game.exit_button.draw_button()
        try:
            if the_game.card_select == True:
                the_game.draw_text(
                    f"Select a card - click twice to confirm.",
                    the_game.screen, screen_rect.width / 2, 590,
                    settings.small_font, settings.board_text_color
                )
        except:
            pass

        card_x = screen_rect.width / 2 - 70
        for card in the_game.deck:
            card = self.card_set.card_back[0]
            card.x = card_x
            card_x += 3
            card.y = screen_rect.height / 2 - 50
            card.blitme()

    def draw_hands(self):
        """Draw the hands on the board."""
        for i, card in enumerate(self.player_2.hand):
            card = self.card_set.card_back[0]
            card.x = i * 25 + 500
            card.y = 60
            card.blitme()
        for i, card in enumerate(self.player_1.hand):
            card.x = i * 25 + 500
            if not card.selected:
                card.y = 630
            else:
                card.y = 630 - 25
            if card.pressed and not card.selected:
                card.selected = True
                card.pressed = False
                self.card_selected(card)

            if card.pressed and card.selected:
                card.selected = False
                card.pressed = False
                card.confirmed = True
            card.blitme()
            if card in self.player_1.hand[0:-1]:
                card.button_rect = shinsai_pygame.Rect(
                card.rect.left, card.rect.top, 25, 112
            )
            else:
                card.button_rect = shinsai_pygame.Rect(
                card.rect.left, card.rect.top, 70, 112
            )

    def card_selected(self, card):
        """If a card is selected, the rest are not."""
        for c in self.player_1.hand:
            if c != card:
                c.selected = False

    def draw_tables(self):
        """Draw the pairs in the players table on the board."""
        card_even_y = card_odd_y = 200
        for i, card in enumerate(self.player_1.table):
            if i % 2 == 0:
                card.x = 50
                card.y = card_even_y
                card_even_y += 20
            else:
                card.x = 70
                card.y = card_odd_y
                card_odd_y += 20
            card.blitme()
        card_even_y = card_odd_y = 200
        for i, card in enumerate(self.player_2.table):
            if i % 2 == 0:
                card.x = 1050
                card.y = card_even_y
                card_even_y += 20
            else:
                card.x = 1070
                card.y = card_odd_y
                card_odd_y += 20
            card.blitme()

    def take_turn(self, player):
        """The main turn sequence."""
        hand_values = []
        self.check_for_pairs()
        self.draw_board_text(
            'Checking for pairs and placing on table.', player
        )

        for card in player.hand:
            # Get list of values of card in hand
            value = card.value
            hand_values.append(value)
        for card_val in player.wait_list[:]:
            # Remove cards from waitlist that are no longer in hand.
            if card_val not in hand_values:
                player.wait_list.remove(card_val)

        self.check_game_over()
        if the_game.game_over:
            return

        if not player.is_computer:
            chosen_value = self.choose_card_human(player, hand_values)
        else:
            chosen_value = self.choose_card_computer(player, hand_values)

        game_over = self.resolve_turn(player, chosen_value)
        if game_over:
            return
        if player.drew_match:
            player.drew_match = False
        else:
            the_game.turn = {player.opponent}


    def draw_board_text(self, text, player):
        """Draws text on the board."""
        the_game.draw_text(
            text, the_game.screen, screen_rect.width / 2,
            screen_rect.height / 2 - 100, settings.medium_font, settings.black
        )

        the_game.update_display()
        if not self.player_1.is_computer:
            the_game.pause_game(.75)
        self.update_screen()

    def check_game_over(self):
        """Checks if the game is over."""
        for player in self.players:
            if len(player.hand) == 0:
                the_game.screen.fill(settings.black)
                the_game.draw_text(
                    f'{player} has run out of cards!', the_game.screen,
                    screen_rect.width / 2, 100, settings.large_font,
                    settings.menu_text_color
                )
                the_game.draw_text(
                    f'{player} has {int(len(player.table) / 2)} pairs on the '
                    'table.', the_game.screen, screen_rect.width / 2, 150,
                    settings.medium_font, settings.menu_text_color
                )
                the_game.draw_text(
                    f'{player.opponent} has '
                    f'{int(len(player.opponent.table) / 2)} pairs on the '
                    'table.', the_game.screen, screen_rect.width / 2, 200,
                    settings.medium_font, settings.menu_text_color
                )
                the_game.draw_text(
                    f'After {the_game.round_num} rounds,', the_game.screen,
                    screen_rect.width / 2, 250, settings.medium_font,
                    settings.menu_text_color
                )
                the_game.game_over = True
                self.game_over(player)

    def game_over(self, player):
        """Actions to take if the game is over.
        If it's a tie, the win goes to the player who ran out of cards.
        Displays results and updates the tracking.
        """
        player_stats = tracking['player_stats'][f'{player}']
        opponent_stats = tracking['player_stats'][f'{player.opponent}']
        game_stats = tracking['game_stats']

        if len(player.table) >= len(player.opponent.table):
            if len(player.table) == len(player.opponent.table):
                the_game.draw_text(
                    f"it's a tie!", the_game.screen, screen_rect.width / 2,
                    300, settings.medium_font, settings.menu_text_color
                )
                the_game.draw_text(
                    f'{player} is the winner, as they went out first.',
                    the_game.screen, screen_rect.width / 2, 350,
                    settings.medium_font, settings.menu_text_color
                )
                game_stats['num_ties'] += 1
            else:
                the_game.draw_text(
                    f'{player} is the winner!', the_game.screen,
                    screen_rect.width / 2, 300, settings.medium_font,
                    settings.menu_text_color
                )
            player_stats[f'{player.opponent}'][0] += 1
            opponent_stats[f'{player}'][1] += 1
            player_stats['total_wins'] += 1
            opponent_stats['total_losses'] += 1
        else:
            the_game.draw_text(
                f'{player.opponent} is the winner!', the_game.screen,
                screen_rect.width / 2, 300, settings.medium_font,
                settings.menu_text_color
            )
            player_stats[f'{player.opponent}'][1] += 1
            opponent_stats[f'{player}'][0] += 1
            opponent_stats['total_wins'] += 1
            player_stats['total_losses'] += 1
        player_stats['total_games'] += 1
        opponent_stats['total_games'] += 1
        player_stats['total_rounds'] += the_game.round_num
        opponent_stats['total_rounds'] += the_game.round_num
        player_stats['total_pairs'] += int(len(player.table) / 2)
        opponent_stats['total_pairs'] += int(len(player.opponent.table) / 2)

        game_stats['total_games'] += 1
        game_stats['total_rounds'] += the_game.round_num
        the_game.write_to_tracking(settings.track_file, tracking)
        the_game.press_any_key(self.menu_sound)

    def choose_card_human(self, player, hand_values):
        """Prompt for a card to ask about for a human player."""
        if len(hand_values) == 1:
            # Automates play if a single card is left.
            chosen_value = hand_values[0]
            if chosen_value not in player.wait_list:
                player.wait_list.append(chosen_value)
        else:
            self.draw_board_text(
                f'Select a card to ask {player.opponent} about.', player
            )
            self.reset_card_state(player)
            the_game.card_select = True
            self.update_screen()
            while not the_game.card_confirmed:
                the_game.x = the_game.y = -5
                self.update_screen()
                the_game.wait_for_input()
                self.update_screen()
                for card in player.hand:
                    self.update_screen()
                    if card.confirmed == True:
                        self.update_screen()
                        the_game.card_confirmed = True
                        card.confirmed = False
                        chosen_value = card.value
                        break

        self.reset_card_state(player)
        self.update_screen()
        if chosen_value not in player.wait_list:
            player.wait_list.append(chosen_value)
        return chosen_value

    def reset_card_state(self, player):
        """Sets the card states back to initial."""
        the_game.card_select = False
        the_game.card_confirmed = False
        for card in player.hand:
            card.confirmed = False
            card.selected = False
            card.pressed = False

    def choose_card_computer(self, player, hand_values):
        """Choose card to ask about for a PC player."""
        chosen_value = ''
        if len(hand_values) == 1:
            chosen_value = hand_values[0]
            if chosen_value not in player.wait_list:
                player.wait_list.append(chosen_value)
        else:
            for val in hand_values:
                if val in player.opponent.wait_list:
                    # If the player has asked about value, selects it.
                    chosen_value = val
                    player.wait_list.append(chosen_value)
                    break
            if chosen_value == '':
                # If no card in the opponent wait list:
                choices = []
                for card in player.hand:
                    # Checks if computer has asked about value prior.
                    val = card.value
                    if val not in player.wait_list:
                        choices.append(val)
                if choices:
                    # Chooses from values not previously asked.
                    chosen_value = random.choice(choices)
                else:
                    # If none, chooses random card in hand.
                    chosen_value = random.choice(hand_values)
            if chosen_value not in player.wait_list:
                player.wait_list.append(chosen_value)
        return chosen_value

    def resolve_turn(self, player, chosen_value):
        """Resolve the turn."""
        for card in player.hand:
            # Translates chosen value to the card in the hand.
            if chosen_value == card.value:
                chosen_card = card
                break
        self.draw_board_text(
            f'{player.opponent}, do you have any {chosen_value}s?', player
        )

        for card in player.opponent.hand:
            if card.value == chosen_value:
                same_value = True
            else:
                same_value = False
            if same_value:
                self.draw_board_text(
                    f'{player.opponent} had the requested card!', player
                )
                player.table.append(chosen_card)
                player.table.append(card)
                player.hand.remove(chosen_card)
                player.opponent.hand.remove(card)
                player.wait_list.remove(chosen_value)
                self.check_game_over()
                if the_game.game_over:
                    return True
                break
        if not same_value:
            game_over = self.handle_go_fish(player, chosen_value)
            if game_over:
                return True
        return False

    def handle_go_fish(self, player, chosen_value):
        """Handle a go fish."""
        self.draw_board_text(f'{player.opponent} says "Go fish!"', player)
        new_card = self.the_deck.deal_top_card(the_game.deck)
        player.hand.append(new_card)
        if not player.is_computer:
            self.draw_board_text(
                f'{player} drew a {new_card} from the deck.', player
            )
        else:
            self.draw_board_text(
                f'{player} drew a card from the deck.', player
            )

        if self.check_for_pairs():
            self.draw_board_text(
                f'The new card matched a card in {player}\'s hand!', player
            )
            self.check_game_over()
            if the_game.game_over:
                return True
        if chosen_value == new_card.value:
            self.draw_board_text(
                f'The drawn card was a {chosen_value}!', player
            )
            self.draw_board_text(f"It is {player}'s turn again.", player)
            player.drew_match = True
            self.check_game_over()
            if the_game.game_over:
                return True
            player.wait_list.remove(chosen_value)
        return False

    def view_game_stats(self):
        """View the stats of the game in general."""
        game_stats = tracking['game_stats']
        total_games = game_stats["total_games"]

        the_game.screen.fill(settings.black)

        the_game.draw_text(
            'Game Stats', the_game.screen, screen_rect.width / 2, 100,
            settings.large_font, settings.menu_text_color
        )

        if total_games == 0:
            the_game.draw_large_center_text(
                'There have been no games played yet.',
                settings.menu_text_color
            )
        else:
            if total_games == 1:
                the_game.draw_text(
                    f'Out of 1 total game:', the_game.screen,
                    screen_rect.width / 2, 250, settings.basic_font,
                    settings.menu_text_color
                )
            else:
                the_game.draw_text(
                    f'Out of {total_games} total games:', the_game.screen,
                    screen_rect.width / 2, 250, settings.basic_font,
                    settings.menu_text_color
                )
            the_game.draw_text(
                f'There have been {game_stats["num_ties"]} tied games - '
                f'{round(game_stats["num_ties"] / total_games * 100, 2)}%',
                the_game.screen, screen_rect.width / 2, 300,
                settings.basic_font, settings.menu_text_color
            )
            the_game.draw_text(
                'The average number of rounds per game: '
                f'{round(game_stats["total_rounds"] / total_games, 2)}',
                the_game.screen, screen_rect.width / 2, 350,
                settings.basic_font, settings.menu_text_color
            )
        the_game.press_any_key(self.menu_sound)

    def view_player_stats(self):
        """View stats for each current player."""
        the_game.screen.fill(settings.black)

        self.player_1.y = 150
        self.player_2.y = 350

        for player in self.players:
            player_stats = tracking['player_stats'][f'{player}']
            total_games = player_stats['total_games']
            games_won = player_stats['total_wins']
            if not total_games:
                the_game.draw_text(
                    f'No stats for {player} - no games played.',
                    the_game.screen, screen_rect.width / 2, player.y + 50,
                    settings.basic_font, settings.menu_text_color
                )
                continue
            the_game.draw_text(
                f'Stats for {player}:', the_game.screen, screen_rect.width / 2,
                player.y, settings.medium_font, settings.menu_text_color
            )
            the_game.draw_text(
                '--------------------', the_game.screen, screen_rect.width / 2,
                player.y + 20, settings.medium_font, settings.menu_text_color
            )
            the_game.draw_text(
                f'Total games played - {total_games}', the_game.screen,
                screen_rect.width / 2, player.y + 50, settings.basic_font,
                settings.menu_text_color
            )
            try:
                the_game.draw_text(
                    f'Won {games_won} games - '
                    f'{round(games_won / total_games * 100, 2)}%',
                    the_game.screen, screen_rect.width / 2, player.y + 80,
                    settings.basic_font, settings.menu_text_color
                )
            except:
                the_game.draw_text(
                    f'Won 0 games - 0%', the_game.screen,
                    screen_rect.width / 2, player.y + 80, settings.basic_font,
                    settings.menu_text_color
                )
            the_game.draw_text(
                f'Average pairs per game: '
                f'{round(player_stats["total_pairs"] / total_games, 1)}',
                the_game.screen, screen_rect.width / 2, player.y + 110,
                settings.basic_font, settings.menu_text_color
            )
            the_game.draw_text(
                'The average number of rounds per game: '
                f'{round(player_stats["total_rounds"] / total_games, 1)}',
                the_game.screen, screen_rect.width / 2, player.y + 140,
                settings.basic_font, settings.menu_text_color
            )
        the_game.press_any_key(self.menu_sound)


if __name__ == '__main__':
    go_fish = GoFish()
    the_game = go_fish.the_game
    settings = the_game.settings
    screen_rect = the_game.screen_rect
    tracking = go_fish.tracking
    go_fish.run_game()