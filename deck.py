"""
deck.py

Deck class for deck objects Script

Author: Chiriac Laura-Florina
Created: 25-12-2024
"""

import pygame
import random
from card import Card
from stack import Stack
from collections import namedtuple


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

        # Draw the dragged card on top, if any
        if self.dragged_card:
            screen.blit(
                self.dragged_card.image if self.dragged_card.face_up else self.dragged_card.back_image,
                self.dragged_card.position
            )

    def stop_dragging(self, mouse_position):
        """Stop dragging the card"""
        for stack in self.stacks:
            if stack.contains_card(self.dragged_card) and stack.can_add_card(self.dragged_card):
                stack.add_card(self.dragged_card)
                if self.dragged_card.original_stack.cards:
                    self.dragged_card.original_stack.cards[-1].face_up = True
                return

        # If no valid stack, return to the original stack
        self.dragged_card.position = self.dragged_card.original_stack.get_next_card_position()
        self.dragged_card.original_stack.add_card(self.dragged_card)

    def check_for_stock_click(self, mouse_position):
        """Check if the stock stack was clicked"""
        stock_stack = self.stacks[7]
        discard_stack = self.stacks[8]
        if stock_stack.cards and stock_stack.cards[-1].check_if_clicked(mouse_position):
            card = stock_stack.remove_card(stock_stack.cards[-1])
            card.face_up = True
            discard_stack.add_card(card)
        elif not stock_stack.cards:
            # Reset the stock stack when empty
            while discard_stack.cards:
                card = discard_stack.remove_card(discard_stack.cards[-1])
                card.face_up = False
                stock_stack.add_card(card)