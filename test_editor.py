import unittest
from stack import Stack
from editor import TextEditor

class TestStack(unittest.TestCase):
    """Test cases for the Stack class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.stack = Stack()
    
    def test_is_empty(self):
        """Test that a new stack is empty."""
        self.assertTrue(self.stack.is_empty())
    
    def test_push_and_size(self):
        """Test pushing items and checking size."""
        self.stack.push(1)
        self.assertEqual(self.stack.size(), 1)
        self.stack.push(2)
        self.assertEqual(self.stack.size(), 2)
    
    def test_peek(self):
        """Test peeking at the top item."""
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.peek(), 2)
        # Ensure the item is still there
        self.assertEqual(self.stack.size(), 2)
    
    def test_pop(self):
        """Test popping items."""
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)
        self.assertTrue(self.stack.is_empty())
    
    def test_pop_empty(self):
        """Test popping from an empty stack raises IndexError."""
        with self.assertRaises(IndexError):
            self.stack.pop()
    
    def test_peek_empty(self):
        """Test peeking at an empty stack raises IndexError."""
        with self.assertRaises(IndexError):
            self.stack.peek()

class TestTextEditor(unittest.TestCase):
    """Test cases for the TextEditor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.editor = TextEditor()
    
    def test_initial_state(self):
        """Test initial state of the editor."""
        self.assertEqual(self.editor.get_content(), "")
        self.assertEqual(self.editor.get_history(), [])
    
    def test_write_valid(self):
        """Test writing valid text."""
        self.editor.write("Hello")
        self.assertEqual(self.editor.get_content(), "Hello")
        self.assertIn("Wrote: 'Hello'", self.editor.get_history())
    
    def test_write_empty(self):
        """Test writing empty text raises ValueError."""
        with self.assertRaises(ValueError):
            self.editor.write("")
    
    def test_delete_valid(self):
        """Test deleting valid number of characters."""
        self.editor.write("Hello World")
        self.editor.delete(5)
        self.assertEqual(self.editor.get_content(), "Hello ")
        self.assertIn("Deleted: 'World'", self.editor.get_history())
    
    def test_delete_too_many(self):
        """Test deleting more characters than available raises ValueError."""
        self.editor.write("Hi")
        with self.assertRaises(ValueError):
            self.editor.delete(3)
    
    def test_delete_negative(self):
        """Test deleting negative number of characters raises ValueError."""
        self.editor.write("Hi")
        with self.assertRaises(ValueError):
            self.editor.delete(-1)
    
    def test_undo_write(self):
        """Test undoing a write operation."""
        self.editor.write("Hello")
        self.editor.undo()
        self.assertEqual(self.editor.get_content(), "")
        # Check that the history records the undo
        history = self.editor.get_history()
        self.assertIn("Wrote: 'Hello'", history)
        self.assertIn("Undo write: deleted 'Hello'", history)
    
    def test_undo_delete(self):
        """Test undoing a delete operation."""
        self.editor.write("Hello World")
        self.editor.delete(5)  # Deletes "World"
        self.editor.undo()     # Should bring back "World"
        self.assertEqual(self.editor.get_content(), "Hello World")
        history = self.editor.get_history()
        self.assertIn("Wrote: 'Hello World'", history)
        self.assertIn("Deleted: 'World'", history)
        self.assertIn("Undo delete: inserted 'World'", history)
    
    def test_redo_write(self):
        """Test redoing a write operation after undo."""
        self.editor.write("Hello")
        self.editor.undo()     # Undo the write
        self.editor.redo()     # Redo the write
        self.assertEqual(self.editor.get_content(), "Hello")
        history = self.editor.get_history()
        self.assertIn("Wrote: 'Hello'", history)
        self.assertIn("Undo write: deleted 'Hello'", history)
        self.assertIn("Redo delete: inserted 'Hello'", history)
    
    def test_redo_delete(self):
        """Test redoing a delete operation after undo."""
        self.editor.write("Hello World")
        self.editor.delete(5)  # Delete "World"
        self.editor.undo()     # Undo the delete (brings back "World")
        self.editor.redo()     # Redo the delete (removes "World" again)
        self.assertEqual(self.editor.get_content(), "Hello ")
        history = self.editor.get_history()
        self.assertIn("Wrote: 'Hello World'", history)
        self.assertIn("Deleted: 'World'", history)
        self.assertIn("Undo delete: inserted 'World'", history)
        self.assertIn("Redo write: deleted 'World'", history)
    
    def test_undo_empty_stack(self):
        """Test undoing when the undo stack is empty raises IndexError."""
        with self.assertRaises(IndexError):
            self.editor.undo()
    
    def test_redo_empty_stack(self):
        """Test redoing when the redo stack is empty raises IndexError."""
        with self.assertRaises(IndexError):
            self.editor.redo()
    
    def test_new_action_clears_redo(self):
        """Test that performing a new action clears the redo stack."""
        self.editor.write("Hello")
        self.editor.undo()     # Now we can redo (hello is in redo stack)
        # Perform a new action - this should clear the redo stack
        self.editor.write(" ") 
        # After new action, redo should not be possible (redo stack cleared)
        with self.assertRaises(IndexError):
            self.editor.redo()
        # We should be able to undo the new action (the space)
        self.editor.undo()     # Undo the space
        self.assertEqual(self.editor.get_content(), "")
        # Redo should now be possible for the space (since we just undid it)
        self.editor.redo()     # Redo the space
        self.assertEqual(self.editor.get_content(), " ")
        # Undo the space again
        self.editor.undo()     # Undo the space
        self.assertEqual(self.editor.get_content(), "")

if __name__ == '__main__':
    unittest.main()