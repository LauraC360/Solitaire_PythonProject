"""
move.py

Move class for handling moves in the Solitaire game.

Author: Chiriac Laura-Florina
Created: 08-12-2024
"""

class Move:
    """
    Class to retain the details of a move in the game, including the cards moved,
    the source stack, the destination stack, and the state changes involved.
    """

    def __init__(self, cards, from_stack, to_stack):
        """
        Initialize the Move object with details about the cards being moved and their origin/destination.

        Args:
            cards (list): The list of card objects being moved.
            from_stack (Stack): The stack from which the cards are moved.
            to_stack (Stack): The stack to which the cards are moved.
        """
        self.cards = cards  # List of cards being moved.
        self.from_stack = from_stack  # The stack from which the cards are moved.
        self.to_stack = to_stack  # The stack to which the cards are moved.

        # Record the original positions of the cards being moved
        self.positions = [card.position for card in cards]

        # Record the face-up states of the cards being moved
        self.face_up_states = [card.face_up for card in cards]

        # Record the face-up state of the last card remaining in the from_stack
        if len(from_stack.cards) > len(cards):
            self.last_card_face_up_state = from_stack.cards[-len(cards) - 1].face_up
        else:
            self.last_card_face_up_state = None

        # Record the face-up states of all cards in the from_stack
        self.from_stack_face_up_state = [card.face_up for card in from_stack.cards]

        # Record the face-up states of all cards in the to_stack
        self.to_stack_face_up_state = [card.face_up for card in to_stack.cards]

    def __str__(self):
        """
        Return a string representation of the move.

        Returns:
            str: A description of the move, including the cards and their source/destination stacks.
        """
        # Get the names of the cards being moved
        card_names = ', '.join(str(card) for card in self.cards)
        return f"Move {card_names} from {self.from_stack} to {self.to_stack}"

