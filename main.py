import customtkinter as ctk
import customtkinter
from tkinter import filedialog
import os
from CTkMessagebox import CTkMessagebox
import string
import sys
        
class MyFrame(customtkinter.CTkFrame):

    def __init__(self, master, text_widget, button_fg_color,button_hover_color, **kwargs):
        super().__init__(master, **kwargs)
        self.text_widget = text_widget
        self.file_path = None
        self.text_alignment = "left"
        self.text_widget.bind("<Control-o>", self.open_file) 
        self.text_widget.bind("<Control-s>", self.save_file)
        self.text_widget.bind("<Control-S>", self.save_file_as)
        self.text_widget.bind("<Control-n>", self.new_file)
        self.text_widget.bind("<Control-j>", self.Everything_in_the_middle)

        # add widgets onto the frame
        self.new_file_button = customtkinter.CTkButton(self, text="New File", command=self.new_file, fg_color=button_fg_color, hover_color=button_hover_color)
        self.new_file_button.grid(row=0, column=0, padx=2,)
        
        self.open = customtkinter.CTkButton(self, text="Open" , command=self.open_file, fg_color=button_fg_color, hover_color=button_hover_color)
        self.open.grid(row=0, column=1, padx=2)
        
        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_file, fg_color=button_fg_color, hover_color=button_hover_color)
        self.save_button.grid(row=0, column=2, padx=2)

        self.save_as_button = customtkinter.CTkButton(self, text="Save As", command=self.save_file_as, fg_color=button_fg_color, hover_color=button_hover_color)
        self.save_as_button.grid(row=0, column=3, padx=2)
        
        self.justify = customtkinter.CTkButton(self, text="Center", command=self.Everything_in_the_middle, fg_color=button_fg_color, hover_color=button_hover_color)
        self.justify.grid(row=0, column=4, padx=2)

    def new_file(self, event=None):
        self.text_widget.delete("1.0", "end")
        self.file_path = None
        return "break"

    def open_file(self, event=None):
        # Open a file dialog and read the selected file's content
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.file_path = file_path
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", content)
        return "break"
    
    def save_file(self, event=None):
        if self.file_path:
            # Save the current content to the last opened/saved file
            with open(self.file_path, "w") as file:
                content = self.text_widget.get("1.0", "end-1c")
                file.write(content)
        else:
            # If no file path exists, use "Save As" instead
            self.save_file_as()

    def save_file_as(self, event=None):
        # Open a file dialog to save the content of the text widget
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        with open(self.file_path, "w") as file:
                content = self.text_widget.get("1.0", "end-1c")
                file.write(content)
        
    def Everything_in_the_middle(self, event=None):
        self.contained_text = self.text_widget.get("1.0", "end-1c")
        self.text_widget.delete("1.0", "end-1c")
        self.text_widget.insert("1.0", self.contained_text)
        if self.text_alignment == "left":
            # Align text to the center
            self.text_widget.tag_config("align", justify="center")
            self.text_alignment = "center"
            self.justify.configure(text="Right")
        elif self.text_alignment == "center":
            # Align text to the right
            self.text_widget.tag_config("align", justify="right")
            self.text_alignment = "right"
            self.justify.configure(text="left")
        else:
            # Align text to the left
            self.text_widget.tag_config("align", justify="left")
            self.text_alignment = "left"
            self.justify.configure(text="Center")
        
        self.text_widget.tag_add("align", 1.0, "end")

class zeneditor(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("400,400")
        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")
        self.button_fg_color = "#3a2dad"
        self.button_hover_color = "#424572"
        self.title(" Zen Notepad")
        self.dontshowagain = 0

        if getattr(sys, 'frozen', False):
            # If the application is running as a single file, use the _MEIPASS directory.
             bundle_dir = sys._MEIPASS
        else:
            # Otherwise, use the regular assets directory.
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(bundle_dir, "assets", "icon.ico")
        self.iconbitmap(self.icon_path)
        
        self.mini_font = ctk.CTkFont(family="Candara", size=28)
        self.text = ctk.CTkTextbox(self, width=400, height=300, font=self.mini_font , wrap='word' , activate_scrollbars=False, undo=True)

        # Create a menu bar
        self.menu = MyFrame(master=self, text_widget=self.text, button_fg_color=self.button_fg_color, button_hover_color = self.button_hover_color)
        self.menu.pack(side="top", fill="both")
        self.text.pack(side="top", expand="True", fill="both", ipadx=80, ipady=80, padx=5, pady=5)
        
        # Add a toggle button to hide/show the menu
        self.toggle_menu_button = ctk.CTkButton(self.menu, text="Hide Menu", command=self.toggle_menu, hover_color = self.button_hover_color, fg_color=self.button_fg_color)
        self.toggle_menu_button.grid(row=0, column=5, padx=2)
        self.sample_text = "(Click on New file to remove this text)\nThis is a distraction-free notepad app \ndesigned to help you capture ideas,\n jot down notes, and stay focused\n on what matters most.\n Zen Notepad helps you concentrate on \n your current thoughts and ideas,\n allowing everything else to\n gently fade into the background.\n\n  Just hover your mouse over the text to get started,\n let your focus flow effortlessly.\n Stay present, stay focused.\n"
        self.sample_text += "\n".join(f"Enjoy Peaceful Writting.. " for _ in range(1, 41))
        self.text.insert("1.0", self.sample_text)
        self.text.tag_config("center", justify="center")
        self.text.tag_add("center", 1.0, "end")

        # Bind mouse motion to the update_line_colors function
        self.text.bind("<Motion>", self.update_line_color)
        self.text.bind("<Return>", self.update_line_color_on_enter)
        self.text.bind("<space>", self.update_line_color_on_enter)
        self.text.bind("<Control-h>", self.toggle_menu)
        self.text.bind("<Control-BackSpace>", self.delete_previous_word)
        self.text.bind("<F11>", self.toggle_fullscreen)
        
        self.toplevel_window = None
        
    def update_line_color(self, event):
        # Get the index of the line where the mouse is currently
        self.index = self.text.index(f"@{event.x},{event.y}")
        self.current_line = int(self.index.split('.')[0])
        
        # Get total number of lines
        self.num_lines = int(self.text.index('end-1c').split('.')[0])
        
        # Update colors based on distance from the current line
        for line in range(1, self.num_lines + 1):
            if line == self.current_line:
                # Highlight the line where the cursor is
                self.text.tag_add(f"line_{line}", f"{line}.0", f"{line}.end")
                self.text.tag_config(f"line_{line}", foreground="white")
            else:
                # Fade out other lines to shades of grey
                distance = abs(self.current_line - line)
                fade_value = min(distance * 16, 180)
                grey_color = f"#{255 - fade_value:02x}{255 - fade_value:02x}{255 - fade_value:02x}"
                self.text.tag_add(f"line_{line}", f"{line}.0", f"{line}.end")
                self.text.tag_config(f"line_{line}", foreground=grey_color)
        
        self.text.update_idletasks()
        
    def update_line_color_on_enter(self, event):
        # Get the index of the line where the mouse is currently
        self.current_index = self.text.index(ctk.INSERT)
        
        self.current_line = int(self.current_index.split(".")[0])
        self.num_lines = int(self.text.index('end-1c').split('.')[0])

        for line in range(1, self.num_lines + 1):
            if line == self.current_line:
                # Highlight the line where the cursor is
                self.text.tag_add(f"line_{line}", f"{line}.0", f"{line}.end")
                self.text.tag_config(f"line_{line}", foreground="white")
            else:
                # Fade out other lines to shades of grey
                distance = abs(self.current_line - line)
                fade_value = min(distance * 16, 180)
                grey_color = f"#{255 - fade_value:02x}{255 - fade_value:02x}{255 - fade_value:02x}"
                self.text.tag_add(f"line_{line}", f"{line}.0", f"{line}.end")
                self.text.tag_config(f"line_{line}", foreground=grey_color)
        
        self.text.update_idletasks()
    
    ### menu functions ####
    def toggle_menu(self, event=None):
        if self.menu.winfo_viewable():
            self.menu.pack_forget()
            self.toggle_menu_button.configure(text="Show Menu")
            instructions = (
            "Navigating the Application:\n\n"
            "To quickly access the application's menu, use the following shortcut:\n\n"
            "• Show/Hide Menu    -> Ctrl + H\n"
            "• Close this window   -> Alt + F4\n\n"
            "For common tasks, consider these handy shortcuts:\n\n"
            "• New File        -> Ctrl + N\n"
            "• Open File       -> Ctrl + O\n"
            "• Save File       -> Ctrl + S\n"
            "• Save As         -> Ctrl + Shift + S\n"
            "• Align Text      -> Ctrl + J\n"
            "• Undo              -> Ctrl + Z\n"
            "• Redo              -> Ctrl + Y\n"
            "• Delete last Word -> Ctrl + Backspace\n"
             )
            if self.dontshowagain == 0:
                msg = CTkMessagebox(title="Info", message=instructions, width=600 , height=100, icon=self.icon_path, option_1="OK", option_2="Don't show this again", button_color="#0754b0", button_hover_color=self.button_hover_color)
                if msg.get() == "Don't show this again":
                    self.dontshowagain = 1
                       
        else:
            self.text.pack_forget()
            self.menu.pack(side="top", fill="x")
            self.toggle_menu_button.configure(text="Hide Menu")
            self.text.pack(side="top", expand="True", fill="both", ipadx=80, ipady=80, padx=5, pady=5)
        
        return "break"
    
   

    def delete_previous_word(self, event=None):
        cursor_pos = self.text.index(ctk.INSERT)
        before_cursor = self.text.get("1.0", cursor_pos)
        
        if before_cursor.strip(): 
            stripped_text = before_cursor.rstrip()
            last_space_index = stripped_text.rfind(" ")
            if last_space_index == -1:
                start_pos = "1.0"
            else:
                start_pos = f"1.0 + {last_space_index + 1}c"
            self.text.delete(start_pos, cursor_pos)
        
        return "break"
    
    def toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))
        return "break"


app = zeneditor()
app.mainloop()
        
    
