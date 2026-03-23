import tkinter as tk
from tkinter import messagebox
from editor import TextEditor

class TextEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Editor con Historial de Acciones")
        self.root.geometry("600x500")
        
        # Instantiate the TextEditor
        self.editor = TextEditor()
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for the current text display
        text_frame = tk.LabelFrame(self.root, text="Texto Actual", padx=10, pady=10)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.text_display = tk.Text(text_frame, height=5, width=60, state="disabled")
        self.text_display.pack(fill="both", expand=True)
        
        # Frame for write controls
        write_frame = tk.LabelFrame(self.root, text="Escribia su Texto", padx=10, pady=10)
        write_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(write_frame, text="Texto:").grid(row=0, column=0, sticky="w")
        self.write_entry = tk.Entry(write_frame, width=40)
        self.write_entry.grid(row=0, column=1, padx=5)
        tk.Button(write_frame, text="Escribir", command=self.handle_write).grid(row=0, column=2, padx=5)
        
        # Frame for delete controls
        delete_frame = tk.LabelFrame(self.root, text="Borrar Caracteres", padx=10, pady=10)
        delete_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(delete_frame, text="Número de caracteres:").grid(row=0, column=0, sticky="w")
        self.delete_entry = tk.Entry(delete_frame, width=10)
        self.delete_entry.grid(row=0, column=1, padx=5, sticky="w")
        tk.Button(delete_frame, text="Borrar", command=self.handle_delete).grid(row=0, column=2, padx=5)
        
        # Frame for undo/redo buttons
        action_frame = tk.Frame(self.root, padx=10, pady=10)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(action_frame, text="Deshacer", command=self.handle_undo).pack(side="left", padx=5)
        tk.Button(action_frame, text="Rehacer", command=self.handle_redo).pack(side="left", padx=5)
        
        # Frame for history log
        history_frame = tk.LabelFrame(self.root, text="Historial de Acciones", padx=10, pady=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.history_display = tk.Text(history_frame, height=8, width=60, state="disabled")
        self.history_display.pack(fill="both", expand=True)
        
        # Initial update of displays
        self.update_displays()
    
    def update_displays(self):
        """Update the text and history displays."""
        # Update current text display
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, self.editor.get_content())
        self.text_display.config(state="disabled")
        
        # Update history display
        self.history_display.config(state="normal")
        self.history_display.delete(1.0, tk.END)
        for action in self.editor.get_history():
            self.history_display.insert(tk.END, action + "\n")
        self.history_display.config(state="disabled")
    
    def handle_write(self):
        """Handle the write button click."""
        text = self.write_entry.get()
        if not text:
            messagebox.showerror("Error", "No se puede escribir texto vacío")
            return
        
        try:
            self.editor.write(text)
            self.write_entry.delete(0, tk.END)  # Clear the entry
            self.update_displays()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def handle_delete(self):
        """Handle the delete button click."""
        try:
            raw = self.delete_entry.get().strip()
            n = int(raw)
            self.editor.delete(n)
            self.delete_entry.delete(0, tk.END)  # Clear the entry
            self.update_displays()
        except ValueError as e:
            messagebox.showerror("Error", str(e) if raw else "Por favor ingrese un número entero")
    
    def handle_undo(self):
        """Handle the undo button click."""
        try:
            self.editor.undo()
            self.update_displays()
        except IndexError as e:
            messagebox.showerror("Error", str(e))
    
    def handle_redo(self):
        """Handle the redo button click."""
        try:
            self.editor.redo()
            self.update_displays()
        except IndexError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorGUI(root)
    root.mainloop()
