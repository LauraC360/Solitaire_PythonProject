import unittest
from deck import Deck
from card import Card
from stack import Stack
from move import Move
from history_manager import HistoryManager

class TestDeckUndo(unittest.TestCase):
    def setUp(self):
        # Initialize a deck with mock data
        self.deck = Deck((0, 0), images={})
        self.deck.history_manager = HistoryManager()
        self.deck.stock_stack = Stack((0, 0), is_stock=True)
        self.deck.stacks = [Stack((0, 0)) for _ in range(9)]
        self.deck.stacks[7] = self.deck.stock_stack
        self.deck.stacks[8] = Stack((0, 0), is_discard=True)

        # Create mock cards
        self.card1 = Card(None, (100, 150), 'ace', 'spades')
        self.card2 = Card(None, (100, 150), '2', 'hearts')
        self.card3 = Card(None, (100, 150), '3', 'clubs')

        # Add cards to the stock stack
        self.deck.stock_stack.add_card(self.card1)
        self.deck.stock_stack.add_card(self.card2)
        self.deck.stock_stack.add_card(self.card3)

    def test_undo_move_from_stock_to_discard(self):
        # Simulate a move from stock to discard
        self.deck.check_for_stock_click((0, 0))
        self.assertEqual(len(self.deck.stacks[7].cards), 2)
        self.assertEqual(len(self.deck.stacks[8].cards), 1)

        # Undo the move
        self.deck.undo_last_move()
        self.assertEqual(len(self.deck.stacks[7].cards), 3)
        self.assertEqual(len(self.deck.stacks[8].cards), 0)

    def test_undo_reset_stock_stack(self):
        # Move all cards from stock to discard
        for _ in range(3):
            self.deck.check_for_stock_click((0, 0))
        self.assertEqual(len(self.deck.stacks[7].cards), 0)
        self.assertEqual(len(self.deck.stacks[8].cards), 3)

        # Reset the stock stack
        self.deck.check_for_stock_click((0, 0))
        self.assertEqual(len(self.deck.stacks[7].cards), 3)
        self.assertEqual(len(self.deck.stacks[8].cards), 0)

        # Undo the reset
        self.deck.undo_last_move()
        self.assertEqual(len(self.deck.stacks[7].cards), 0)
        self.assertEqual(len(self.deck.stacks[8].cards), 3)

if __name__ == '__main__':
    unittest.main()