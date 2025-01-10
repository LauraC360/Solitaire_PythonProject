"""
deck.py

Deck class for deck objects Script

Author: Chiriac Laura-Florina
Created: 25-12-2024
"""
from math import remainder

import pygame
import random
from history_manager import HistoryManager
from move import Move
from card import Card
from stack import Stack
from collections import namedtuple
import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Deck(object):
    """Class to represent a deck object"""

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
        self.history_manager = HistoryManager()

    def create_deck(self):
        """Create a deck of cards"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

        for suit in suits:
            for rank in ranks:
                image = self.images[suit][rank]
                card = Card(image, self.card_size, rank, suit)
                self.cards.append(card)
        random.shuffle(self.cards)

    def setup_stacks(self, display_size):
        """Initialize the stacks of cards"""
        display_width, display_height = display_size
        stack_spacing = 50

        start_x = 200
        start_y = self.card_size[1] + 100

        # Set the foundation stack in the place where I need it to be
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

    def draw(self, screen):
        """Draw the card deck and stacks on the screen"""
        for stack in self.stacks:
            stack.draw(screen)

        # Draw the dragged cards on top, if any
        if self.dragged_cards:
            for card in self.dragged_cards:
                screen.blit(
                    card.image if card.face_up else card.back_image,
                    card.position
                )

    def undo_last_move(self):
        """Undo the last move"""
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

            # Restore the stock and discard stacks
            #self.stacks[7].cards = move.stock_state
            #self.stacks[8].cards = move.discard_state

            # Ensure cards in the stock stack are face down
            for card in self.stacks[7].cards:
                card.face_up = False
            # Ensure cards in the foundation stack are face up
            for stack in self.stacks[9:]:
                for card in stack.cards:
                    card.face_up = True

            # Ensure cards in the discard stack are face up
            for card in self.stacks[8].cards:
                card.face_up = True

            # Redraw the screen to update the visual representation
            #self.draw(pygame.display.get_surface())
            logging.debug('Move undone successfully')

        # Ensure the last card in the stack is face down if it was like that before the move
        # if move.from_stack.cards:
        #     move.from_stack.cards[-2].face_up = False
        #     logging.debug('Move undone successfully')
        else:
            logging.debug('No moves to undo')
            # move.from_stack.add_card(move.cards)
            # move.card.position = move.from_stack.get_next_card_position()

    def stop_dragging(self, mouse_position):
        """Stop dragging the cards"""
        for stack in self.stacks:
            if stack.contains_card(self.dragged_cards[0]) and stack.can_add_card(self.dragged_cards[0]):
                #move = Move(self.dragged_cards, self.dragged_cards[0].original_stack, stack)
                move = Move(
                    self.dragged_cards,
                    self.dragged_cards[0].original_stack,
                    stack,
                    self.stock_stack.cards.copy(),
                    self.stacks[8].cards.copy()
                )
                self.history_manager.record_move(move)

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
                discard_stack,
                self.stock_stack.cards.copy(),
                self.stacks[8].cards.copy()
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
                stock_stack,
                self.stock_stack.cards.copy(),
                self.stacks[8].cards.copy()
            )
            self.history_manager.record_move(move)

            # Reset the stock stack when empty
            while discard_stack.cards:
                card = discard_stack.remove_card(discard_stack.cards[-1])
                card.face_up = False
                stock_stack.add_card(card)