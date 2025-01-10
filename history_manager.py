"""
history_manager.py

Card class for cards objects Script

Author: Chiriac Laura-Florina
Created: 24-12-2024
"""

class HistoryManager:
    def __init__(self):
        self.history = []

    def record_move(self, move):
        self.history.append(move)

    def undo_move(self):
        if self.history:
            return self.history.pop() # Return the last move in the history
        return None