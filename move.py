"""
move.py

Card class for cards objects Script

Author: Chiriac Laura-Florina
Created: 24-12-2024
"""

class Move:
    def __init__(self, cards, from_stack, to_stack, stock_state=None, discard_state=None):
        """Initialize the move"""
        self.cards = cards
        self.from_stack = from_stack
        self.to_stack = to_stack
        self.stock_state = stock_state
        self.discard_state = discard_state
        # self.original_face_up_states = face_up_states
        self.positions = [card.position for card in cards]
        self.face_up_states = [card.face_up for card in cards]

        # Record the face_up state of the last card remaining in the from_stack (if any)
        if len(from_stack.cards) > len(cards):
            self.last_card_face_up_state = from_stack.cards[-len(cards) - 1].face_up
        else:
            self.last_card_face_up_state = None

        self.from_stack_face_up_state = [card.face_up for card in from_stack.cards]
        self.to_stack_face_up_state = [card.face_up for card in to_stack.cards]

    def __str__(self):
        """Return a string representation of the move"""
        card_names = ', '.join(str(card) for card in self.cards)
        return f"Move {card_names} from {self.from_stack} to {self.to_stack}"