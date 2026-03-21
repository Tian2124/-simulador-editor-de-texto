from stack import Stack

class TextEditor:
    """A text editor with undo/redo functionality using stacks."""
    
    def __init__(self):
        """Initialize the text editor with empty state."""
        self._current_text = ""
        self._undo_stack = Stack()
        self._redo_stack = Stack()
        self._history = []  # Simple list of descriptive action strings
    
    def write(self, text):
        """Write text to the editor.
        
        Args:
            text (str): The text to write.
            
        Raises:
            ValueError: If text is empty.
        """
        if not text:
            raise ValueError("Cannot write empty text")
        
        # Save current state for undo (we need to know what to delete)
        self._undo_stack.push(("delete", len(text)))
        # Clear redo stack when new action is performed
        self._redo_stack = Stack()
        # Update current text
        self._current_text += text
        # Record in history
        self._history.append(f"Wrote: '{text}'")
    
    def delete(self, n):
        """Delete the last n characters from the editor.
        
        Args:
            n (int): Number of characters to delete.
            
        Raises:
            ValueError: If n is negative or greater than current text length.
        """
        if n < 0:
            raise ValueError("Cannot delete negative number of characters")
        if n == 0:
            # No-op: avoid Python slicing edge case with -0 clearing the whole string.
            self._history.append("Deleted: 0 characters (no-op)")
            return
        if n > len(self._current_text):
            raise ValueError(f"Cannot delete {n} characters, only {len(self._current_text)} available")
        
        # Get the text that will be deleted
        deleted_text = self._current_text[-n:]
        # Save current state for undo (we need to know what to reinsert)
        self._undo_stack.push(("insert", deleted_text))
        # Clear redo stack when new action is performed
        self._redo_stack = Stack()
        # Update current text
        self._current_text = self._current_text[:-n]
        # Record in history
        self._history.append(f"Deleted: '{deleted_text}'")
    
    def undo(self):
        """Undo the last action.
        
        Raises:
            IndexError: If there are no actions to undo.
        """
        if self._undo_stack.is_empty():
            raise IndexError("No actions to undo")
        
        # Get the last action from undo stack
        action_type, action_data = self._undo_stack.pop()
        
        # Apply the reverse action
        if action_type == "delete":
            # We previously wrote text, so now we delete it
            text_to_delete = action_data  # This is the length of text that was written
            deleted_text = self._current_text[-text_to_delete:]
            self._current_text = self._current_text[:-text_to_delete]
            # Save the complementary action for redo
            self._redo_stack.push(("insert", deleted_text))
            self._history.append(f"Undo write: deleted '{deleted_text}'")
        elif action_type == "insert":
            # We previously deleted text, so now we insert it back
            text_to_insert = action_data  # This is the actual text that was deleted
            self._current_text += text_to_insert
            # Save the complementary action for redo
            self._redo_stack.push(("delete", len(text_to_insert)))
            self._history.append(f"Undo delete: inserted '{text_to_insert}'")
    
    def redo(self):
        """Redo the last undone action.
        
        Raises:
            IndexError: If there are no actions to redo.
        """
        if self._redo_stack.is_empty():
            raise IndexError("No actions to redo")
        
        # Get the last action from redo stack
        action_type, action_data = self._redo_stack.pop()
        
        # Apply the action
        if action_type == "insert":
            # We previously undid a delete, so now we insert the text back
            text_to_insert = action_data
            self._current_text += text_to_insert
            # Save the complementary action for undo
            self._undo_stack.push(("delete", len(text_to_insert)))
            self._history.append(f"Redo delete: inserted '{text_to_insert}'")
        elif action_type == "delete":
            # We previously undid a write, so now we delete the text again
            length_to_delete = action_data
            deleted_text = self._current_text[-length_to_delete:]
            self._current_text = self._current_text[:-length_to_delete]
            # Save the complementary action for undo
            self._undo_stack.push(("insert", deleted_text))
            self._history.append(f"Redo write: deleted '{deleted_text}'")
    
    def get_content(self):
        """Get the current text content.
        
        Returns:
            str: The current text.
        """
        return self._current_text
    
    def get_history(self):
        """Get the history of actions.
        
        Returns:
            list: A list of descriptive action strings.
        """
        return self._history.copy()  # Return a copy to prevent external modification

    def show(self):
        """Alias requerido: mostrar el contenido actual."""
        return self.get_content()

    def history(self):
        """Alias requerido: mostrar el historial de acciones."""
        return self.get_history()