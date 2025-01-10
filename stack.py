"""
stack.py

Stack class for handling stacks of cards Script

Author: Chiriac Laura-Florina
Created: 24-12-2024
"""

import pygame
from card import Card

import pygame
from card import Card
import logging

from history_manager import HistoryManager

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Stack:
    """Class to represent a stack of cards"""
    def __init__(self, position, is_stock=False, is_discard=False, is_foundation=False):
        self.cards = []
        self.position = position
        self.is_stock = is_stock
        self.is_discard = is_discard
        self.is_foundation = is_foundation
        if is_stock:
            self.deck = 'stock'
        elif is_discard:
            self.deck = 'discard'
        elif is_foundation:
            self.deck = 'foundation'
        else:
            self.deck = 'tableau'
        self.highlight = True # Highlight attribute for valid drop zones
        self.rect = pygame.Rect(position, (100, 150))  # Add rect attribute

    def contains_card(self, card):
        """Check if a card is within the stack's bounding box"""
        stack_rect = pygame.Rect(self.position, (100, 150))
        card_rect = pygame.Rect(card.position, card.card_size)
        return stack_rect.colliderect(card_rect)

    def add_card(self, card):
        """Add a card to the stack"""
        logging.debug(f'Adding card {card.rank} of {card.suit} to stack at position {self.position} with is_discard = {self.is_discard}')
        if self.is_discard or self.is_foundation:
            card.position = self.position
            card.face_up = True
            card.draggable = True
        else:
            card.position = self.get_next_card_position()
        self.cards.append(card)
        card.stack = self # Set the current stack
        #if card.original_stack is None:
        #    card.original_stack = self # Set the original stack
        #self.draw(pygame.display.get_surface()) # Physically update the stack

    # def remove_card(self, card):
    #     """Remove a card from the stack"""
    #     if card in self.cards:
    #         self.cards.remove(card)
    #         # if self.cards:
    #         #     self.cards[-1].face_up = True
    #         return card

    def remove_card(self, card):
        """Remove a card from the stack"""
        if card in self.cards:
            self.cards.remove(card)
            card.stack = None
        return card
        #return self.cards.pop()

    def remove_cards(self, cards):
        """Remove multiple cards from the stack"""
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)
                card.stack = None
        return cards

    # def get_next_card_position(self):
    #     """Get the position of the next card in the stack"""
    #     if self.cards:
    #         top_card = self.cards[-1]
    #         return top_card.position[0], top_card.position[1] + 20  # Example offset
    #     return self.position

    def get_next_card_position(self):
        if self.is_stock:
            return self.position
        else:
            return self.position[0], self.position[1] + len(self.cards) * 30

    def draw(self, screen):
        """Draw the stack of cards on the screen"""
        if self.highlight:
            pygame.draw.rect(screen, (0, 255, 0), (*self.position, 100, 150), 5)  # Green border for valid drop
        if self.cards:
            if self.is_stock:
                for card in self.cards:
                    screen.blit(card.back_image, card.position)
            elif self.is_discard or self.is_foundation:
                # Draw only the top card face up for the discard stack
                top_card = self.cards[-1]
                screen.blit(top_card.image, top_card.position)
                #for card in self.cards:
                    #screen.blit(card.back_image, card.position)
            else:
                for card in self.cards:
                    screen.blit(card.image if card.face_up else card.back_image, card.position)
        else:
            # Placeholder for empty stack
            pygame.draw.rect(screen, (200, 200, 200), (*self.position, 100, 150), 2)

    def can_add_card(self, card):
        """Check if a card can be added to the stack (tableau or foundation)"""
        rank_mapping = {
            'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13
        }

        # Stock-specific rules
        if self.is_stock or self.is_discard:
            return False

        # Foundation-specific rules
        if self.is_foundation:
            if not self.cards:
                return card.rank == 'ace'  # Only Aces can be placed on empty foundation stacks
            top_card = self.cards[-1]
            return (card.suit == top_card.suit) and (rank_mapping[card.rank] == rank_mapping[top_card.rank] + 1)

        # Tableau-specific rules
        if not self.cards:
            return card.rank == 'king'  # Only Kings can be placed on empty tableau stacks
        top_card = self.cards[-1]
        return card.color != top_card.color and rank_mapping[card.rank] == rank_mapping[top_card.rank] - 1