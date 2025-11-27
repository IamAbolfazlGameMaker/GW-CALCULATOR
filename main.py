import customtkinter as ctk

# Configure the application's appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") # We keep the default theme but override colors below

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GW CALCULATOR")
        self.geometry("380x480")
        self.resizable(False, False)

        self.expression = ""

        # --- Display (Entry Widget) ---
        self.display = ctk.CTkEntry(self, 
                                    font=ctk.CTkFont(size=35), 
                                    justify="right",
                                    border_width=0,
                                    fg_color="#2B2B2B", # Deep dark gray background
                                    text_color="#FFFFFF", # White text for display
                                    height=70)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(20, 10), sticky="nsew")

        # --- Buttons Layout ---
        # NOTE: Changed 'orange' to 'operator' in the list
        buttons = [
            ('C', 1, 0, 'red'), ('(', 1, 1), (')', 1, 2), ('/', 1, 3, 'operator'),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3, 'operator'),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3, 'operator'),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3, 'operator'),
            ('0', 5, 0, None, 2), ('.', 5, 2), ('=', 5, 3, 'green')
        ]

        # Loop through the list to create and place buttons
        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            color = btn[3] if len(btn) > 3 else None
            colspan = btn[4] if len(btn) > 4 else 1

            if text == 'C':
                command = self.clear_display
            elif text == '=':
                command = self.calculate_result
            else:
                command = lambda t=text: self.add_to_expression(t)
            
            self.create_button(text, row, col, command, color, colspan)

        # Configure row and column weights for responsiveness
        self.grid_rowconfigure(0, weight=1)
        for i in range(1, 6):
            self.grid_rowconfigure(i, weight=2)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
            
        # Keyboard Binding
        self.bind_keyboard_events()

    # Function to create and style a CTkButton (AESTHETIC CHANGES HERE)
    def create_button(self, text, row, col, command, color=None, colspan=1):
        # NEW: Default button color for numbers and non-operators
        fg_color = "#414141" 
        hover_color = "#555555" 
        
        if color == 'red':
            fg_color = "#D24545" # Red for Clear
            hover_color = "#E66A6A"
        elif color == 'green':
            fg_color = "#2AAA8A" # Green for Equals
            hover_color = "#3BDBB2"
        elif color == 'operator': # NEW: Teal/Cyan color for operators
            fg_color = "#00A8A8" 
            hover_color = "#00CACA"
        
        btn = ctk.CTkButton(self, 
                            text=text, 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            command=command,
                            fg_color=fg_color,
                            hover_color=hover_color,
                            height=60,
                            corner_radius=12) # Increased radius
        btn.grid(row=row, column=col, columnspan=colspan, padx=6, pady=6, sticky="nsew") # Increased padding

    # --- Calculator Logic Functions (No change) ---

    def add_to_expression(self, value):
        self.expression += str(value)
        self.display.delete(0, "end")
        self.display.insert(0, self.expression)

    def clear_display(self):
        self.expression = ""
        self.display.delete(0, "end")

    def backspace(self, event=None):
        self.expression = self.expression[:-1]
        self.display.delete(0, "end")
        self.display.insert(0, self.expression)
        
    def calculate_result(self, event=None):
        try:
            result = str(eval(self.expression))
            self.display.delete(0, "end")
            self.display.insert(0, result)
            self.expression = result
        except Exception as e:
            self.display.delete(0, "end")
            self.display.insert(0, "Error")
            self.expression = ""

    def bind_keyboard_events(self):
        self.bind('<Key>', self.key_press)
        self.bind('<Return>', self.calculate_result) 
        self.bind('<KP_Enter>', self.calculate_result) 
        self.bind('<Escape>', lambda event: self.clear_display()) 
        self.bind('<BackSpace>', self.backspace) 
        self.bind('<Delete>', self.clear_display)

    def key_press(self, event):
        key = event.char
        if key == 'x' or key == 'X':
            key = '*'
        if key in '0123456789+-*/.()':
            self.add_to_expression(key)


# --- Run the Application ---
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
    