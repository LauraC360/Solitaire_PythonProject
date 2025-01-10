"""
history_manager.py

Class for managing the history of moves in the Solitaire game.

Author: Chiriac Laura-Florina
Created: 24-12-2024
"""

class HistoryManager:
    """
    Class to manage the history of moves in the game.
    Allows recording moves, undoing the last move, and clearing history.
    """
    def __init__(self):
        """
        Initialize the HistoryManager with an empty history.
        """
        self.history = []  # List to store the history of moves.

    def record_move(self, move):
        """
        Record a move in the history.

        Args:
            move: A tuple or object representing the move to be recorded.
        """
        self.history.append(move)

    def undo_move(self):
        """
        Undo the last move by retrieving and removing it from the history.

        Returns:
            The last move in the history, or None if the history is empty.
        """
        if self.history:
            return self.history.pop()  # Remove and return the last move.
        return None  # No move to undo.

    def clear_history(self):
        """
        Clear all recorded history.
        Used when restarting the game.
        """
        self.history = []