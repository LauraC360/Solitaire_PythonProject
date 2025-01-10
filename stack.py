"""
stack.py

Stack class for handling stacks of cards in a Solitaire game.

Author: Chiriac Laura-Florina
Created: 24-12-2024
"""

# Imports
import pygame
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Stack:
    """Class to represent a stack of cards in a Solitaire game."""

    def __init__(self, position, is_stock=False, is_discard=False, is_foundation=False):
        """
        Initialize the stack with its position and type (stock, discard, foundation, or tableau).

        Args:
            position (tuple): The (x, y) coordinates of the stack's position on the screen.
            is_stock (bool): Flag indicating if this stack is the stock pile (default is False).
            is_discard (bool): Flag indicating if this stack is the discard pile (default is False).
            is_foundation (bool): Flag indicating if this stack is a foundation pile (default is False).
        """
        self.cards = []  # List to hold the cards in the stack
        self.position = position  # Position of the stack on the screen
        self.is_stock = is_stock  # Flag to indicate if this is a stock pile
        self.is_discard = is_discard  # Flag to indicate if this is a discard pile
        self.is_foundation = is_foundation  # Flag to indicate if this is a foundation pile

        # Determine the deck type based on the flags.
        if is_stock:
            self.deck = 'stock'
        elif is_discard:
            self.deck = 'discard'
        elif is_foundation:
            self.deck = 'foundation'
        else:
            self.deck = 'tableau'

        self.highlight = None  # Highlight attribute for valid drop zones
        self.rect = pygame.Rect(position, (100, 150))  # Rectangular area representing the stack's position

    def contains_card(self, card):
        """
        Check if a card is within the stack's zone

        Args:
            card (Card): The card to check for presence in the stack.

        Returns:
            bool: True if the card is within the stack's bounding box, False otherwise.
        """
        stack_rect = pygame.Rect(self.position, (100, 150))  # Create the stack's rectangle
        card_rect = pygame.Rect(card.position, card.card_size)  # Create the card's rectangle
        return stack_rect.colliderect(card_rect)  # Check if the rectangles intersect

    def add_card(self, card):
        """
        Add a card to the stack.

        Args:
            card (Card): The card to add to the stack.
        """
        logging.debug(
            f'Adding card {card.rank} of {card.suit} to stack at position {self.position} with is_discard = {self.is_discard}')

        # Update card properties based on the type of stack
        if self.is_discard or self.is_foundation:
            card.position = self.position  # Place the card at the stack's position
            card.face_up = True  # Set the card face up for discard or foundation stacks
            card.draggable = True  # Allow the card to be dragged
        else:
            card.position = self.get_next_card_position()  # Set the card position for tableau stacks

        self.cards.append(card)  # Add the card to the stack
        card.stack = self  # Set the stack to which the card belongs

    def remove_card(self, card):
        """
        Remove a card from the stack.

        Args:
            card (Card): The card to remove from the stack.

        Returns:
            Card: The card that was removed.
        """
        if card in self.cards:
            self.cards.remove(card)  # Remove the card from the stack.
            card.stack = None  # Set the stack attribute of the card to None.
        return card

    def remove_cards(self, cards):
        """
        Remove multiple cards from the stack.

        Args:
            cards (list): A list of cards to remove from the stack.

        Returns:
            list: The list of cards that were removed.
        """
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)  # Remove each card from the stack.
                card.stack = None  # Set the stack attribute of each card to None.
        return cards

    def get_next_card_position(self):
        """
        Get the position for the next card in the stack.

        Returns:
            tuple: The (x, y) coordinates for the next card's position.
        """
        if self.is_stock:
            return self.position  # Stock cards have a fixed position.
        else:
            # For tableau, offset the y-coordinate based on the number of cards in the stack.
            return self.position[0], self.position[1] + len(self.cards) * 30

    def draw(self, screen):
        """
        Draw the stack of cards on the screen.

        Args:
            screen (pygame.Surface): The surface on which to draw the stack.
        """
        if self.cards:
            if self.is_stock:
                for card in self.cards:
                    screen.blit(card.back_image, card.position)  # Draw the back image for stock cards.
            elif self.is_discard or self.is_foundation:
                # For discard or foundation stacks, draw only the top card face-up.
                top_card = self.cards[-1]
                screen.blit(top_card.image, top_card.position)
            else:
                for card in self.cards:
                    # Draw each card face-up or face-down depending on its state.
                    screen.blit(card.image if card.face_up else card.back_image, card.position)
        else:
            # Draw an empty placeholder for the stack.
            pygame.draw.rect(screen, (200, 200, 200), (*self.position, 100, 150), 2)

    def can_add_card(self, card):
        """
        Check if a card can be added to the stack based on its type and the rules of Solitaire.

        Args:
            card (Card): The card to check if it can be added to the stack.

        Returns:
            bool: True if the card can be added to the stack, False otherwise.
        """
        rank_mapping = {
            'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13
        }

        # Stock and discard stacks cannot accept new cards
        if self.is_stock or self.is_discard:
            return False

        # Foundation stacks accept cards of the same suit and one rank higher than the top card
        if self.is_foundation:
            if not self.cards:
                return card.rank == 'ace'  # Only Aces can be placed on an empty foundation stack
            top_card = self.cards[-1]
            return (card.suit == top_card.suit) and (rank_mapping[card.rank] == rank_mapping[top_card.rank] + 1)

        # Tableau stacks accept cards of alternating colors and one rank lower than the top card
        if not self.cards:
            return card.rank == 'king'  # Only Kings can be placed on an empty tableau stack.
        top_card = self.cards[-1]
        return card.color != top_card.color and rank_mapping[card.rank] == rank_mapping[top_card.rank] - 1