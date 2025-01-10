"""
deck.py

Deck class for deck objects Script

Author: Chiriac Laura-Florina
Created: 25-12-2024
"""

# Standard Imports
import random
import logging

import pygame

# Local Imports
from history_manager import HistoryManager
from move import Move
from card import Card
from stack import Stack


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Deck(object):
    """Class to represent a deck object containing cards and stacks.

    Handles the creation of cards, shuffling, and managing stacks.

    Attributes:
        cards (list): A list of card objects in the deck.
        position (tuple): The (x, y) position of the deck on the screen.
        card_size (tuple): The dimensions (width, height) of the cards in the deck.
        images (dict): A dictionary of card images for each suit and rank.
        stacks (list): A list of stack objects representing the different card stacks.
        dragged_card (Card): The card currently being dragged.
        stock_stack (Stack): The stack representing the stock pile.
        dragged_cards (list): A list of cards currently being dragged.
        hint (str): A hint message for possible moves.
        highlight_start_time (int): The time when the highlight starts (for temporary hint highlight)
        history_manager (HistoryManager): An instance of the HistoryManager class for managing
    """

    def __init__(self, pos, images, card_size=(100, 150)):
        self.cards = []
        self.position = pos
        self.card_size = card_size
        self.images = images
        self.create_deck()
        self.stacks = []
        self.dragged_card = None
        self.stock_stack = None
        self.dragged_cards = None
        self.hint = None
        self.highlight_start_time = None
        self.history_manager = HistoryManager()

    def create_deck(self):
        """
        Create a standard 52-card deck and shuffle it.
        Each card has a suit, rank, and is initially face down.
        """
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

        for suit in suits:
            for rank in ranks:
                image = self.images[suit][rank]
                card = Card(image, self.card_size, rank, suit)
                self.cards.append(card)
        random.shuffle(self.cards)

    def setup_stacks(self, display_size):
        """
        Initialize the tableau, stock, discard, and foundation stacks.
        Distribute cards to tableau stacks and prepare for the game.
        """
        display_width, display_height = display_size
        stack_spacing = 50

        start_x = 200
        start_y = self.card_size[1] + 100

        # Sets the foundation stack in the place where it needs to be
        foundation_stack_step = self.card_size[0] + stack_spacing
        foundation_start_y = 50

        # Create the stacks
        stack1 = Stack((start_x, start_y))
        stack2 = Stack((start_x + self.card_size[0] + stack_spacing, start_y))
        stack3 = Stack((start_x + (self.card_size[0] + stack_spacing) * 2, start_y))
        stack4 = Stack((start_x + (self.card_size[0] + stack_spacing) * 3, start_y))
        stack5 = Stack((start_x + (self.card_size[0] + stack_spacing) * 4, start_y))
        stack6 = Stack((start_x + (self.card_size[0] + stack_spacing) * 5, start_y))
        stack7 = Stack((start_x + (self.card_size[0] + stack_spacing) * 6, start_y))

        self.stock_stack = Stack((start_x, stack_spacing), is_stock=True)
        discard_stack = Stack((start_x + self.card_size[0] + stack_spacing, stack_spacing), is_discard=True)

        # Foundation stacks
        foundation_stack1 = Stack((650, foundation_start_y), is_foundation=True)
        foundation_stack2 = Stack((650 + foundation_stack_step, foundation_start_y), is_foundation=True)
        foundation_stack3 = Stack((650 + foundation_stack_step * 2, foundation_start_y), is_foundation=True)
        foundation_stack4 = Stack((650 + foundation_stack_step * 3, foundation_start_y), is_foundation=True)

        # Add all stacks created from the cards
        self.stacks = [stack1, stack2, stack3, stack4, stack5, stack6, stack7,
                       self.stock_stack, discard_stack,
                       foundation_stack1, foundation_stack2, foundation_stack3, foundation_stack4]

        # Distribute cards to the stacks 1-7
        for i, stack in enumerate(self.stacks[:7]):
            for j in range(i + 1):
                card = self.cards.pop()
                card.face_up = (j == i)
                stack.add_card(card)
        # Add the rest of the cards to the stock stack
        self.stock_stack = self.stacks[7]
        while self.cards:
            card = self.cards.pop()
            card.face_up = False
            self.stock_stack.add_card(card)

    def reset_all(self, display_size):
        """Reset the game by reinitializing the deck and stacks"""
        self.create_deck()  # Recreate the deck
        self.setup_stacks(display_size)  # Reinitialize the stacks
        self.history_manager.clear_history()  # Clear the move history

    def check_win(self):
        """Check if all foundation stacks are complete

        Returns:
            bool: True if all foundations are complete, False otherwise.
        """
        for stack in self.stacks[9:]:
            if len(stack.cards) != 13:  # Assuming each foundation stack should have 13 cards
                return False
        return True

    def show_hint(self):
        """Show a hint for possible moves"""
        self.hint = None  # Reset hint message
        logging.debug("Resetting hint message")

        # Clear all highlights
        for stack in self.stacks:
            stack.highlight = False
            for card in stack.cards:
                card.highlight = False

        suggested_cards = set()  # Keep track of suggestions to only show one
        highlighted_pairs = []  # List to keep track of highlighted pairs

        for stack in self.stacks:
            logging.debug(f"Checking stack: {stack}")
            if stack.is_foundation:
                continue
            for card in stack.cards:
                logging.debug(f"Checking card: {card.rank} of {card.suit}, face_up: {card.face_up}")
                if card.face_up and (card.rank, card.suit) not in suggested_cards:
                    for target_stack in self.stacks:
                        # Skip if the target stack is the same as the current stack or if the target stack is empty
                        if target_stack == stack or not target_stack.cards:
                            continue
                        logging.debug(f"Checking if the hint is redundant")

                        logging.debug(f"Checking if card can be added to target stack: {target_stack}")

                        if target_stack.can_add_card(card):
                            # Highlight the card and the target stack
                            card.highlight = True
                            if target_stack.cards:
                                target_stack.cards[-1].highlight = True  # Highlight the front card of the target stack
                                highlighted_pairs.append((card, target_stack.cards[-1]))
                            else:
                                target_stack.highlight = True  # Highlight the empty stack
                                highlighted_pairs.append((card, target_stack))
                            logging.debug(f"Hint found: {card.rank} of {card.suit} can be moved to target stack")
                            self.highlight_start_time = pygame.time.get_ticks()  # Set the highlight start time
                            if len(highlighted_pairs) >= 1:
                                return

        # If no moves are found, suggest clicking the stock stack
        if self.stock_stack.cards:
            self.stock_stack.cards[-1].highlight = True
        self.stock_stack.highlight = True


        self.hint = "No other moves available. Try clicking the stock stack."
        self.highlight_start_time = pygame.time.get_ticks()
        logging.debug("No moves found. Suggest clicking the stock stack.")

    def draw(self, screen):
        """Draw the card deck and stacks on the screen

        Args:
            screen (pygame.Surface): The surface to draw the deck on.
        """
        for stack in self.stacks:
            stack.draw(screen) # Draw each stack

        # Draw the dragged cards on top, if any
        if self.dragged_cards:
            for card in self.dragged_cards:
                screen.blit(
                    card.image if card.face_up else card.back_image,
                    card.position
                )

        # Draw hint highlights, if any
        if self.highlight_start_time:
            elapsed_time = pygame.time.get_ticks() - self.highlight_start_time
            if elapsed_time > 2000:  # 2 seconds
                for stack in self.stacks:
                    for card in stack.cards:
                        card.highlight = False
                self.highlight_start_time = None  # Reset the highlight start time
            else:
                for stack in self.stacks:
                    if stack.cards:
                        front_card = stack.cards[-1]
                        if front_card.highlight:
                            highlight_rect = pygame.Rect(front_card.position, (
                                front_card.image.get_width(), front_card.image.get_height()))
                            pygame.draw.rect(screen, (0, 0, 255), highlight_rect, 4)
                    if stack.highlight:
                        highlight_rect = pygame.Rect(stack.position, (self.card_size[0], self.card_size[1]))
                        pygame.draw.rect(screen, (0, 0, 255), highlight_rect, 4)
                # Highlight the stock stack if it is highlighted
                if self.stock_stack.highlight:
                    if self.stock_stack.cards:
                        front_card = self.stock_stack.cards[-1]
                        highlight_rect = pygame.Rect(front_card.position,
                                                     (front_card.image.get_width(), front_card.image.get_height()))
                    else:
                        highlight_rect = pygame.Rect(self.stock_stack.position, (self.card_size[0], self.card_size[1]))
                    pygame.draw.rect(screen, (255, 0, 0), highlight_rect, 4)

    def undo_last_move(self):
        """
        Undo the last move
        Handles moves between tableau, stock, discard, and foundation stacks.
        """
        logging.debug('Attempting to undo the last move')
        move = self.history_manager.undo_move()
        if move:
            logging.debug(f'Undoing move: {move}')
            move.to_stack.remove_cards(move.cards)
            for card, position in zip(move.cards, move.positions):
                card.stack = move.from_stack
                card.face_up = True
                card.position = position
                move.from_stack.add_card(card)

            # Restore the face_up state if needed
            remaining_cards_in_from_stack = len(move.from_stack.cards) - len(move.cards)
            if move.last_card_face_up_state is not None and len(move.from_stack.cards) > len(move.cards):
                last_card_index = -len(move.cards) - 1
                last_card = move.from_stack.cards[last_card_index]
                last_card.face_up = move.from_stack_face_up_state[remaining_cards_in_from_stack - 1]

            # Make sure cards in the stock stack are face down
            for card in self.stacks[7].cards:
                card.face_up = False

            # Make sure cards in the foundation stack are face up
            for stack in self.stacks[9:]:
                for card in stack.cards:
                    card.face_up = True

            # Make sure cards in the discard stack are face up
            for card in self.stacks[8].cards:
                card.face_up = True

            # Redraw the screen to update the visual representation
            #self.draw(pygame.display.get_surface())
            logging.debug('Move undone successfully')

        else:
            logging.debug('No moves to undo')

    def stop_dragging(self):
        """Stop dragging the cards"""
        for stack in self.stacks:
            if stack.contains_card(self.dragged_cards[0]) and stack.can_add_card(self.dragged_cards[0]):
                # Record the move
                move = Move(
                    self.dragged_cards,
                    self.dragged_cards[0].original_stack,
                    stack
                )
                self.history_manager.record_move(move)

                # Move the cards to the new stack
                for card in self.dragged_cards:
                    stack.add_card(card)
                if self.dragged_cards[0].original_stack.cards:
                    self.dragged_cards[0].original_stack.cards[-1].face_up = True
                return

        # If no valid stack, return to the original stack
        for card in self.dragged_cards:
            card.position = card.original_stack.get_next_card_position()
            card.original_stack.add_card(card)

    def check_for_stock_click(self, mouse_position):
        """Check if the stock stack was clicked"""
        stock_stack = self.stacks[7]
        discard_stack = self.stacks[8]
        if stock_stack.cards and stock_stack.cards[-1].check_if_clicked(mouse_position):
            # Record the state of the stock and discard stacks
            move = Move(
                [stock_stack.cards[-1]],
                stock_stack,
                discard_stack
            )
            self.history_manager.record_move(move)

            # Move the top card from the stock stack to the discard stack
            card = stock_stack.remove_card(stock_stack.cards[-1])
            card.face_up = True
            discard_stack.add_card(card)
        elif not stock_stack.cards:
            # Record the stock reset as a move
            move = Move(
                discard_stack.cards.copy(),
                discard_stack,
                stock_stack
            )
            self.history_manager.record_move(move)

            # Reset the stock stack when empty
            while discard_stack.cards:
                card = discard_stack.remove_card(discard_stack.cards[-1])
                card.face_up = False
                stock_stack.add_card(card)