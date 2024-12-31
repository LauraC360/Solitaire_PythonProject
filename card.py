"""
card.py

Card class for cards objects Script

Author: Chiriac Laura-Florina
Created: 24-12-2024
"""

import pygame

class Card(object):
    """Class to represent a card object"""
    def __init__(self, image, card_size, rank, suit, position=(0,0), face_up=False):
        self.image = image
        self.card_size = card_size
        self.suit = suit
        self.rank = rank
        self.position = position
        self.face_up = face_up
        self.dragging = False
        self.offset = (0, 0)
        self.original_stack = None  # Track the original stack
        self.stack = None # Track the current stack
        #self.original_holder = None

        # Assign the color of the card
        if self.suit in ['diamonds', 'hearts']:
            self.color = 'red'
        else:
            self.color = 'black'

        self.back_image = pygame.image.load('resources/images/cards/card_back.png')
        self.back_image = pygame.transform.scale(self.back_image, self.card_size)

    def start_drag(self, mouse_position):
        """Start dragging the card"""
        self.dragging = True
        self.offset = (mouse_position[0] - self.position[0], mouse_position[1] - self.position[1])
        self.original_stack = self.stack

    def stop_drag(self):
        """Stop dragging the card"""
        self.dragging = False
        self.offset = (0, 0)

    def update_position(self, mouse_position):
        """Update the position of the card"""
        if self.dragging:
            self.position = (mouse_position[0] - self.offset[0], mouse_position[1] - self.offset[1])

    def check_if_clicked(self, mouse_position):
        """Check if the card is clicked by the player"""
        card_rect = pygame.Rect(self.position, self.card_size)
        return card_rect.collidepoint(mouse_position)

    def get_draggable_stack(self):
        """Get all face-up cards in the stack starting from this card"""
        if not self.face_up:
            return []
        index = self.stack.cards.index(self)
        return self.stack.cards[index:]

    def __str__(self):
        """Return the string representation of the card"""
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        """Return the string representation of the card"""
        return self.__str__()