"""
card.py

Card class for cards objects Script

Author: Chiriac Laura-Florina
Created: 24-12-2024
"""

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

        # Assign the color of the card
        if self.suit == 'diamonds' or self.suit == 'hearts':
            self.color = 'red'
        elif self.suit == 'spades' or self.suit == 'clubs':
            self.color = 'black'

    def start_drag(self):
        """Start dragging the card action from player"""
        self.dragging = True

    def stop_drag(self):
        """Stop dragging the card action from player"""
        self.dragging = False

    def update_position(self, mouse_position):
        """Update the position of the card while dragging"""
        if self.dragging:
            self.position = (mouse_position[0] - self.card_size[0] // 2, mouse_position[1] - self.card_size[1] // 2)

    def check_if_clicked(self, mouse_position):
        """Check if the card is clicked by the player"""
        width, height = self.card_size
        mouse_x, mouse_y = mouse_position

        if self.position[0] < mouse_x < self.position[0] + width and self.position[1] < mouse_y < self.position[1] + height:
            return True
        else:
            return False

    def __str__(self):
        """Return the string representation of the card"""
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        """Return the string representation of the card"""
        return self.__str__()