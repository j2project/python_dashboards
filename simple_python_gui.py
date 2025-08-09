import tkinter as tk
from tkinter import ttk
import random

class EnvironmentalDataGUI:
    def __init__(self, root):
        """
        Initialize the GUI application with all components
        """
        self.root = root
        self.root.title("Environmental Data Viewer")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Data sets - primary and alternate data
        self.primary_data = self.generate_primary_data()
        self.alternate_data = self.generate_alternate_data()
        self.current_data = self.primary_data
        self.showing_alternate = False
        
        self.setup_ui()
    
    def generate_primary_data(self):
        """Generate primary environmental data for three locations"""
        return [
            ["Amazon Rainforest", "28.5°C", "0.1 PSU", "7.2 mg/L", "6.8", "25 NTU", "Jaguar"],
            ["Great Barrier Reef", "26.2°C", "35.5 PSU", "8.1 mg/L", "8.1", "5 NTU", "Clownfish"],
            ["Siberian Tundra", "-12.8°C", "0.3 PSU", "12.5 mg/L", "7.4", "8 NTU", "Arctic Fox"]
        ]
    
    def generate_alternate_data(self):
        """Generate alternate environmental data showing different readings"""
        return [
            ["Amazon Rainforest", "31.2°C", "0.2 PSU", "6.8 mg/L", "6.5", "32 NTU", "Toucan"],
            ["Great Barrier Reef", "24.8°C", "36.1 PSU", "7.9 mg/L", "8.2", "3 NTU", "Sea Turtle"],
            ["Siberian Tundra", "-18.5°C", "0.4 PSU", "13.2 mg/L", "7.1", "12 NTU", "Snowy Owl"]
        ]
    
    def setup_ui(self):
        """
        Create and arrange all UI components
        """
        # ================================================================
        # HEADER TITLE
        # ================================================================
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🌍 Environmental Sensor Data Viewer",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # ================================================================
        # DATA TABLE
        # ================================================================
        table_frame = tk.Frame(self.root, bg='#f0f0f0')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Table title
        table_title = tk.Label(
            table_frame,
            text="Current Environmental Readings",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#34495e'
        )
        table_title.pack(pady=(0, 10))
        
        # Create Treeview (table widget)
        self.tree = ttk.Treeview(table_frame)
        self.tree.pack(fill='both', expand=True, padx=20)
        
        # Define columns
        columns = ['Location', 'Temperature', 'Salinity', 'Dissolved O2', 'pH', 'Turbidity', 'Organism']
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        # Configure column headings and widths
        column_widths = [140, 100, 100, 100, 80, 100, 120]
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[i], anchor='center')
        
        # Add scrollbar for table
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Populate table with initial data
        self.populate_table()
        
        # ================================================================
        # BUTTON
        # ================================================================
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.toggle_button = tk.Button(
            button_frame,
            text="📊 Show Alternative Data",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            relief='raised',
            borderwidth=2,
            padx=20,
            pady=10,
            command=self.toggle_data
        )
        self.toggle_button.pack(pady=10)
        
        # ================================================================
        # PROJECT DESCRIPTION PARAGRAPH
        # ================================================================
        desc_frame = tk.Frame(self.root, bg='#ecf0f1', relief='sunken', borderwidth=2)
        desc_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        desc_title = tk.Label(
            desc_frame,
            text="About This Project",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        desc_title.pack(pady=(10, 5))
        
        description_text = """This Python GUI application demonstrates how to create user interfaces using Tkinter, 
Python's standard GUI toolkit. The application displays environmental sensor data from three distinct 
geographical locations: Amazon Rainforest, Great Barrier Reef, and Siberian Tundra. 

Key UI components include:
• Header with styled title and emoji
• Interactive data table (Treeview widget) showing environmental parameters
• Button that toggles between different data sets when clicked
• Text description area explaining the project

This simple interface showcases fundamental GUI programming concepts including event handling, 
data visualization, and component layout management. Unlike web-based frameworks like Dash, 
Tkinter creates native desktop applications that run directly on the operating system."""
        
        desc_label = tk.Label(
            desc_frame,
            text=description_text,
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#34495e',
            justify='left',
            wraplength=750,  # Wrap text at 750 pixels
            padx=20,
            pady=10
        )
        desc_label.pack()
        
        # ================================================================
        # STATUS BAR
        # ================================================================
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready | Showing Primary Data Set",
            font=('Arial', 10),
            bg='#34495e',
            fg='white',
            anchor='w'
        )
        self.status_label.pack(fill='x', padx=10, pady=5)
    
    def populate_table(self):
        """
        Clear and repopulate the table with current data
        """
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert current data
        for row in self.current_data:
            self.tree.insert('', 'end', values=row)
        
        # Add some visual styling to rows
        for i, item in enumerate(self.tree.get_children()):
            if i % 2 == 0:  # Alternate row colors
                self.tree.set(item, '#1', self.tree.set(item, '#1'))  # Keep data same, just for styling
    
    def toggle_data(self):
        """
        Event handler for button click - toggles between data sets
        """
        if self.showing_alternate:
            # Switch back to primary data
            self.current_data = self.primary_data
            self.toggle_button.config(
                text="📊 Show Alternative Data",
                bg='#3498db',
                activebackground='#2980b9'
            )
            self.status_label.config(text="Ready | Showing Primary Data Set")
            self.showing_alternate = False
        else:
            # Switch to alternate data
            self.current_data = self.alternate_data
            self.toggle_button.config(
                text="📈 Show Primary Data",
                bg='#e67e22',
                activebackground='#d35400'
            )
            self.status_label.config(text="Ready | Showing Alternative Data Set")
            self.showing_alternate = True
        
        # Refresh the table with new data
        self.populate_table()
        
        # Add a brief visual feedback
        self.root.after(100, self.button_flash)
    
    def button_flash(self):
        """
        Brief visual feedback when button is pressed
        """
        original_relief = self.toggle_button.cget('relief')
        self.toggle_button.config(relief='sunken')
        self.root.after(150, lambda: self.toggle_button.config(relief=original_relief))

def main():
    """
    Main function to create and run the GUI application
    """
    # Create the main window
    root = tk.Tk()
    
    # Create the application
    app = EnvironmentalDataGUI(root)
    
    # Start the GUI event loop
    print("Starting Environmental Data Viewer...")
    print("Close the window to exit the application.")
    root.mainloop()
    print("Application closed.")

# Run the application if this file is executed directly
if __name__ == "__main__":
    main()