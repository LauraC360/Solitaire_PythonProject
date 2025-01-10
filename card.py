"""
card.py

Card class for card objects.

This script defines the `Card` class, which represents individual playing cards
used in the game. It handles attributes such as rank, suit, position, and graphical
representation, as well as interactions like dragging and clicking.

Author: Chiriac Laura-Florina
Created: 24-12-2024
"""

import pygame

class Card:
    """Class to represent a card object.

    Attributes:
        image (pygame.Surface): The front image of the card.
        card_size (tuple): The dimensions (width, height) of the card.
        rank (str): The rank of the card ('Ace', '2', 'King', etc.).
        suit (str): The suit of the card ('diamonds', 'hearts', 'clubs', 'spades').
        position (tuple): The (x, y) position of the card on the screen.
        face_up (bool): Whether the card is face-up or face-down.
        dragging (bool): Indicate if the card is currently being dragged.
        offset (tuple): The offset between the mouse position and the card's position during drag-and-drop.
        original_stack (list): The original stack for the card before dragging.
        stack (list): The current stack of cards the card belongs to.
        highlight (bool): Whether the card is highlighted.
        color (str): The color of the card ('red' for hearts/diamonds, 'black' for clubs/spades).
        back_image (pygame.Surface): The back image of the card.
    """

    def __init__(self, image, card_size, rank, suit, position=(0, 0), face_up=False):
        """Initialize a card object.

        Args:
            image (pygame.Surface): The front image of the card.
            card_size (tuple): The dimensions (width, height) of the card.
            rank (str): The rank of the card (e.g., 'Ace', '2', 'King').
            suit (str): The suit of the card ('diamonds', 'hearts', 'clubs', 'spades').
            position (tuple): The (x, y) position of the card on the screen.
            face_up (bool): Whether the card is face-up or face-down (default: False).
        """
        self.image = image
        self.card_size = card_size
        self.suit = suit
        self.rank = rank
        self.position = position
        self.face_up = face_up
        self.dragging = False
        self.offset = (0, 0)
        self.original_stack = None  # Track the original stack
        self.stack = None  # Track the current stack
        self.highlight = False

        # Assign the color of the card
        if self.suit in ['diamonds', 'hearts']:
            self.color = 'red'
        else:
            self.color = 'black'

        self.back_image = pygame.image.load('resources/images/cards/card_back.png')
        self.back_image = pygame.transform.scale(self.back_image, self.card_size)

    def start_drag(self, mouse_position):
        """Start dragging the card.

        Args:
            mouse_position (tuple): The (x, y) position of the mouse when dragging starts.
        """
        self.dragging = True
        self.offset = (mouse_position[0] - self.position[0], mouse_position[1] - self.position[1])
        self.original_stack = self.stack

    def stop_drag(self):
        """Stop dragging the card."""
        self.dragging = False
        self.offset = (0, 0)

    def update_position(self, mouse_position):
        """Update the position of the card while dragging.

        Args:
            mouse_position (tuple): The current (x, y) position of the mouse.
        """
        if self.dragging:
            self.position = (mouse_position[0] - self.offset[0], mouse_position[1] - self.offset[1])

    def check_if_clicked(self, mouse_position):
        """Check if the card is clicked by the player.

        Args:
            mouse_position (tuple): The (x, y) position of the mouse click.

        Returns:
            bool: True if the card is clicked, False otherwise.
        """
        card_rect = pygame.Rect(self.position, self.card_size)
        return card_rect.collidepoint(mouse_position)

    def get_draggable_stack(self):
        """Get all face-up cards in the stack starting from this card.

        Returns:
            self.stack.cards[index:] (list): A list of face-up cards in the stack.

        Raises:
            ValueError: If the card is not part of a stack.
        """
        if not self.face_up:
            return []
        if self.stack is None:
            raise ValueError("Card is not in a stack")
        index = self.stack.cards.index(self)
        return self.stack.cards[index:]

    def __str__(self):
        """Return the string representation of the card.

        Returns:
            str: A string in the format 'Rank of Suit'.
        """
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        """Return the detailed string representation of the card.

        Returns:
            str: A string in the format 'Rank of Suit'.
        """
        return self.__str__()